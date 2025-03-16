from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author
from .filters import ProductFilter
from .forms import PostForm
from django.urls import reverse_lazy


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
    

class NewsCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news_create.html'
    success_url = reverse_lazy('posts_list')  # куда перейти после создания

    def form_valid(self, form):
        post = form.save(commit=False)
        # Найти или создать автора для текущего пользователя
        author,created = Author.objects.get_or_create(user=self.request.user)
        post.author = author
        post.post_type = 'NW'  # Новость
        post.save()
        return super().form_valid(form)
    
class ArticleCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'article_create.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        author,created = Author.objects.get_or_create(user=self.request.user)
        post.author = author
        post.post_type = 'AR'  # Новость
        post.save()
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