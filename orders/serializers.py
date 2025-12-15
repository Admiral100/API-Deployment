from rest_framework import serializers
from Products.models import Product
from orders.models import Order, OrderProduct

class ProductSaleSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    quantity = serializers.IntegerField()
    def validate_quantity(self, obj):
        if obj < 1:
            raise serializers.ValidationError("Quantity can not be less than 1")
        return obj

class OrderProductSerializer(serializers.ModelSerializer):
    buyer = serializers.SerializerMethodField()
    class Meta:
        model = OrderProduct
        fields = ["id", "buyer", "quantity", "amount","created_at"]
    def get_buyer(self, obj):
        buyer = obj.order.buyer
        return {
            "id": buyer.id,
            "name": f'{buyer.firstname} {buyer.lastname}'
        }



class OrderSerializer(serializers.ModelSerializer):
    products = ProductSaleSerializer(write_only = True, many=True)
    order_products = serializers.SerializerMethodField()
    buyer = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id","buyer","order_total","created_at","products", "order_products"]
        read_only_fields = ["id","buyer","order_total", "order_products"]
    def get_order_products(self, obj):
        products = obj.order_OrderProduct.all()
        return [
            {
                "id": prod.product.id,
                "name": prod.product.name,
                "quantity": prod.quantity,
                "amount": prod.amount

            } for prod in products
        ]
    def get_buyer(self, obj):
        return {
            "id": obj.buyer.id,
            "name": f'{obj.buyer.firstname} {obj.buyer.lastname}'
        }
