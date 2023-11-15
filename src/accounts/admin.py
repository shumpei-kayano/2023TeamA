from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser, MelimitUser, MelimitStore

# Register your models here.

# CustomUserChangeFormはユーザー編集時に使用するフォーム
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
    list_display = ('username','email','city')

    # ユーザー編集時に必要なフィールド(管理画面で入力するフィールド)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username','postal_code','prefecture','city','address','phone_number',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # ユーザー作成時に必要なフィールド(登録画面で入力するフィールド)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', ),
        }),
    )

# 同じようにMelimitUserとMelimitStoreの管理画面を定義する
class MelimitUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = BaseUserAdmin.add_form
    model = MelimitUser
    list_display = ('username','city')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username','postal_code','prefecture','city','address','phone_number',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email',),
        }),
    )

class MelimitStoreAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = BaseUserAdmin.add_form
    model = MelimitStore
    list_display = ('username','city')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username','postal_code','prefecture','city','address','phone_number', 'store_image', 'site_url',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'store_image', 'site_url', ),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(MelimitUser, MelimitUserAdmin)
admin.site.register(MelimitStore, MelimitStoreAdmin)