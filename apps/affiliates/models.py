# apps/affiliates/models.py
import uuid
from django.conf import settings
from django.db import models

class Affiliate(models.Model):
    STATUS = [('pending','Pending'),('active','Active'),('suspended','Suspended')]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='affiliate')
    referral_code = models.CharField(max_length=20, unique=True, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    first_purchase_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    recurring_rate = models.DecimalField(max_digits=5, decimal_places=2, default=4.00)
    payout_method = models.CharField(max_length=50, blank=True)
    payout_details = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

class ReferralClick(models.Model):
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE, related_name='clicks')
    visitor_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    landing_url = models.URLField(max_length=1000)
    referrer_url = models.URLField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)