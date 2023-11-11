from django.shortcuts import render
from rest_framework import generics




from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser,Pengolahan
from .serializers import CustomUserSerializer,PengolahanSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from deepface import DeepFace
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.files.base import ContentFile

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


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def face_recognition_api(request):
    print(request.data)

    # Ensure the request has an image file
    if 'sampel_1' not in request.FILES:
        return Response({'error': 'Tidak ada file gambar yang diberikan'}, status=400)

    # Get all instances of 'Pengolahan' for the authenticated user
    pengolahan_instances = get_list_or_404(Pengolahan, staff=request.user)

    # Get the uploaded image
    uploaded_image = request.FILES['sampel_1']

    # Create a temporary directory if it does not exist
    temporary_directory = 'temp'
    os.makedirs(temporary_directory, exist_ok=True)

    # Save the temporary file to the file system
    temporary_image_path = Path(temporary_directory) / uploaded_image.name
    with open(temporary_image_path, 'wb+') as destination:
        for chunk in uploaded_image.chunks():
            destination.write(chunk)

    # Perform face detection and save the result
    



    # List to store verification results for each Pengolahan instance
    verified_list = []

    for pengolahan_instance in pengolahan_instances:
        image_path = Path(pengolahan_instance.sampel_2.path)

        print(f"image_path: {image_path}")
        print(f"uploaded_image_name: {uploaded_image.name}")

        try:
            # Perform face verification using deepface with the saved detection result
            result = DeepFace.verify(
                img1_path=str(image_path),
                img2_path=str(temporary_image_path),
                model_name="VGG-Face",
                distance_metric='cosine',
                enforce_detection=False,
                detector_backend='opencv',
                align=True,
                normalization='base',
            )

            # Extract relevant information from the result
            verified = result['verified']
            verified_list.append(verified)

        except Exception as e:
            print(f"Error in deepface.verify: {str(e)}")
            return Response({'error': str(e)}, status=500)

    # Remove the temporary file after use
    temporary_image_path.unlink()

    # Calculate the average of the verification results
    average_verified = sum(verified_list) / len(verified_list) if verified_list else 0.0

    # Determine the overall verification status
    overall_verified = average_verified >= 0.71  # Adjust the threshold as needed

    # Return the response
    response_data = {
        'verified': overall_verified,
        'average_distance': average_verified,
    }

    return Response(response_data)

























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