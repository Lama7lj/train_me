# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager

from phonenumber_field.modelfields import PhoneNumberField

class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'

class MyCustomUserManager(BaseUserManager):
    def create_user(self, email_id, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email_id:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=MyCustomUserManager.normalize_email(email_id),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name=None):
        u = self.create_user(email_id=email, password=password, first_name=first_name, last_name=last_name)
        u.is_superuser = True
        u.is_staff = True
        u.save(using=self._db)
        return u

class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, default="female")
    email = models.CharField(max_length=100, primary_key=True)
    phone_number = PhoneNumberField(blank=True)

    objects = MyCustomUserManager()


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]
    
    

class InterviewAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    about_yourself = models.TextField()
    hear_about = models.TextField()
    company_info = models.TextField()
    apply_position = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interview Answer by {self.user} at {self.timestamp}"

