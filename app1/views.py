from django.shortcuts import render
from rest_framework import views,generics,permissions
from rest_framework.response import Response
from authentication.permissions import IsStaff

# Create your views/logic here.

class Hiit(views.APIView):
    def get(self, request):
        feedback = {"message": "hello guys"}
        return Response(data=feedback, status=200)
    def post(self, request):
        feedback1 = {"message":"this is post"}
        return Response(data=feedback1, status=201)
    

class Hiit1(generics.GenericAPIView):
    def post(self, request):
        feedback3 = {"capital": "ikeja",
                     "zone": "southwest"}
        return Response(data=feedback3, status=200)
    def get(self, request):
        feedback4 = {"governor":"sanwo olu"}
        return Response(data=feedback4, status=201)
    def delete(self,request):
        feedback5 = {"message":"lagos is deleted"}
        return Response(data=feedback5, status=200)

class Hiit2(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStaff]
    def get(self, request):
        user = request.user
        token = user.tokens()
        acc = token["access"]
        feedback6 = {"message": f"welcome {user.firstname}. your token is {acc}"}
        return Response(data=feedback6, status=201)
   

    