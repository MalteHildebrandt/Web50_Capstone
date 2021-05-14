from django.contrib import admin
from .models import User, Category, Article, ContentUnit

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "display_order", "is_active", "description")

class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description_short", "price", "stock", "is_active")
    filter_horizontal = ('categories',)

class ContentUnitAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

# Register your models here.
admin.site.register(User)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ContentUnit, ContentUnitAdmin)
