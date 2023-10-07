from django.urls import path
from . import views

urlpatterns = [
    path('',views.test,name='test'),
    path('api/dosen/', views.DosenListCreateView.as_view(), name='dosen-list-create'),
    path('api/pengolahan/', views.PengolahanListCreateView.as_view(), name='pengolahan-list-create'),
    path('api/absensi/',views.AbsensiListCreateView.as_view(), name='absensi-list-create'),
    
]
