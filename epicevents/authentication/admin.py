from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('first_name', 'last_name', 'email', 'role', 'is_active')
    list_filter = ('role',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name',)}),
        ('Personal info', {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('groups', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'role'),
        }),
    )
    search_fields = ('email', 'last_name',)
    ordering = ('role', 'last_name')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
