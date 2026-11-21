# apps/reputation/views.py
from rest_framework import generics, permissions, serializers
from .models import UserReputation

class RepSerializer(serializers.ModelSerializer):
    tier = serializers.CharField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = UserReputation
        fields = ['username','score','buyer_score','seller_score','tier','updated_at']

class UserRepView(generics.RetrieveAPIView):
    serializer_class = RepSerializer
    permission_classes = [permissions.AllowAny]
    def get_object(self):
        return UserReputation.objects.get(user__username=self.kwargs['username'])