# apps/reputation/services.py
from django.db import transaction
from .models import UserReputation, RepEvent

POINTS = {
    'SIGNUP_BONUS': 5,
    'UPVOTE_RECEIVED': 1,
    'DOWNVOTE_RECEIVED': -1,
    'PURCHASE_COMPLETED': 5,
    'SALE_COMPLETED': 10,
    'POSITIVE_REVIEW': 15,
    'NEGATIVE_REVIEW': -20,
}

@transaction.atomic
def award_rep(user, event_type, source=None, points=None):
    """The ONLY way to change Rep. Every app calls this."""
    if points is None:
        points = POINTS.get(event_type, 0)
    if points == 0:
        return None
    rep, _ = UserReputation.objects.select_for_update().get_or_create(user=user)
    rep.score += points
    if event_type == 'SALE_COMPLETED':      rep.seller_score += points
    if event_type == 'PURCHASE_COMPLETED':  rep.buyer_score += points
    rep.save()
    return RepEvent.objects.create(user=user, event_type=event_type, points_change=points, source=source)