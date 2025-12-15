from django.urls import path
from Products.views import ProductViews,SingleProductView,UserProductsView, ProductSalesView

urlpatterns = [
    path('',ProductViews.as_view()),
    path('user/<str:user_id>/',UserProductsView.as_view()),
    path('orders/<str:id>/', ProductSalesView.as_view()),
    path('<str:id>/', SingleProductView.as_view())
]