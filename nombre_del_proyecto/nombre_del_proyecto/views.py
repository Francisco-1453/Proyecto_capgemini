from django.http import HttpResponse
from django.template import Template, context, loader
from django.shortcuts import render
from .models import Database

def inicio_de_sesion(request):
    return render(request, "index.html", {})

def crear_usuario(request):
    return render(request,"crearUsuario.html",{})

