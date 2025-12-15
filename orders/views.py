from django.shortcuts import render, get_object_or_404
from utils.pagination import CustomPagination
from rest_framework import views,generics, permissions, status
from rest_framework.response import Response
from orders.serializers import OrderSerializer
from django.db import transaction
from Products.models import Product
from orders.models import Order, OrderProduct

# Create your views here.
class OrderViews(generics.GenericAPIView):
    serializer_class = OrderSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(buyer=user).order_by("-created_at")
    
    def get(self, request):
        orders = self.get_queryset()
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(orders, many=True)
        return Response (data = serializer.data, status = 200)

    def post(self,request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        products = serializer.validated_data.get("products", [])
        with transaction.atomic():
            order_total = 0
            order = Order.objects.create(buyer=user, order_total=0)
            for prd in products:
                product = get_object_or_404(Product, id= prd["id"])
                quantity = prd["quantity"]
                if product.owner == user:
                    return Response(data={"error":"You can not buy your own product"}, status=400)
                if product.quantity < quantity:
                    return Response(data={"error":"Product does not have up to the desired quantity"}, status=400)
                amount = quantity * product.price
                order_total += amount
                OrderProduct.objects.create(product=product, order=order,
                                            quantity=quantity, amount=amount)
                product.quantity -= quantity
                product.save()
            order.order_total = order_total
            order.save()
        return Response(data=serializer.data, status=201)
