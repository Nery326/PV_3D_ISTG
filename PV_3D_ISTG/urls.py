"""Sistemas_facturacion_3d URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import path,include,re_path
from django.contrib.auth.decorators import login_required
from loginApp.views import Inicio,Login,logoutUsuario
from menuApp.views import dynamicmenu,dashobord
from loginApp.views import listTrabajadores,CrearTrabajador,EditarTrabajador,EliminarTrabajador,\
                            listUsuarios,RegistarUsuario,CambiarPassword

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Inicio.as_view(), name='index'),
    path('accounts/login/', Login.as_view(), name='login'),
    path('dynamicmenu/', dynamicmenu, name='dynamicmenu' ),
    path('logout/', login_required(logoutUsuario), name='logout'),
    path('dashboard/', dashobord, name='dashboard'),
    path('crearTrabajador/', CrearTrabajador.as_view(), name='crearTrabajador'),
    path('editarTrabajador/<int:pk>', EditarTrabajador.as_view(), name='editarTrabajador'),
    path('eliminar_trabajador/<int:pk>',EliminarTrabajador.as_view(), name='eliminar_trabajador'),
    path('listado_trabajadores/', listTrabajadores.as_view(), name='listado_trabajadores'),
    path('lista_Usuarios/',listUsuarios.as_view(), name='listaUsuarios'),
    path('registar_Usuarios/', RegistarUsuario.as_view(), name='registar_Usuarios'),
    path('cambiar_password/',CambiarPassword.as_view(), name='cambiar_password'),


] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
