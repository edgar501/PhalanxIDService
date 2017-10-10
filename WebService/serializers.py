from rest_framework import serializers
from .models import PhalanxIDDataModel


class PhalanxIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhalanxIDDataModel
        exclude = ('id',)
