# apps/accounts/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    rep = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','username','email','display_name','bio','avatar','is_seller','rep','created_at']
        read_only_fields = ['id','rep','created_at','is_seller']
    def get_rep(self, obj):
        return getattr(getattr(obj, 'reputation', None), 'score', 0)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ['username','email','password','display_name']
    def create(self, data):
        return User.objects.create_user(**data)