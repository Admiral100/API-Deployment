from django.shortcuts import render
from rest_framework import views,generics
from rest_framework.response import Response
from authentication.serializers import (
    SignupSerializer,
    LoginSerializer,
    UserSerializer
    )
from authentication.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q

# Create your views/logic here.

class SignupView(generics.GenericAPIView):
    serializer_class = SignupSerializer
    def post(self,request):
        serializer=self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.pop("password")
        user = serializer.save()
        user.set_password(password)
        user.save()
        return Response(data=serializer.data,status=200)
    
class loginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer=self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data,status=200)
    
class UserView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = UserSerializer
    def get_queryset(self):
        search = self.request.query_params.get("search")
        users = User.objects.all().order_by("-created_at")
        if search:
            users = users.filter(Q(firstname__icontains=search) | Q(lastname__icontains=search)| Q(email__icontains = search))
        return users
    
    @swagger_auto_schema(
            manual_parameters = [
                openapi.Parameter(name="search", in_ = openapi.IN_QUERY,description= "search by name or email",type = openapi.TYPE_STRING, required= False)
            ]
    )
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many = True)
        return Response(data = serializer.data, status=200)