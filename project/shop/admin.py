from django.contrib import admin
from . models import Category, Product, Cart, Favourite

"""
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'description')
admin.site.register(Category, CategoryAdmin)
"""

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Favourite)