from django.contrib import admin

# Register your models here.
from .models import WebauthnRegistration, WebauthnAuthentication, WebauthnCredentials, Profile

admin.site.register(WebauthnRegistration)
admin.site.register(WebauthnAuthentication)
admin.site.register(WebauthnCredentials)
admin.site.register(Profile)

