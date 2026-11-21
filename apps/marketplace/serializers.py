# apps/marketplace/serializers.py
from rest_framework import serializers
from .models import Seller, Show, Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'position']


class SellerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    rep = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ['id', 'username', 'shop_name', 'shop_bio', 'shop_banner',
                  'shop_avatar', 'is_verified', 'total_sales', 'rep', 'created_at']
        read_only_fields = ['id', 'is_verified', 'total_sales', 'rep', 'created_at']

    def get_rep(self, obj):
        rep = getattr(obj.user, 'reputation', None)
        return rep.score if rep else 0


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    seller_name = serializers.CharField(source='seller.shop_name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'seller', 'seller_name', 'title', 'description', 'category',
                  'condition', 'starting_price', 'buy_now_price', 'quantity',
                  'status', 'images', 'created_at']
        read_only_fields = ['id', 'seller', 'created_at']

    def create(self, validated_data):
        request = self.context['request']
        seller = request.user.seller
        product = Product.objects.create(seller=seller, **validated_data)
        # Handle uploaded images from request.FILES
        for i, f in enumerate(request.FILES.getlist('images')):
            ProductImage.objects.create(product=product, image=f, position=i)
        return product


class ShowSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.shop_name', read_only=True)

    class Meta:
        model = Show
        fields = ['id', 'seller', 'seller_name', 'title', 'description', 'cover_image',
                  'scheduled_at', 'started_at', 'ended_at', 'status', 'playback_url', 'created_at']
        read_only_fields = ['id', 'seller', 'started_at', 'ended_at', 'status',
                            'playback_url', 'created_at']

    def create(self, validated_data):
        return Show.objects.create(seller=self.context['request'].user.seller, **validated_data)