from django.contrib import admin
from .models import Inventory
#from import_export.admin import ImportExportModelAdmin

# Register your models here.
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'category', 'brand', 'quantity','price', 'discount', 'is_displayed')
    list_display_links = ('id', 'name')
    list_editable = ('is_displayed',)
    list_filter = ('category', 'brand')
    search_fields = ('name',)

admin.site.register(Inventory, InventoryAdmin)


admin.site.site_header = "Spares Shop KE"