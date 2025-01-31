from django.urls import path

from apps.accounts.views import (
    GenerateCaptchaAPIView, UserSignupView, CustomAuthTokenView, CustomUserDetailView, PasswordUpdateView
)

urlpatterns = [
    path('captcha/generate/', GenerateCaptchaAPIView.as_view(), name='generate_captcha'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('signin/', CustomAuthTokenView.as_view(), name='signin'),
    path('user/', CustomUserDetailView.as_view(), name='user-detail'),
    path('update-password/', PasswordUpdateView.as_view(), name='update-password'),
]
