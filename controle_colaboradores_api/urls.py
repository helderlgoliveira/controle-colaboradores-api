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
from django.contrib import admin
from django.urls import path, include

from api_cursos.urls import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('appexemplo.urls')),

    path('minhaconta/', include('django.contrib.auth.urls')),

    path('api/v1/', include('api_cursos.urls')),
    path('api/v2/', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]

"""
admin.site.site_header = 'Geek University'
admin.site.site_title = 'Evolua seu lado geek!'
admin.site.index_title = 'Sistema de Gerenciamento de Posts'
"""

"""
O include do minhaconta/ inclui:

minhaconta/login/ [name='login']
minhaconta/logout/ [name='logout']
minhaconta/password_change/ [name='password_change']
minhaconta/password_change/done/ [name='password_change_done']
minhaconta/password_reset/ [name='password_reset']
minhaconta/password_reset/done/ [name='password_reset_done']
minhaconta/reset/<uidb64>/<token>/ [name='password_reset_confirm']
minhaconta/reset/done/ [name='password_reset_complete']

- Lembrando que a página de login, por padrão fica no caminho: /RAIZ_DO_PROJETO_registration/login.html
Talvez precise fazer modificações para ela ser encontrada na raiz do app usuarios, em vez da raiz do projeto.
"""