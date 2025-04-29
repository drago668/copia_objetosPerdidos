"""
URL configuration for gestion_freelancers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from gestion.views import index,registrar,publicar_objeto,listar_objetos,solicitar_prestamo,listar_objetos_prpietario
from django.contrib.auth import views as auth_views
from gestion import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("", index, name='inicio'),
    path('registrar/', registrar, name='registrar'),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path("publicar/", publicar_objeto, name='publicar'),
    path("verMios/", listar_objetos_prpietario, name='listar_objetos_propietario'),
    path("verObjetos/", listar_objetos, name='listar_objetos'),
    path('solicitar/<int:objeto_id>/', solicitar_prestamo, name='solicitar_prestamo'),
    path('gestionar_solicitudes/', views.gestionar_solicitudes, name='gestionar_solicitudes'),
    path('solicitudes_aprobadas/', views.solicitudes_aprobadas, name='solicitudes_aprobadas'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
