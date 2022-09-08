from django.contrib import admin
from accounts.models import FailedLogin

# Register your models here.
class FailedLoginAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'date', 'reason')
    list_display_links = ('id','user')
    list_filter = ('user',)
    search_fields = ('user',)

admin.site.register(FailedLogin, FailedLoginAdmin)