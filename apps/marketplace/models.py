# apps/marketplace/models.py
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class Seller(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller')
    shop_name = models.CharField(max_length=60, unique=True)
    shop_bio = models.TextField(max_length=500, blank=True)
    shop_banner = models.ImageField(upload_to='shop_banners/', null=True, blank=True)
    shop_avatar = models.ImageField(upload_to='shop_avatars/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    stripe_account_id = models.CharField(max_length=255, blank=True)   # Stripe Connect (Phase 7)
    total_sales = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_name


class Show(models.Model):
    STATUS = [
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('ended', 'Ended'),
        ('cancelled', 'Cancelled'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='shows')
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='show_covers/', null=True, blank=True)
    scheduled_at = models.DateTimeField(default=timezone.now)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='scheduled', db_index=True)

    # Streaming — populated in Phase 4
    stream_key = models.CharField(max_length=100, blank=True)
    playback_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scheduled_at']
        indexes = [models.Index(fields=['status', '-scheduled_at'])]

    def __str__(self):
        return f"{self.seller.shop_name} — {self.title}"


class Product(models.Model):
    CONDITION = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('used', 'Used'),
        ('vintage', 'Vintage'),
    ]
    STATUS = [
        ('draft', 'Draft'),
        ('listed', 'Listed'),
        ('sold', 'Sold'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=60, blank=True, db_index=True)
    condition = models.CharField(max_length=20, choices=CONDITION, default='new')
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_now_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS, default='draft', db_index=True)
    is_auction_ready = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['status', '-created_at'])]

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['position']