from django import forms
from django.contrib import admin

from .models import *

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Pengolahan

class PengolahanForm(forms.ModelForm):
    class Meta:
        model = Pengolahan
        fields = '__all__'

class CustomImageForm(forms.ModelForm):
    class Meta:
        model = Pengolahan
        fields = ['sampel_1','sampel_2']

class PengolahanAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff','sampel_1', 'sampel_2')
    search_fields = ('staff__nama',)  # Mencari berdasarkan nama staff
    form = PengolahanForm

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            kwargs['form'] = CustomImageForm
        return super(PengolahanAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(Pengolahan, PengolahanAdmin)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['nip', 'profil', 'nama', 'umur', 'golongan', 'is_active', 'is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('nip', 'nama', 'profil', 'umur', 'golongan')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Password', {'fields': ('password',)}),  # Menambahkan bagian untuk mengelola password
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nip', 'nama', 'profil', 'umur', 'golongan', 'is_active', 'is_staff', 'is_superuser', 'password1', 'password2'),
        }),
    )
    search_fields = ['nip', 'nama']
    ordering = ['nama']

admin.site.register(CustomUser, CustomUserAdmin)

class AbsensiAdmin(admin.ModelAdmin):
    list_display = ('staff', 'pengolahan', 'tanggal_absensi', 'status_absensi', 'berapa_kali_absensi')
    search_fields = ('staff__username', 'pengolahan__nama')  # Menambahkan kolom pencarian

admin.site.register(Absensi, AbsensiAdmin)





