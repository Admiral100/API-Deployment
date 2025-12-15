from django.urls import path
from app1.views import Hiit,Hiit1,Hiit2

urlpatterns = [
    path('user/',Hiit.as_view()),
    path('lagos/',Hiit1.as_view()),
    path('hello/',Hiit2.as_view()),
]
