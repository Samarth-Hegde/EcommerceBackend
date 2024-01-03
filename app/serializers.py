from rest_framework import serializers
from .models import Address, Product, Cart, CartItem, Review, Like, DisLike
# from users.serializers import UserProfileSerializer

class AddressSerializer(serializers.ModelSerializer):
    # user = UserProfileSerializer()

    class Meta:
        model = Address
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    image = serializers.ImageField()

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.cost = validated_data.get('cost', instance.cost)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class DisLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisLike
        fields = '__all__'
