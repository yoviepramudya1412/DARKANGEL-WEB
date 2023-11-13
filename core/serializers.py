

from rest_framework import serializers
from .models import CustomUser, Pengolahan

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'nip', 'nama', 'umur', 'golongan', 'is_active', 'is_staff', 'is_superuser')

class PengolahanSerializer(serializers.ModelSerializer):
    staff = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Pengolahan
        fields = ('id', 'staff', 'sampel_1', 'sampel_2', 'profil')