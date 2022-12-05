"""nombre_del_proyecto URL Configuration

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
from django.urls import path
from nombre_del_proyecto.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio_de_sesion),
    path('registro/',registro),
    path('registrar_usuario/', registrar_usuario),
    path('mis-cuentas/', cuentas),
    path('mis-cuentas/crear/', crear_cuenta),
    path('mis-cuentas/transferir/', transferir),
    path('inicio_sesion/', inicio_sesion),
    path('movimientos/', movimientos),
    path('mis_tarjetas/', mis_tarjetas),
    path('agregar_tarjetas/', agregar_tarjetas),
    path('Mi_perfil/', Perfil),
    path('editar/', editar),
    path('editar_perfil/', editar_perfil),
    path('volver/', volver),
    path('agregar-tarjetas2/', agregar_tarjeta2)
]
