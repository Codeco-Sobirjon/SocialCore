from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from captcha.models import CaptchaStore
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext as _

from apps.accounts.serializers import SignUpSerializer, CustomAuthTokenSerializer, CustomUserDetailSerializer, \
    UpdateUserSerializer, PasswordUpdateSerializer


class GenerateCaptchaAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["Captcha"],
        operation_summary="Генерация CAPTCHA",
        operation_description="Создает новую CAPTCHA и возвращает ключ и URL изображения.",
        responses={
            200: openapi.Response(
                description="Успешная генерация CAPTCHA",
                examples={
                    "application/json": {
                        "captcha_key": "some_hash_key",
                        "captcha_image_url": "/captcha/image/some_hash_key/"
                    }
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        base_url = settings.BASE_URL
        captcha_key = CaptchaStore.generate_key()
        captcha_image_url = f"{base_url}/captcha/image/{captcha_key}/"

        return Response({
            "captcha_key": captcha_key,
            "captcha_image_url": captcha_image_url
        })


class UserSignupView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=SignUpSerializer, tags=['Account'])
    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthTokenView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=CustomAuthTokenSerializer, tags=['Account'])
    def post(self, request):
        serializer = CustomAuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: CustomUserDetailSerializer()},
        operation_description="Retrieve details of the authenticated user.", tags=['Account']
    )
    def get(self, request):
        user = request.user
        serializer = CustomUserDetailSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UpdateUserSerializer,
        responses={200: UpdateUserSerializer()},
        operation_description="Update the authenticated user's profile.", tags=['Account']
    )
    def put(self, request):
        user = request.user
        serializer = UpdateUserSerializer(user, data=request.data, partial=True, context={'request': request} )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: 'No Content'},
        operation_description="Delete the authenticated user's account.", tags=['Account']
    )
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"detail": _("User deleted successfully.")}, status=status.HTTP_204_NO_CONTENT)


class PasswordUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=PasswordUpdateSerializer,
        tags = ['Account'],
        responses={
            200: "Password updated successfully.",
            400: "Bad Request: Password update failed."
        },
        operation_description="Update the authenticated user's password."
    )
    def patch(self, request):
        serializer = PasswordUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
