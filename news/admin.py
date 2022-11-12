from django.contrib import admin
from .models import *
# Register your models here.

# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('header', 'author') # генерируем список имён всех полей для более красивого отображения


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')

admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(UserSubscribe)