from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework import permissions

from apps.accounts.views import VKLogin

schema_view: get_schema_view = get_schema_view(
    openapi.Info(
        title="Social Core Swagger",
        default_version='v1',
        description="Social Core Apies",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('ckeditor5/', include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path('captcha/', include('captcha.urls')),

    path('auth/vk/', VKLogin.as_view(), name='vk_login'),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/social/', include('allauth.socialaccount.urls')),
]

urlpatterns += [
    path('api/account/', include('apps.accounts.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/blogs/', include('apps.blog.urls')),
    path('api/chat/', include('apps.chat.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT, }, ), ]
