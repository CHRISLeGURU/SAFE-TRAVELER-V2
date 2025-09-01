from django.contrib import admin
from .models import CustomUser

#on fait la meme chose avec  la table CustomerUser issu du model
admin.site.register(CustomUser)