from django.contrib import admin
from accounts.models import FailedLogin, User, Customer

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email', 'phone', 'dob')
    list_display_links = ('id','email')
    search_fields = ('email',)

admin.site.register(User, UserAdmin)

class FailedLoginAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'date', 'reason')
    list_display_links = ('id','user')
    list_filter = ('user',)
    search_fields = ('user',)

admin.site.register(FailedLogin, FailedLoginAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','email', 'phone')
    list_display_links = ('id','email')
    search_fields = ('email',)

admin.site.register(Customer, CustomerAdmin)