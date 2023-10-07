from rest_framework import serializers
from .models import Dosen, Pengolahan, Absensi

class DosenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dosen
        fields = '__all__'

class PengolahanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pengolahan
        fields = '__all__'

class AbsensiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Absensi
        fields = '__all__'
