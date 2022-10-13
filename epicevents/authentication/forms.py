from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role')

    def save(self, commit=True):
        chars = "abcdefghijklmnopqrstuvwxyz0123456789!£$*"
        user = super().save(commit=False)
        password = get_random_string(40, chars)
        user.set_password(password)
        send_mail(
            'Admin Epic-Events',
            f'Hi {user.first_name} this is your password: {password}',
            'admin@epic-events.com',
            [f'{user.email}'],
            fail_silently=False,
        )
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name',
                  'last_name', 'groups', 'is_active')
