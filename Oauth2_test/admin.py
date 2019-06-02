from django.contrib import admin
from Oauth2_test.models.models import Camera, Drone


@admin.register(Camera)
class AuthorCamera(admin.ModelAdmin):
    pass


@admin.register(Drone)
class AuthorDrone(admin.ModelAdmin):
    pass
