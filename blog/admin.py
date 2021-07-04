from django.contrib import admin

from blog.models import BlogPost, Category, SubCategory


admin.site.register(BlogPost)
admin.site.register(Category)
admin.site.register(SubCategory)