from django.contrib import admin
from .models import Post, Comment, Category, Tag


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
