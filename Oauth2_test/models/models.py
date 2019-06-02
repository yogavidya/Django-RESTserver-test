from django.db import models

class Camera(models.Model):
    camera_model = models.CharField(max_length=256, blank=False)
    sensor_mp = models.IntegerField(blank=False)
    brand = models.CharField(max_length=256, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['camera_model', 'brand'], name='unique_camera')
        ]
        ordering = ('brand', 'camera_model')
        app_label = 'Oauth2_test'

    def __str__(self):
        return '{} {}'.format(self.brand, self.camera_model)


class Drone(models.Model):
    name = models.CharField(max_length=256, blank=False)
    brand = models.CharField(max_length=256, blank=False)
    serial_number = models.CharField(max_length=256, blank=False)
    cameras = models.ManyToManyField('Camera', blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'brand', 'serial_number'],
                                    name='unique_drone')
        ]
        ordering = ('brand', 'name', 'serial_number')
        app_label = 'Oauth2_test'

    def __str__(self):
        return '{} {} [{}]'.format(self.brand, self.name, self.serial_number)
