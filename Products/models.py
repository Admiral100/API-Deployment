from django.db import models
from authentication.models import User
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class Product(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=250)
    description = models.TextField(null = True, blank = True)
    price = models.IntegerField()
    picture = models.ImageField(upload_to="product/", null=True, blank=True)
    quantity = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return f'{self.name} N{self.price} {self.quantity}qty by {self.owner.firstname} {self.owner.lastname}'