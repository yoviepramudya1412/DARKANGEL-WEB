from django.urls import path
from . import views
from .views import StaffDetail

urlpatterns = [
    path('test/', views.test, name='test'),
    path('', views.landingpage, name='landingpage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('form/', views.form_pengguna, name='form'),
    path('tabel_1/', views.tabel_sampel, name='tabel_1'),
    path('tabel_2/', views.tabel_sampel_2, name='tabel_2'),
    path('masuk/', views.user_login, name='masuk'),
    path('keluar/', views.logout_view, name='keluar'),
    path('ceknip/', views.cek_nip, name='ceknip'),
    path('tambahfoto/', views.tambahfoto, name='tambahfoto'),
    path('delete_pengolahan/<int:pengolahan_id>/',views.delete_pengolahan, name='delete_pengolahan'),
    # batas suci
    
    path('api/login/', views.api_login, name='staff-login'),
    
    path('halo/', views.face_recognition_api, name='face_recognition_api'),
    path('absensi/', views.absensi_api, name='absensi_api'),
    path('absensibelum/', views.absensi_belum_api, name='absensi_belum_api'),
    

    # Endpoint yang dilindungi oleh otorisasi token
    path('api/staff/', views.staff_api, name='staff-list'),
    path('api/staff/<uuid:pk>/', StaffDetail.as_view(), name='staff_detail'),
    
]
