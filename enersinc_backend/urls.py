from django.contrib import admin
from django.urls import path, include, re_path
from apps.person.views import LoginView, ValidateTokenView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API - Prueba enersinc",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="daceron96@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('person/',include('apps.person.api.routers')),
    path('login/',LoginView.as_view(), name = 'login'),
    path('validateToken/',ValidateTokenView.as_view(), name = 'validateToken'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
