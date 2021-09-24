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

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from controle_colaboradores_api.apps.usuarios.urls import router as usuarios_router
from controle_colaboradores_api.apps.perfis.urls import router as perfis_router
from controle_colaboradores_api.apps.localidades_brasileiras.urls import router as localidades_brasileiras_router

main_router = DefaultRouter()

main_router.registry.extend(usuarios_router.registry)
main_router.registry.extend(perfis_router.registry)
main_router.registry.extend(localidades_brasileiras_router.registry)

urlpatterns = [
    path('api/v1/', include(main_router.urls)),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
]
