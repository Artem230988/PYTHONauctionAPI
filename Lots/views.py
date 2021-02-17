from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from .permissions import IsLotOwner
from .models import *
from .serializer import *
import datetime


class LotViewSet(viewsets.ModelViewSet):
    """CRUD для Лотов"""
    queryset = Lot.objects.filter(closed_date__gte=datetime.datetime.today())
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'create':
            return LotCreateSerializer
        elif self.action == 'partial_update':
            return LotUpdateSerializer
        return LotSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [permissions.AllowAny]
        elif self.action == 'retrieve' or 'create':
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.IsAdminUser, IsLotOwner]
        return super().get_permissions()


class UpdateRateView(generics.UpdateAPIView):
    http_method_names = ['patch', ]
    queryset = Lot.objects.all()
    serializer_class = UpdateRateSerializer
    permission_classes = [permissions.IsAuthenticated, ]
