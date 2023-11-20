from django.urls import path
from . import views
from .views import StaffDetail

urlpatterns = [
    path('', views.test, name='test'),
    path('api/login/', views.api_login, name='staff-login'),
    
    path('halo/', views.face_recognition_api, name='face_recognition_api'),
    path('absensi/', views.absensi_api, name='absensi_api'),
    path('absensibelum/', views.absensi_belum_api, name='absensi_belum_api'),
    

    # Endpoint yang dilindungi oleh otorisasi token
    path('api/staff/', views.staff_api, name='staff-list'),
    path('api/staff/<uuid:pk>/', StaffDetail.as_view(), name='staff_detail'),
    
]
