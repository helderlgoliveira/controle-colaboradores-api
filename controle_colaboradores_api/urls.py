""" Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include

from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from controle_colaboradores_api.apps.usuarios.urls import router as usuarios_router
from controle_colaboradores_api.apps.perfis.urls import router as perfis_router
from controle_colaboradores_api.apps.localidades_brasileiras.urls import router as localidades_brasileiras_router

schema_view = get_schema_view(
   openapi.Info(
      title="Controle de Colaboradores API",
      default_version='v1',
      description="API para controle de aspectos relativos a colaboradores em uma empresa/instituição.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contato@dominio.com.br"),
      license=openapi.License(name="BSD License"),
   ),
   public=False,
   permission_classes=(permissions.AllowAny,),
)

api_docs_urlpatterns = [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]

main_router = DefaultRouter()

main_router.registry.extend(usuarios_router.registry)
main_router.registry.extend(perfis_router.registry)
main_router.registry.extend(localidades_brasileiras_router.registry)
main_router.registry.extend(localidades_brasileiras_router.registry)

api_v1 = main_router.urls + api_docs_urlpatterns

urlpatterns = [
   path('api/v1/', include(api_v1)),
   path('api/auth/', include('rest_framework.urls', namespace='rest_framework'))
]
