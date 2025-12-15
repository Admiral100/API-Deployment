from rest_framework import serializers
from Products.models import Product

class ProductSerializers(serializers.ModelSerializer):
    name = serializers.CharField(max_length=250)
    description = serializers.CharField(required = False)
    price = serializers.IntegerField()
    picture = serializers.ImageField( required = False)
    quantity = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ["id", "name", "description","price","picture","quantity", "created_at","updated_at"]
        read_only_fields = ["id","created_at","updated_at"]

    def validate_price(self, obj):
        if obj < 1:
            raise serializers.ValidationError("price cannot be a negative number")
        return obj
    def validate_quantity(self,obj):
        if obj < 1:
            raise serializers.ValidationError("quantity cannot be a negative number")
        return obj
    
