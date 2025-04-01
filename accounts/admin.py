from django.contrib import admin
from .models import CustomUser  # Import your CustomUser model

admin.site.register(CustomUser)  # Register it in the Django admin panel
