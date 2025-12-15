from django.shortcuts import render, get_object_or_404
from rest_framework import views,generics, permissions, status
from rest_framework.response import Response
from Products.serializers import ProductSerializers
from Products.models import Product
from drf_yasg import openapi
from orders.models import OrderProduct
from orders.serializers import OrderProductSerializer
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from utils.pagination import CustomPagination
# Create your views here.

class ProductViews(generics.GenericAPIView):
    serializer_class = ProductSerializers
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):

        prods = Product.objects.filter(quantity__gt = 0).order_by("-created_at")
        search = self.request.query_params.get("search")
        if search:
            prods = prods.filter(Q(name__icontains=search)| Q(description__icontains=search))
        return prods
    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=user)
        return Response(data = serializer.data, status = 201)
    @swagger_auto_schema(
            manual_parameters = [
                openapi.Parameter(name="search", in_ = openapi.IN_QUERY,description= "search by name or description",type = openapi.TYPE_STRING, required= False)
            ]
    )
    def get(self, request):
        prods  = self.get_queryset()
        page = self.paginate_queryset(prods)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(prods, many=True)
        return Response (data = serializer.data, status = 200)
    
class SingleProductView(generics.GenericAPIView):
    serializer_class = ProductSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        id = self.kwargs["id"]
        prod = get_object_or_404(Product, id=id)
        return prod
    def get(self, request, id):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset)
        return Response(data = serializer.data, status=200)
    def patch (self, request, id):
        queryset = self.get_queryset()
        user = request.user
        if queryset.owner != user:
            return Response(data={"message": "Unauthorized!"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.serializer_class(instance=queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data = serializer.data, status=201)
    
    def delete (self, request, id):
        queryset = self.get_queryset()
        user = request.user
        if queryset.owner != user:
            return Response(data={"message": "Unauthorized!"}, status=status.HTTP_401_UNAUTHORIZED)
        queryset.delete()
        return Response(status=204)

class UserProductsView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = ProductSerializers
    
    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        search = self.request.query_params.get("search")
        prods = Product.objects.filter(owner__id=user_id).order_by("-created_at")
        if search:
            prods = prods.filter(Q(name__icontains=search)| Q(description__icontains=search))
        return prods
    

    @swagger_auto_schema(
            manual_parameters = [
                openapi.Parameter(name="search", in_ = openapi.IN_QUERY,description= "search by name or description",type = openapi.TYPE_STRING, required= False)
            ]
    )
    def get(self,request,user_id):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many = True)
        return Response(data = serializer.data, status=200)

class ProductSalesView(generics.GenericAPIView):
    serializer_class = OrderProductSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        id = self.kwargs["id"]
        user = self.request.user
        product = get_object_or_404(Product, id=id, owner=user)
        return OrderProduct.objects.filter(product=product).order_by("-created_at")

    def get(self, request, id):
        prods  = self.get_queryset()
        page = self.paginate_queryset(prods)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(prods, many=True)
        return Response (data = serializer.data, status = 200)