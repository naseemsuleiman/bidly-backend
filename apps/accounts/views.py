# apps/accounts/views.py
from rest_framework import generics, permissions
from .serializers import UserSerializer, RegisterSerializer
from django.http import JsonResponse
from django.db import connection

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self): return self.request.user

def health(request):
    try:
        with connection.cursor() as c:
            c.execute("SELECT 1")
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'fail', 'error': str(e)}, status=503)