from urllib.parse import urlparse, parse_qs
from datetime import datetime
import requests
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
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
from apps.users.serializers import UserDetailSerializer

User = get_user_model()

USER_FIELDS = [
    "first_name", "last_name", "nickname", "screen_name", "sex", "bdate", "city",
    "country", "timezone", "photo", "photo_medium", "photo_big", "photo_max_orig",
    "has_mobile", "contacts", "education", "online", "counters", "relation",
    "last_seen", "activity", "universities",
]


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
        base_url = 'https://healthsphere.ru/'
        captcha_key = CaptchaStore.generate_key()
        captcha_image_url = f"{base_url}captcha/image/{captcha_key}/"

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
        serializer = UpdateUserSerializer(user, data=request.data, partial=True, context={'request': request})
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


class CustomUserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: UserDetailSerializer()},
        operation_description="Retrieve details of the guest user.", tags=['Account']
    )
    def get(self, request, *args, **kwargs):
        user_model = get_user_model()
        user = get_object_or_404(user_model, id=kwargs.get('id'))
        serializer = UserDetailSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=PasswordUpdateSerializer,
        tags=['Account'],
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


class VKAuthAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Получение access_token от VK",
        operation_description="Этот эндпоинт принимает callback_url, извлекает code и получает access_token от VK API.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "callback_url": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="URL с кодом авторизации VK, полученным после логина."
                )
            },
            required=["callback_url"]
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "access_token": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Токен доступа VK."
                    )
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Описание ошибки."
                    )
                }
            ),
        }
    )
    def post(self, request):
        callback_url = request.data.get("callback_url")

        if not callback_url:
            return Response({"error": "callback_url is required"}, status=status.HTTP_400_BAD_REQUEST)

        parsed_url = urlparse(callback_url)
        query_params = parse_qs(parsed_url.query)
        code = query_params.get("code", [None])[0]

        if not code:
            return Response({"error": "Authorization code not found"}, status=status.HTTP_400_BAD_REQUEST)

        token_url = (
            f"https://oauth.vk.com/access_token?"
            f"client_id=52982778&"
            f"client_secret=tPZ6YRgnZzwubzWy7RyF&"
            f"redirect_uri=https://patient-opal.vercel.app/auth/vk/login/callback/in&"
            f"code={code}"
        )

        response = requests.get(token_url)

        if response.status_code == 200:
            data = response.json()
            access_token = data.get("access_token")

            if not access_token:
                return Response({"error": "access_token not found"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"access_token": access_token}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Failed to get access token", "details": response.text},
                status=response.status_code,
            )


class VKLogin(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Аутентификация через VK",
        operation_description="Получает `access_token` VK, запрашивает профиль пользователя и возвращает JWT токены.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "access_token": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="VK access token, полученный после авторизации."
                )
            },
            required=["access_token"]
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "access_token": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="JWT access token."
                    ),
                    "refresh_token": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="JWT refresh token."
                    ),
                    "user_data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description="Данные пользователя VK.",
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="VK ID пользователя."),
                            "first_name": openapi.Schema(type=openapi.TYPE_STRING, description="Имя."),
                            "last_name": openapi.Schema(type=openapi.TYPE_STRING, description="Фамилия."),
                            "photo_max_orig": openapi.Schema(type=openapi.TYPE_STRING, description="URL аватара.")
                        }
                    )
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Описание ошибки.")
                }
            ),
            500: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Ошибка на сервере.")
                }
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        access_token = data.get("access_token")

        if not access_token:
            return Response({"error": "Access token is required"}, status=status.HTTP_400_BAD_REQUEST)

        profile_url = "https://api.vk.com/method/users.get"
        params = {
            "v": "5.131",
            "access_token": access_token,
            "fields": ",".join(USER_FIELDS),
        }

        try:
            response = requests.get(profile_url, params=params)
            response.raise_for_status()
            user_data = response.json().get("response", [{}])[0]

            if not user_data:
                return Response({"error": "No user data found"}, status=status.HTTP_404_NOT_FOUND)

            vk_id = user_data.get("id")
            first_name = user_data.get("first_name", "")
            last_name = user_data.get("last_name", "")
            bdate = user_data.get("bdate", "")
            photo_url = user_data.get("photo_max_orig", "")

            username = f"vk_{vk_id}"

            user, created = User.objects.get_or_create(username=username, defaults={
                "first_name": first_name,
                "last_name": last_name,
                'birth_date': datetime.strptime(bdate, "%d.%m.%Y").date() if bdate else None,
            })

            if photo_url:
                photo_response = requests.get(photo_url)
                if photo_response.status_code == 200:
                    avatar_name = f"avatars/{username}.jpg"
                    user.avatar.save(avatar_name, ContentFile(photo_response.content), save=True)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "access_token": access_token,
                "refresh_token": str(refresh),
                "user_data": user_data
            }, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# https://oauth.vk.com/authorize?client_id=52982778&redirect_uri=https://patient-opal.vercel.app/auth/vk/login/callback/&display=page&scope=email&response_type=code&v=5.131