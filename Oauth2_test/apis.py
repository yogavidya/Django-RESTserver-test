from django.http import HttpRequest, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import generics, permissions, serializers
from oauth2_provider.contrib.rest_framework import TokenHasScope
import json

valid_groups = {
    'Pix4D Employees': 'read',
    'Pix4D Support': 'write',
}


def get_group_permissions(request: HttpRequest):
    groups = [g.name for g in request.user.groups.all()]
    group_permissions = [valid_groups[g] for g in filter(lambda g: g in valid_groups, groups)]
    return group_permissions


def can_modify(request):
    group_permissions = get_group_permissions(request)
    return 'write' in group_permissions


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class UserListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    required_scopes = ['read', 'write']

    def post(self, request: HttpRequest):
        if not can_modify(request):
            return HttpResponseForbidden()
        else:
            return self.create(request)


class UserDestroy(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    required_scopes = ['read', 'write']

    def delete(self, request: HttpRequest, pk=-1):
        if not can_modify(request):
            return HttpResponseForbidden()
        else:
            return self.destroy(request, pk)
