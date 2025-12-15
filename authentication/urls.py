from django.urls import path
from authentication.views import (SignupView, loginView,UserView)
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
     path('signup/',SignupView.as_view()),
     path('login/',loginView.as_view()),
     path('refresh_token/',TokenRefreshView.as_view()),
     path('users/',UserView.as_view()),

]