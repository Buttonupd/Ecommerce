from django.db import models
from datetime import timedelta
from django.conf import settings
from django.urls import reverse
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils import timezone
from ecommerce.utils import random_string_generator, unique_key_generator

DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVATION_DAYS', 7)

class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, is_active= True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('users must have a password')

        user_obj = self.model(
            email =self.normalize_email(email),
            full_name = full_name

        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj


        def create_staff_user(self, email, full_name=None, password= None):
            user = self.create_user(
                email, 
                full_name = full_name,
                password = password,
                is_staff = True,
                is_admin = True
            )
            return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique_key_generatorTrue)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
        