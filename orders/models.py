from django.db import models
import uuid
from authentication.models import User
from Products.models import Product

# Create your models here.

class Order(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer_order")
    order_total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderProduct(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name="product_OrderProduct")
    order = models.ForeignKey(Order,on_delete=models.CASCADE, related_name="order_OrderProduct")
    quantity = models.IntegerField(blank= False)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return f'{self.id} ,{self.product} ,{self.quantity} {self.order} {self.quantity}, {self.amount}'