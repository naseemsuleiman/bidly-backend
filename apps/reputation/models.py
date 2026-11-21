# apps/reputation/models.py
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

class UserReputation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reputation')
    score = models.IntegerField(default=0, db_index=True)
    buyer_score = models.IntegerField(default=0)
    seller_score = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def tier(self):
        if self.score >= 1000: return 'elite'
        if self.score >= 250:  return 'trusted'
        if self.score >= 50:   return 'contributor'
        return 'newcomer'

class RepEvent(models.Model):
    EVENT_TYPES = [
        ('SIGNUP_BONUS', 'Signup bonus'),
        ('UPVOTE_RECEIVED', 'Upvote received'),
        ('DOWNVOTE_RECEIVED', 'Downvote received'),
        ('PURCHASE_COMPLETED', 'Purchase completed'),
        ('SALE_COMPLETED', 'Sale completed'),
        ('POSITIVE_REVIEW', 'Positive review'),
        ('NEGATIVE_REVIEW', 'Negative review'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rep_events')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    points_change = models.IntegerField()
    source_content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    source_object_id = models.PositiveIntegerField(null=True, blank=True)
    source = GenericForeignKey('source_content_type', 'source_object_id')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta: ordering = ['-created_at']