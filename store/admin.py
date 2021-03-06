from atexit import register
from csv import list_dialects
from django.contrib import admin
from .models import Category, Product, Author, Image, Promotion
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug',
                    'price', 'in_stock', 'created', 'updated']
    list_filter = ['in_stock', 'is_active']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug': ('title', )}

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['name']