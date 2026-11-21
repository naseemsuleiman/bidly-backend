# apps/reputation/urls.py
from django.urls import path
from .views import UserRepView

urlpatterns = [path('<str:username>/', UserRepView.as_view())]