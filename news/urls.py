from django.urls import path, include
# Импортируем созданное нами представление
from .views import CategoryView, SubscribeView, PostsList, PostDetail, PostsSearch, NewsCreateView, ArticleCreateView, NewsDeleteView, NewsUpdateView, ArticleDeleteView, ArticleUpdateView


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
    path('news/', PostsList.as_view(),name='posts_list'), 
    path('', include('protect.urls')),


    path('category/<int:pk>/', CategoryView.as_view(), name='category_list'),
    path('category/<int:pk>/subscribe/', SubscribeView.as_view(), name='category_subscribe'),

    path('sign/', include('sign.urls')),
 
    path('news/<int:pk>', PostDetail.as_view(),name='post_detail'),
    path('news/search/', PostsSearch.as_view(), name='post_search'),

    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    
    # Страницы редактирования
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    
    # Страницы удаления
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),

   
]