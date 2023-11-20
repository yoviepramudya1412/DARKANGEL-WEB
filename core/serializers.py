

from rest_framework import serializers
from .models import CustomUser, Pengolahan, Absensi

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'nip','profil', 'nama', 'umur', 'golongan', 'is_active', 'is_staff', 'is_superuser')

class PengolahanSerializer(serializers.ModelSerializer):
    staff = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Pengolahan
        fields = ('id', 'staff', 'sampel_1', 'sampel_2', 'profil')
        
class AbsensiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Absensi
        fields = ['id', 'staff', 'pengolahan', 'tanggal_absensi', 'status_absensi', 'berapa_kali_absensi']

    def to_representation(self, instance):
        representation = super(AbsensiSerializer, self).to_representation(instance)
        representation['staff'] = instance.staff.nama  # Ubah 'nama' sesuai dengan atribut yang sesuai
    
        return representation