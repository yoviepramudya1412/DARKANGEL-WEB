from django.forms import ImageField
from django.shortcuts import render,  redirect 

from django.contrib import messages

from rest_framework import generics
from django.conf import settings

import sys, os
sys.path.insert(1, "api-fs")
# print("------CURRENT DIR:", os.getcwd())

from deepface import DeepFace
from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from .models import Absensi, CustomUser,Pengolahan
from .serializers import CustomUserSerializer,PengolahanSerializer,AbsensiSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.files.base import ContentFile
from django.utils import timezone
from django.core.files import File
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
import numpy as np
import cv2
import io

from PIL import Image
import numpy as np
import cv2
from mtcnn.mtcnn import MTCNN

from django.core.files.images import ImageFile
from PIL import Image


from PIL import Image
from io import BytesIO
from django.http import JsonResponse
import base64
from django.views.decorators.csrf import csrf_protect
from django.db.models import Count, Avg
from django.contrib.auth import authenticate, login
from django.db.models import Q

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
        # Memeriksa apakah sampel_2 ada atau tidak
        if not pengolahan_instance.sampel_2:
            continue 
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


    # Menghitung hasil voting
    print(f"isi voting = {verified_list}")
    overall_verified = sum(verified_list) > len(verified_list) / 2
    print(f"Hasil_final = {overall_verified}")
    # Logika penyimpanan ke dalam model Absensi
    current_time = timezone.now()
    deadline_time = current_time.replace(hour=8, minute=30, second=0, microsecond=0)

    if overall_verified:
        absensi_entry = Absensi.objects.create(
            staff=request.user,
            pengolahan=pengolahan_instance,
            status_absensi='sudah absen',
            berapa_kali_absensi=2  # Sesuaikan sesuai kebutuhan
        )
        absensi_entry.save()
        new_pengolahan = Pengolahan.objects.create(
                staff=request.user,
                sampel_1=uploaded_image  # Menyimpan gambar dari temporary_image_path
            )

            # Simpan objek Pengolahan baru
        new_pengolahan.save()
    temporary_image_path.unlink()
                
    # Logika penyimpanan ke dalam model Absensi
    # if overall_verified:
    #     total_savings = Absensi.objects.filter(staff=request.user).count()
    #     if total_savings < 2:
    #         if current_time > deadline_time:
    #             status_absensi = 'belum absen'
    #         else:
    #             status_absensi = 'sudah absen'
            # with open(temporary_image_path, 'rb') as file:
            #     file_obj = File(file)
            #     # Menyimpan gambar ke model Pengolahan jika overall_verified adalah True
            #     pengolahan_instance.sampel_1.save(uploaded_image.name, file_obj, save=True)
    #         absensi_entry = Absensi.objects.create(
    #             staff=request.user,
    #             pengolahan=pengolahan_instance,
    #             status_absensi=status_absensi,
    #             berapa_kali_absensi=2  # Sesuaikan sesuai kebutuhan
    #         )
    #         absensi_entry.save()
    # pengolahan_instance.sampel_1 = temporary_image_path
    # pengolahan_instance.save()

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




# Percobaan render 
def test(request):
    return render(request, 'pengguna/test.html')
def landingpage(request):
    return render(request, 'landingpage/index.html')





def user_login(request):
    if request.method == 'POST':
        nip = request.POST.get('nip')
        password = request.POST.get('lpassword')

        # Authenticate user
        user = authenticate(request, nip=nip, password=password)

        if user is not None:
            # User authenticated, log them in
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('dashboard')  # Ganti 'home' dengan nama URL tujuan setelah login
        else:
            # User authentication failed
            messages.error(request, 'Invalid NIP or password.')
            return redirect('masuk')

    return render(request, 'landingpage/log-in.html')

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('masuk')


@login_required(login_url=settings.LOGIN_URL)
def dashboard(request):
    user_profil_url = None
    user_nama = None

    if request.user.is_authenticated:
        user_profil_url = request.user.profil.url if request.user.profil else None
        user_nama = request.user.nama
    context= {  'user_profil_url': user_profil_url,
                'user_nama': user_nama,
                
                }
    return render(request, 'pengguna/dashboard.html', context)


def cek_nip(request):
    if request.method == 'GET':
        cek_nip = request.GET.get('cekNIP')

        try:
            user = get_user_model().objects.get(nip=cek_nip)
            response_data = {
                'found': True,
                'nama': user.nama,
                'nip': user.nip,
            }
        except get_user_model().DoesNotExist:
            response_data = {
                'found': False,
            }

        return JsonResponse(response_data)

    return render(request, 'pengguna/form/form.html')


@login_required(login_url=settings.LOGIN_URL)
def form_pengguna(request):
    
    user_profil_url = None
    user_nama = None

    if request.user.is_authenticated:
        user_profil_url = request.user.profil.url if request.user.profil else None
        user_nama = request.user.nama
    context= {  'user_profil_url': user_profil_url,
                'user_nama': user_nama,
                
                }
    return render(request, 'pengguna/form/form.html',context)




@login_required(login_url=settings.LOGIN_URL)
def tambahfoto(request):
    if request.method == 'POST':
        staff_nama = request.POST.get('nama')
        sampel_files = request.FILES.getlist('sampel')  
        print(f'staff_nama: {staff_nama}')
        staff = get_object_or_404(CustomUser, nama__iexact=staff_nama)

        try:
            for sampel_file in sampel_files:
                # Simpan gambar sementara di server
                temporary_image_path = f'temp/temporary_image_{sampel_file.name}.jpg'
                with open(temporary_image_path, 'wb+') as destination:
                    for chunk in sampel_file.chunks():
                        destination.write(chunk)

                # Deteksi wajah menggunakan MTCNN
                image = cv2.imread(temporary_image_path)
                detector = MTCNN()
                results = detector.detect_faces(image)

                if results:
                    # Ambil koordinat wajah pertama yang terdeteksi
                    x, y, w, h = results[0]['box']

                    # Crop wajah dari gambar
                    face_cropped = image[y:y+h, x:x+w]

                    # Simpan gambar wajah yang sudah di-crop ke dalam objek Pengolahan
                    image_array = Image.fromarray(cv2.cvtColor(face_cropped, cv2.COLOR_BGR2RGB))
                    face_cropped_path = f'temp/face_cropped_{sampel_file.name}.jpg'
                    image_array.save(face_cropped_path)

                    pengolahan_obj = Pengolahan(staff=staff)
                    pengolahan_obj.sampel_2.save(f'face_cropped_{sampel_file.name}.jpg', ImageFile(open(face_cropped_path, 'rb')))
                    
                    # Hapus gambar sementara di server
                    os.remove(temporary_image_path)
                    os.remove(face_cropped_path)

                    messages.success(request, 'Foto berhasil ditambahkan!')
                else:
                    messages.warning(request, f'Wajah tidak ditemukan pada gambar {sampel_file.name}.')
                    return redirect('tabel_1')

            return redirect('form')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')

    # Handle request method selain POST
    return render(request, 'pengguna/form/form.html')



@login_required(login_url=settings.LOGIN_URL)
def tabel_sampel(request):
    user_profil_url = None
    user_nama = None

    if request.user.is_authenticated:
        user_profil_url = request.user.profil.url if request.user.profil else None
        user_nama = request.user.nama

        # Ambil data Pengolahan berdasarkan staff (user yang sedang login)
        # Filter baris dengan sampel_2 yang tidak null atau kosong
        pengolahan_data = Pengolahan.objects.filter(Q(sampel_2=None) and ~Q(sampel_2=''))
        
        context = {
            'user_profil_url': user_profil_url,
            'user_nama': user_nama,
            'pengolahan_data': pengolahan_data,  # Tambahkan data Pengolahan ke dalam konteks
        }

        return render(request, 'pengguna/tabel/sampel_1.html', context)

    # Handle request method selain POST
    return render(request, 'pengguna/tabel/sampel_1.html')

@login_required(login_url=settings.LOGIN_URL)
def delete_pengolahan(request, pengolahan_id):
    pengolahan = get_object_or_404(Pengolahan, id=pengolahan_id)

    # Pastikan hanya staf yang memiliki hak akses untuk menghapus data Pengolahan
    if request.user == pengolahan.staff:
        # Hapus file gambar terkait sebelum menghapus objek Pengolahan
        if pengolahan.sampel_1:
            pengolahan.sampel_1.delete()
        if pengolahan.sampel_2:
            pengolahan.sampel_2.delete()
        

        # Hapus objek Pengolahan
        pengolahan.delete()

        messages.success(request, 'Data Pengolahan berhasil dihapus.')
    else:
        messages.error(request, 'Anda tidak memiliki izin untuk menghapus data ini.')

    return redirect('tabel_1')

def tabel_sampel_2(request):
    return render(request, 'pengguna/tabel/sampel_2.html')