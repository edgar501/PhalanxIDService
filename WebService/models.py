from django.db import models
from django.core import validators


class PhalanxIDDataModel(models.Model):
    phalanx_id = models.CharField(max_length=16, unique=True)
    phalanx_uid = models.CharField(max_length=64, unique=True)
    uart_test = models.BooleanField(default=False)
    gpio_test = models.BooleanField(default=False)
    radio_test = models.BooleanField(default=False)
    phalanx_ok = models.BooleanField(default=False)
    sender_rssi = models.CharField(max_length=100, blank=True, null=True)
    receiver_rssi = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.CharField(max_length=100, blank=True, null=True)
    firmware_name = models.CharField(max_length=100, blank=True, null=True)
    firmware_version = models.CharField(max_length=100, blank=True, null=True)
