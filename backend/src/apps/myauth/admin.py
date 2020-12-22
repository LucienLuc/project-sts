from django.contrib.auth import get_user_model as user_model
User = user_model()
from django.contrib.auth.admin import UserAdmin
# from src.apps.myauth.main.models import User

from django.contrib import admin

admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.register(User, UserAdmin)