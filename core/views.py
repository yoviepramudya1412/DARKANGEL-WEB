from django.shortcuts import render
from rest_framework import generics
from .models import Dosen, Pengolahan, Absensi
from .serializers import DosenSerializer, PengolahanSerializer, AbsensiSerializer

class DosenListCreateView(generics.ListCreateAPIView):
    queryset = Dosen.objects.all()
    serializer_class = DosenSerializer

class PengolahanListCreateView(generics.ListCreateAPIView):
    queryset = Pengolahan.objects.all()
    serializer_class = PengolahanSerializer

class AbsensiListCreateView(generics.ListCreateAPIView):
    queryset = Absensi.objects.all()
    serializer_class = AbsensiSerializer


# Create your views here.
def test(request):
    return render(request, 'pengguna/test.html')