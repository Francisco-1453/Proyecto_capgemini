from django.http import HttpResponse
from django.template import Template, context, loader
from django.shortcuts import render
from .models import Database

def inicio_de_sesion(request):
    return render(request, "inicioSesion.html", {})

def registro(request):
    return render(request,"crearUsuario.html",{})

def registrar_usuario(request):
    usuario = request.POST["usuario"]
    nombre = request.POST["Nombre"]
    apellido = request.POST["Apellido"]
    dni = request.POST["dni"]
    telefono = request.POST["telefono"]
    clave = request.POST["password"]
    email = request.POST["email"]
    db = Database()
    if db.create_user(nombre, apellido, dni, email, telefono, usuario, clave):
        datos = db.get_user(usuario, clave)
        return render(request, "operaciones.html", {"id": datos[0], "nombre": nombre.capitalize(), "operacion": "Se ha creado su usuario", "flag": True})
    else:
        return render(request, "operaciones.html", {"nombre": "", "operacion": "Error: No se ha podido crear el usuario", "flag": False})

def inicio_sesion(request):
    usuario = request.POST["usuario"]
    clave = request.POST["clave"]
    db= Database()
    datos = db.get_user(usuario, clave)
    if datos:
        nombre = datos[1]
        id_usuario = datos[0]
        return render (request, "operaciones.html", {"id_usuario": id_usuario, "nombre": nombre.capitalize(), "operacion": "", "flag": True})
    else:
        return render(request, "operaciones.html", {"nombre": "", "operacion": "Usuario o contraseña incorrecta", "flag": False})

def movimientos(request):
    id=request.session["id"]
    db= Database()
    datos=db.get_movements(id)
    return render(request,"movimientos.html",{"id":id,"Datos":datos})