from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser, MelimitUser, MelimitStore

# Register your models here.

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = '__all__'
class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = BaseUserAdmin.add_form
    model = CustomUser
    list_display = ('username','city')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username','postal_code','prefecture','city','address','phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(MelimitUser)
admin.site.register(MelimitStore)