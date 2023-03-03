from rest_framework.serializers import ModelSerializer
from .models import *

class SwanSerializer(ModelSerializer):
    class Meta:
        model = Swan
        fields = '__all__'

class DetectorSerializer(ModelSerializer):
    class Meta:
        model = Detector
        fields = '__all__'