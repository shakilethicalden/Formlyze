from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, HealthCare, Form, FormResponse
# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'username',  'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )
    
    

admin.site.register(User, CustomUserAdmin)
admin.site.register(HealthCare)
admin.site.register(Form)
admin.site.register(FormResponse)


