from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    user_type_choices = [
        ('blind', 'Blind Student'),
        ('mute', 'Mute Student'),
        ('regular', 'Deaf & Physically Disabled Student'),
    ]
    user_type = models.CharField(max_length=10, choices=user_type_choices, default='regular')
    secret_code = models.CharField(max_length=10, blank=True, null=True)  # Only for mute students

    # Fix related name conflicts
    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)
