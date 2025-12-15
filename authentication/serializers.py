from rest_framework import serializers
from authentication.models import User
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth

class SignupSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    firstname = serializers.CharField(min_length = 2, max_length = 50)
    lastname = serializers.CharField(min_length = 2, max_length = 50)
    password = serializers.CharField(min_length = 8, max_length = 70, write_only = True)
    pfp = serializers.ImageField(required = False)
    phone = serializers.CharField(min_length = 11, max_length=11)

    class Meta:
        model = User
        fields = ["id","email","firstname","lastname","password","pfp","phone"]

    def validate(self, attrs):
       email = attrs.get("email").lower()
       attrs['email'] = email
       phone = attrs.get("phone")
       email_exists = User.objects.filter(email = email).exists()
       phone_exists = User.objects.filter(phone = phone).exists()

       if email_exists : 
           raise serializers.ValidationError("Email already exists")
       if phone_exists :
           raise serializers.ValidationError("Phone number already exists")
       return attrs
    
class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    password = serializers.CharField(min_length = 8, max_length = 70, write_only = True)

    class Meta:
        model = User
        fields = ["email","password","id","tokens"]

    def validate(self, attrs):
       email = attrs.get("email","").lower()
       attrs["email"] = email
       password = attrs.get("password","")
       valid_user = User.objects.filter(email = email).first()
       if not valid_user:
           raise AuthenticationFailed("invalid credentials,try again")
       if not valid_user.is_active:
           raise AuthenticationFailed("account suspended, contact admin")
       user = auth.authenticate(email = email, password = password)
       if not user:
           raise AuthenticationFailed("invalid credentials")
       
       return{
           "id":user.id,
           "email": user.email,
           "tokens":user.tokens()
       }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","firstname","lastname","pfp","email"]