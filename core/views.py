from django.shortcuts import render
from rest_framework import generics

import sys, os
sys.path.insert(1, "api-fs")
# print("------CURRENT DIR:", os.getcwd())

from deepface import DeepFace
from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Absensi, CustomUser,Pengolahan
from .serializers import CustomUserSerializer,PengolahanSerializer,AbsensiSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.files.base import ContentFile
from django.utils import timezone

import numpy as np
import cv2
import io



from PIL import Image
from io import BytesIO
from django.http import JsonResponse
import base64

from django.db.models import Count, Avg

import os
from pathlib import Path


from statistics import mean





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def face_recognition_api(request):
    print(request.data)

    if 'sampel_1' not in request.FILES:
        return Response({'error': 'Tidak ada file gambar yang diberikan'}, status=400)

    pengolahan_instances = get_list_or_404(Pengolahan, staff=request.user)

    uploaded_image = request.FILES['sampel_1']

    temporary_directory = 'temp'
    os.makedirs(temporary_directory, exist_ok=True)

    temporary_image_path = Path(temporary_directory) / uploaded_image.name
    with open(temporary_image_path, 'wb+') as destination:
        for chunk in uploaded_image.chunks():
            destination.write(chunk)

    verified_list = []

    for pengolahan_instance in pengolahan_instances:
        image_path = Path(pengolahan_instance.sampel_2.path)

        print(f"image_path: {image_path}")
        print(f"uploaded_image_name: {uploaded_image.name}")

        try:
            results = DeepFace.verify( img1_path=str(image_path),
                                        img2_path=str(temporary_image_path),
                                        model_name=["VGG-Face", "Facenet"],
                                        voting_method="based on threshold",
                                        distance_metric="cosine",
                                        enforce_detection=False)
            print(f"hasil_akhir{results}")

            # Menambahkan nilai 'verified' ke dalam daftar
            verified_list.append(results['verified'])

        except Exception as e:
            print(f"Error in deepface.verify: {str(e)}")
            return Response({'error': str(e)}, status=500)

    temporary_image_path.unlink()

    # Menghitung hasil voting
    print(f"isi voting = {verified_list}")
    overall_verified = sum(verified_list) > len(verified_list) / 2
    print(f"Hasil_final = {overall_verified}")
    # Logika penyimpanan ke dalam model Absensi
    current_time = timezone.now()
    deadline_time = current_time.replace(hour=8, minute=30, second=0, microsecond=0)

    # if overall_verified:
    #     absensi_entry = Absensi.objects.create(
    #         staff=request.user,
    #         pengolahan=pengolahan_instance,
    #         status_absensi='sudah absen',
    #         berapa_kali_absensi=2  # Sesuaikan sesuai kebutuhan
    #     )
    absensi_entry.save()
    # Logika penyimpanan ke dalam model Absensi
    if overall_verified:
        total_savings = Absensi.objects.filter(staff=request.user).count()
        if total_savings < 2:
            if current_time > deadline_time:
                status_absensi = 'belum absen'
            else:
                status_absensi = 'sudah absen'

            absensi_entry = Absensi.objects.create(
                staff=request.user,
                pengolahan=pengolahan_instance,
                status_absensi=status_absensi,
                berapa_kali_absensi=2  # Sesuaikan sesuai kebutuhan
            )
            absensi_entry.save()

    response_data = {
        'voting_results': {
            'verified': overall_verified,
            'count_true': sum(verified_list),
            'count_false': len(verified_list) - sum(verified_list),
            'total_votes': len(verified_list),
        },
    }
    return Response(response_data)


















@api_view(['GET'])
@permission_classes([IsAuthenticated])
def absensi_api(request):
    # Mengambil semua entri Absensi yang memiliki status 'sudah absen' untuk pengguna yang diautentikasi
    absensi_entries = Absensi.objects.filter(staff=request.user, status_absensi='sudah absen').order_by('-tanggal_absensi')

    # Menggunakan serializer untuk mengonversi objek Absensi ke dalam format JSON
    serializer = AbsensiSerializer(absensi_entries, many=True)

    # Mengembalikan respons JSON
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def absensi_belum_api(request):
    # Mengambil semua entri Absensi yang memiliki status 'sudah absen' untuk pengguna yang diautentikasi
    absensi_entries = Absensi.objects.filter(staff=request.user, status_absensi='belum absen').order_by('-tanggal_absensi')

    # Menggunakan serializer untuk mengonversi objek Absensi ke dalam format JSON
    serializer = AbsensiSerializer(absensi_entries, many=True)

    # Mengembalikan respons JSON
    return Response(serializer.data)








@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def api_login(request):
    if request.method == 'POST':
        nip = request.data.get('nip')
        password = request.data.get('password')

        try:
            user = CustomUser.objects.get(nip=nip)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid NIP or password'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            serializer = CustomUserSerializer(user)  # Serialisasi data pengguna
            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': serializer.data  # Menambahkan data pengguna ke respons
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid NIP or password'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes(['rest_framework_simplejwt.authentication.JWTAuthentication'])
@permission_classes(['rest_framework.permissions.IsAuthenticated'])
def staff_api(request):
    CustomUser = CustomUser.objects.all()
    serializer = CustomUserSerializer(CustomUser, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class StaffDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer




# Create your views here.
def test(request):
    return render(request, 'pengguna/test.html')