from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment

user1 = User.objects.create_user('user1')
user2 = User.objects.create_user('user2')

author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

category1 = Category.objects.create(name='Технологии')
category2 = Category.objects.create(name='Медицина')
category3 = Category.objects.create(name='Спорт')
category4 = Category.objects.create(name='Политика')

post1 = Post.objects.create(author=author1, post_type='AR', title='Технологиеские новости', content='какой то там текст')
post2 = Post.objects.create(author=author2, post_type='AR', title='Спорт новости', content='какой то там текст')
post3 = Post.objects.create(author=author1, post_type='NW', title='Политические новости', content='какой то там текст')

post1.categories.add(category1, category2)  
post2.categories.add(category3)
post3.categories.add(category4)

comment1 = Comment.objects.create(post=post1, user=user2, content='Классная новость')
comment2 = Comment.objects.create(post=post2, user=user1, content='Интересно')
comment3 = Comment.objects.create(post=post3, user=user2, content='Спасибо')
comment4 = Comment.objects.create(post=post1, user=user1, content='Я согласен')

post1.like()
post1.like()
post2.like()
post3.dislike()
comment1.like()
comment2.like()
comment3.dislike()
comment4.like()

author1.update_rating()
author2.update_rating()

best_author = Author.objects.order_by('-rating').first()
print(f'Лучший пользователь: {best_author.user.username}, рейтинг: {best_author.rating}')

best_post = Post.objects.order_by('-rating').first()
print(f'''Лучшая статья:
Дата: {best_post.created_at}
Автор: {best_post.author.user.username}
Рейтинг: {best_post.rating}
Заголовок: {best_post.title}
Превью: {best_post.preview()}''')

comments = Comment.objects.filter(post=best_post)
for comment in comments:
    print(f'Дата: {comment.created_at}, Пользователь: {comment.user.username}, Рейтинг: {comment.rating}, Текст: {comment.content}')
