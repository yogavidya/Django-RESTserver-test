from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from rest_framework import generics, permissions, serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework import routers, viewsets
from django.contrib.auth.models import Permission
from typing import Any
from Oauth2_test.models.models import Camera, Drone
from functools import reduce

valid_groups = {
    'Pix4D Employees': 'read',
    'Pix4D Support': 'write',
}


def has_permission(request, action, model):
    user_permissions = list(
        filter(
            lambda p: 'Oauth2_test.'+action+'_'+model in p,
            request.user.get_all_permissions()))
    group_permissions = list(
        filter(
            lambda p: 'Oauth2_test.'+action+'_'+model in p,
            request.user.get_group_permissions()))
    return len(user_permissions) > 0 \
           or len(group_permissions) > 0 \
           or request.user.is_superuser


def protected_create(self, request: Request, *args, **kwargs):
    if not has_permission(request, 'create', self.basename):
        return HttpResponseForbidden()
    else:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except BaseException as e:
            return Response(data=str(e),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)


def protected_update(self, request, *args, **kwargs):
    if not has_permission(request, 'change', self.basename):
        return HttpResponseForbidden()
    else:
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
        except BaseException as e:
            return Response(data=str(e),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)


def protected_partial_update(self, request, *args, **kwargs):
    kwargs['partial'] = True
    return self.update(request, *args, **kwargs)


def protected_destroy(self, request, *args, **kwargs):
    if not has_permission(request, 'delete', self.basename):
        return HttpResponseForbidden()
    else:
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except BaseException as e:
            return Response(data=str(e),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


def build_order_by(self):
    sort_records = self.request.query_params.get('sort', None)
    if sort_records is not None:
        sort_records = sort_records.split(',')[0]  # ignore extra
        sort_records_desc = self.request.query_params.get('desc', None)
        if sort_records_desc is not None:
            sort_records = '-' + sort_records
    return sort_records


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ('id', 'camera_model', 'sensor_mp', 'brand')


class CameraViewSet(viewsets.ModelViewSet):
    basename = 'cameras'
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['read', 'write']
    create = protected_create
    update = protected_update
    partial_update = protected_partial_update
    destroy = protected_destroy

    def get_queryset(self):
        queryset = Camera.objects.all()
        camera_model = self.request.query_params.get('camera_model', None)
        brand = self.request.query_params.get('brand', None)
        sensor_mp = self.request.query_params.get('sensor_mp', None)
        sort_records = build_order_by(self)
        if camera_model is not None:
            queryset = queryset.filter(camera_model__icontains=camera_model)
        if brand is not None:
            queryset = queryset.filter(brand__icontains=brand)
        if sensor_mp is not None:
            queryset = queryset.filter(sensor_mp=sensor_mp)
        if sort_records is not None:
            queryset = queryset.order_by(sort_records)
        return queryset


class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ('id', 'name', 'brand', 'serial_number', 'cameras')


class DroneViewSet(viewsets.ModelViewSet):
    basename = 'drones'
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['read', 'write']
    create = protected_create
    update = protected_update
    partial_update = protected_partial_update
    destroy = protected_destroy

    def get_queryset(self):
        queryset = Drone.objects.all()
        name = self.request.query_params.get('name', None)
        brand = self.request.query_params.get('brand', None)
        serial_number = self.request.query_params.get('serial_number', None)
        cameras_brand = self.request.query_params.get('cameras_brand', None)
        cameras_model = self.request.query_params.get('cameras_model', None)
        cameras_sensor_mp = self.request.query_params.get('cameras_sensor_mp', None)
        sort_records = build_order_by(self)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        if brand is not None:
            queryset = queryset.filter(brand__icontains=brand)
        if serial_number is not None:
            queryset = \
                queryset.filter(serial_number__icontains=serial_number)
        if cameras_brand is not None:
            queryset = queryset.filter(cameras__brand__icontains=cameras_brand)
        if cameras_model is not None:
            queryset = \
                queryset.filter(cameras__camera_model__icontains=cameras_model)
        if cameras_sensor_mp is not None:
            queryset = \
                queryset.filter(cameras__sensor_mp__exact=cameras_sensor_mp)
        if sort_records is not None:
            queryset = queryset.order_by(sort_records)
        return queryset


api_router = routers.SimpleRouter()
api_router.register('cameras', CameraViewSet)
api_router.register('drones', DroneViewSet)
api_urlpatterns = api_router.urls
