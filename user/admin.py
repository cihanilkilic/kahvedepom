from django.contrib import admin
from .models import UserAddress, InviteCode


admin.site.register(UserAddress)
admin.site.register(InviteCode)