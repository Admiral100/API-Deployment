from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, firstname, lastname, email, phone, password = None, **extra_fields):
        if email is None or lastname is None or firstname is None or phone is None:
            raise TypeError("please fill in your correct information")
        user = self.model(firstname = firstname, lastname= lastname, email = self.normalize_email(email),phone= phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, firstname, lastname, email,  password = None, **extra_fields):
        if email is None or lastname is None or firstname is None:
            raise TypeError("please fill in your correct information")
        user = self.model(firstname = firstname, lastname= lastname, email = self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    firstname = models.CharField(max_length= 250)
    lastname = models. CharField(max_length=250)
    date_of_birth = models.DateField(null = True, blank = True)
    email = models.EmailField(unique=True, max_length=50,)
    pfp = models.ImageField(upload_to=u"profile/", null=True, blank=True)
    phone = models.CharField(unique=True, max_length=11, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstname", "lastname"]
    objects = UserManager()
    def __str__(self):
        return f'{self.firstname} {self.lastname} {self.email}'
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh': str(refresh),
            'access': str (refresh.access_token)
        }