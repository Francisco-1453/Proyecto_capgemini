from django.http import HttpResponse
from django.template import Template, context, loader
from django.shortcuts import render
from .models import Database

def inicio_de_sesion(request):
    return render(request, "inicioSesion.html", {})

def registro(request):
    return render(request,"crearUsuario.html",{})

def registrar_usuario(request):
    usuario = request.GET["usuario"]
    nombre = request.GET["Nombre"]
    apellido = request.GET["Apellido"]
    dni = request.GET["dni"]
    telefono = request.GET["telefono"]
    clave = request.GET["password"]
    email = request.GET["email"]
    db = Database()
    if db.create_user(nombre, apellido, dni, email, telefono, usuario, clave):
        print("USUARIO CREADO EXITOSAMENTE")
        return render(request, "operaciones.html", {"nombre": nombre})
    else:
        print("NO SE PUDO CREAR EL USUARIO")
        return render(request, "operaciones.html", {"nombre": "No se ha podido crear usuario"})

