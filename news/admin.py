from django.contrib import admin
from .models import Category, Post, Author, PostCategory, Comment


class PostAdmin(admin.ModelAdmin, ):
    list_display = [field.name for field in Post._meta.fields] 
    list_filter = ( 'title', 'content') # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'category__name') # тут всё очень похоже на фильтры из запросов в базу
 
class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields] 
 
class AuthorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Author._meta.fields] 

class PostCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PostCategory._meta.fields] 

class CommetAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.fields] 



admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommetAdmin)


