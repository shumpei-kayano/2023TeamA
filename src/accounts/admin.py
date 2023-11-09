from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser, MelimitUserDetail, MelimitStoreDetail

# Register your models here.

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = '__all__'
class CustomUserAdmin(BaseUserAdmin):
    # ユーザー編集時に使用するフォーム
    form = CustomUserChangeForm
    # ユーザー作成時に使用するフォーム
    # 「BaseUserAdmin.add_form」でハッシュ化やバリデーションを行っている
    add_form = BaseUserAdmin.add_form
    # 一覧画面で表示する項目
    model = CustomUser
    list_display = ('username','city')

    # ユーザー編集時に必要なフィールド(管理画面で入力するフィールド)
    fieldsets = (
        (None, {'fields': ('email', 'password','is_typename')}),
        ('Personal info', {'fields': ('username','postal_code','prefecture','city','address','phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # ユーザー作成時に必要なフィールド(登録画面で入力するフィールド)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(MelimitUserDetail)
admin.site.register(MelimitStoreDetail)