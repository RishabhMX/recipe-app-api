"""
Django Admin Customisation
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _  #used to add translations and '_' is used as shortcut can be written anything instead of that

from core import models

class UserAdmin(BaseUserAdmin): #customising the admin
    """Define the admin page for users"""
    ordering=['id']
    list_display=['email','name']
    #adding custom fieldsets
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}), #instead of a tuple any iterable object like a list can also be inserted
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login'] #cannot be edited
    add_fieldsets = (
        (None, {
            'classes': ('wide',), #custom is,used to add custom css classes to make the page neater
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )



admin.site.register(models.User,UserAdmin) #add UserAdmin or else django will use default model manager
admin.site.register(models.Recipe)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)


