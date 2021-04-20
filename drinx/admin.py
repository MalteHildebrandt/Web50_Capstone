from django.contrib import admin
from .models import User, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "display_order", "is_active", "description")

# Register your models here.
admin.site.register(User)
admin.site.register(Category, CategoryAdmin)
