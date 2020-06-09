from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.apps import apps

from hitchify.models import MyUser

models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass


# class MyUserInline(admin.StackedInline):
#     model = MyUser
#     can_delete = False
#     verbose_name_plural = 'myuser'
#
#
# class UserAdmin(BaseUserAdmin):
#     inlines = (MyUserInline,)
#
#
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)