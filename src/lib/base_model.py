from django.db import models
from django.contrib.auth.base_user import BaseUserManager


class BaseAbstractModel(models.Model):
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True

class AdminUserManager(BaseUserManager):
    # Custom user model manager where email is the UID

    def create_user(self, email, password, **extra_fields):
        # Create and save user with a given email, password

        if not email:
            raise ValueError(_('Email must be given'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user