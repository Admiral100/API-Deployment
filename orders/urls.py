from django.urls import path
from .views import OrderViews

urlpatterns = [
 path('',OrderViews.as_view()),
]