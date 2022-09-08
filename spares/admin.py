from django.contrib import admin
from .models import Inventory, Category, Brand
#from import_export.admin import ImportExportModelAdmin

# Register your models here.
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'category','brand', 'quantity','price', 'discount', 'is_displayed')
    list_display_links = ('id', 'name')
    list_editable = ('is_displayed',)
    list_filter = ('category', 'brand')
    search_fields = ('name',)

admin.site.register(Inventory, InventoryAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand_name')

admin.site.register(Brand, BrandAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')

admin.site.register(Category, CategoryAdmin)

admin.site.site_header = "Spares Shop KE"