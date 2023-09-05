from rest_framework import serializers
from decimal import Decimal
from .models import MenuItem, Category, Cart, Order, OrderItem
from rest_framework.validators import UniqueTogetherValidator
import bleach
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemInventory(serializers.ModelSerializer):
    disc_price = serializers.SerializerMethodField(method_name='discount')
    Category = CategorySerializer(read_only=True)
    Category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price','disc_price', 'Category', 'Category_id']
        extra_kwargs = {
            'sotk' : {'source': 'inventory', 'min_value' : 0},
            'price' : {'min_value' : 0.5},
        }
        # unique value
        """ validators = [
            UniqueTogetherValidator(
                queryset=MenuItem.objects.all(),
                fields=['title']
            )
        ] """
        # sanitize data it can be used for rules
        def validate(self, attrs):
            attrs['title'] = bleach.clean(attrs['title'])

            # if attrs['price'] < 1:
            # .....
            
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance
    def discount(self, product:MenuItem):
        return product.price * Decimal(0.5)
    
class UserGroupSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CartSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(read_only=True)
    # user = serializers.IntegerField(read_only=True)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)   
    class Meta:
        model = Cart
        fields = [
            'user', 'menuitem', 'quantity', 'unit_price', 'price'
        ]
    
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'order', 'menuitem', 'quantity', 'unit_price', 'price'
        ]

class OrderSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    class Meta:
        model = Order
        fields = ['id','user', 'delivery_crew', 'status', 'total', 'date']