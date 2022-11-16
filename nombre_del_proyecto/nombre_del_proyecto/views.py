from django.http import HttpResponse
from django.template import Template, context, loader
from django.shortcuts import render

def inicio_de_sesion(request):
    return render(request, "index.html", {})
    
