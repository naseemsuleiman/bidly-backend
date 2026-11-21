# apps/marketplace/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Seller, Show, Product
from .serializers import SellerSerializer, ShowSerializer, ProductSerializer


class IsSellerOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return hasattr(request.user, 'seller') and obj.seller == request.user.seller


class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    lookup_field = 'shop_name'

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        seller = serializer.save(user=self.request.user)
        # Flip the flag so the UI can show seller tools
        self.request.user.is_seller = True
        self.request.user.save(update_fields=['is_seller'])


class ShowViewSet(viewsets.ModelViewSet):
    queryset = Show.objects.select_related('seller').all()
    serializer_class = ShowSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsSellerOwner()]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.seller)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def live(self, request):
        qs = Show.objects.filter(status='live').select_related('seller')
        return Response(ShowSerializer(qs, many=True, context={'request': request}).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsSellerOwner])
    def go_live(self, request, pk=None):
        show = self.get_object()
        show.status = 'live'
        from django.utils import timezone
        show.started_at = timezone.now()
        show.save(update_fields=['status', 'started_at'])
        return Response(ShowSerializer(show).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsSellerOwner])
    def end(self, request, pk=None):
        from django.utils import timezone
        show = self.get_object()
        show.status = 'ended'
        show.ended_at = timezone.now()
        show.save(update_fields=['status', 'ended_at'])
        return Response(ShowSerializer(show).data)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('seller').prefetch_related('images')

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsSellerOwner()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list' and 'mine' not in self.request.query_params:
            qs = qs.filter(status='listed')
        if cat := self.request.query_params.get('category'):
            qs = qs.filter(category=cat)
        if q := self.request.query_params.get('q'):
            qs = qs.filter(title__icontains=q)
        return qs

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.seller)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def mine(self, request):
        if not hasattr(request.user, 'seller'):
            return Response([])
        qs = Product.objects.filter(seller=request.user.seller).prefetch_related('images')
        return Response(self.get_serializer(qs, many=True).data)