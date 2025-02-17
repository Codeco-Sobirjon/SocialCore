from django.urls import path

from apps.accounts.views import (
    GenerateCaptchaAPIView, UserSignupView, CustomAuthTokenView, CustomUserDetailView, PasswordUpdateView,
    CustomUserView, VKAuthAPIView, VKLogin
)

urlpatterns = [
    path('captcha/generate/', GenerateCaptchaAPIView.as_view(), name='generate_captcha'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('signin/', CustomAuthTokenView.as_view(), name='signin'),
    path('user/', CustomUserDetailView.as_view(), name='user-detail'),
    path('guest/user/<int:id>/', CustomUserView.as_view(), name='guest-user-detail'),
    path('update-password/', PasswordUpdateView.as_view(), name='update-password'),
    path("auth/check/vk/", VKAuthAPIView.as_view(), name="vk-auth"),
    path('auth/vk/', VKLogin.as_view(), name='vk_login'),
]
