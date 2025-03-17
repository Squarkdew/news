from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from .models import Post, Author, Category
from .filters import ProductFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives 




class PostsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    

class PostsSearch(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

def notify_subscribers(post):
    categories = post.categories.all()
    subscribers = set()  # чтобы убрать дубликаты
    for category in categories:
        for user in category.subscribers.all():
            subscribers.add(user)

    if subscribers:
        subject = post.title
        html_content = render_to_string('email_notification.html', {'post': post})
        for user in subscribers:
            msg = EmailMultiAlternatives(
                subject=subject,
                body=f"Здравствуй, {user.username}. Новая статья в твоём любимом разделе!",
                from_email='',
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
     

class NewsCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news_create.html'
    success_url = reverse_lazy('posts_list')  # куда перейти после создания

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = Post.NEWS
        post.author = Author.objects.get(user=self.request.user)
        post.save()
        form.save_m2m()  # чтобы сохранить many-to-many поля

        # Отправляем уведомления
        categories = post.categories.all()
        for category in categories:
            subscribers = category.subscribers.all()
            notify_subscribers(post)

        return super().form_valid(form)
    


class ArticleCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'article_create.html'
    success_url = reverse_lazy('posts_list')

    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = Post.ARTICLE
        post.author, _ = Author.objects.get_or_create(user=self.request.user)
        post.save()
        form.save_m2m()

        notify_subscribers(post)  # уведомляем

        return super().form_valid(form)
    


class NewsUpdateView(UpdateView):
    model = Post
    template_name = 'news_edit.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})
    
class ArticleUpdateView(UpdateView):
    model = Post
    template_name = 'article_edit.html'
    form_class = PostForm

    def get_success_url(self): 
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})
    
class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'news_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('posts_list')
    
class ArticleDeleteView(DeleteView):
    model = Post
    template_name = 'article_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('posts_list') 
    
class SubscribeView(View):
    
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        if request.user.is_authenticated:
            if request.user in category.subscribers.all():
                category.subscribers.remove(request.user) 
            else:
                category.subscribers.add(request.user) 
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
class CategoryView(DetailView):
    model = Category
    template_name = 'category/category_detail.html'
    context_object_name = 'category'

