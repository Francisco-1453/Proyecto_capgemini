from datetime import datetime
import os
import json
from django.http import HttpResponse
from django.template import Template, context, loader
from django.shortcuts import render
from django.http.response import StreamingHttpResponse
import cv2
import numpy as np
import threading
from .models import Database

tipo_cambio = {"dolares": 166, "euros": 173, "pesos": 1}

def inicio_de_sesion(request):
    if 'id' in request.session.keys():
        del request.session['id']
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
        datos = db.inicio_sesion(usuario, clave)
        request.session["id"] = datos[0]
        return render(request, "operaciones.html", {"id": datos[0], "nombre": nombre.capitalize(), "operacion": "Se ha creado su usuario", "flag": True})
    else:
        return render(request, "operaciones.html", {"nombre": "", "operacion": "Error: No se ha podido crear el usuario", "flag": False})

def inicio_sesion(request):
    usuario = request.POST["usuario"]
    clave = request.POST["clave"]
    db= Database()
    datos = db.inicio_sesion(usuario, clave)
    if datos:
        nombre = datos[1]
        id_usuario = datos[0]
        request.session["id"] = datos[0]
        return render(request, "operaciones.html", {"id_usuario": id_usuario, "nombre": nombre.capitalize(), "operacion": "", "flag": True})
    else:
        return render(request, "operaciones.html", {"nombre": "", "operacion": "Usuario o contraseña incorrecta", "flag": False})

def cuentas(request):
    id = request.session["id"]
    db= Database()
    cuentas = db.get_cuentas(id)
    return render(request, "cuentas.html", {"id_usuario": id, "cuentas":cuentas})

def crear_cuenta(request):
    descripcion = request.POST["descripcion"]
    divisa = request.POST["divisa"]
    saldo = request.POST["saldo"]
    id_usuario = request.session["id"]
    db = Database()
    if db.create_cuenta(descripcion, divisa, saldo, id_usuario):
        db= Database()
        cuentas = db.get_cuentas(id_usuario)
        return render(request, "cuentas.html", {"operacion": "Cuenta creada exitosamente", "cuentas": cuentas})
    else:
        return render(request, "cuentas.html", {"operacion": "No se pudo crear la cuenta"})

def movimientos(request):
    id=request.session["id"]
    db = Database()
    datos = db.get_movements(id)
    return render(request, "movimientos.html", {"id": id, "Datos": datos})

def mis_tarjetas(request):
    id = request.session["id"]
    archivo = f"nombre_del_proyecto/jsons/{id}_tarjetas.json"
    try:
        if os.path.exists(archivo):
            file = open(archivo, "r")
            data = json.loads(file.read())
            print(type(data))
            print(data)
            file.close()
        else:
            return render(request, "misTarjetas.html", {"mensaje": "No posee tarjetas por el momento", "flag": False})
        return render(request, "misTarjetas.html", {"mensaje": "Sus tarjetas son", "Datos": data, "flag": True})
    except Exception:
        return render(request, "misTarjetas.html", {"mensaje": "Error", "flag": False})

def agregar_tarjetas(request):
    return render(request, "agregarTarjetas.html", {})

def Perfil(request):
    id=request.session["id"]
    db=Database()
    datos=db.get_user(id)
    return render(request,"Mi perfil.html",{"id":id,"Datos":datos})

def editar(request):
    id=request.session["id"]
    db= Database()
    a=db.get_user(id)
    return render(request, "Editar perfil.html", {"datos": a})


def editar_perfil(request):
    id=request.session["id"]
    nombre_usuario = request.POST["nombre_usuario"]
    email = request.POST["email"]
    telefono = request.POST["telefono"]
    db = Database() 
    db.update_user(id,nombre_usuario,email,telefono)
    a=db.get_user(id)
    return render(request,"Mi perfil.html",{"id":id,"Datos":a})


def transferir(request):
    id_usuario = request.session["id"]
    id_origen = request.POST["cuenta"]
    id_destino = request.POST["destino"]
    monto = int(request.POST["monto"])
    descripcion = request.POST["descripcion"]

    db = Database()

    origen = db.get_cuenta(id_origen)
    destino = db.get_cuenta(id_destino)

    monto = _to_divisa_(monto, origen[2], "pesos")
    saldo = _to_divisa_(origen[3], origen[2], "pesos")

    if destino and monto <= saldo:
        id_usuario_destino = destino[4]
        _descontar_cuenta_(origen, monto)
        _sumar_cuenta_(destino, monto)
        _log_movimiento_(id_usuario, id_origen, id_destino, descripcion, monto)
        _log_movimiento_(id_usuario_destino, id_destino, id_origen, descripcion, monto)
        operacion ="Transferencia realizada con exito"
    else:
        operacion= "No se pudo realizar la transferencia"

    cuentas = db.get_cuentas(id_usuario)
    
    return render(request, "cuentas.html", {"cuentas": cuentas, "operacion": operacion, "id_usuario": id_usuario})

def _to_divisa_(monto, divisa_original, divisa):
    return (monto*tipo_cambio[divisa_original]) / tipo_cambio[divisa]

def _descontar_cuenta_(cuenta, monto):
    db = Database()
    saldo_cuenta = float(cuenta[3])
    divisa_cuenta = cuenta[2]

    if divisa_cuenta == "pesos":
        nuevo_saldo = saldo_cuenta - monto
    else:
        monto = _to_divisa_(monto, "pesos", cuenta[2])
        nuevo_saldo = saldo_cuenta - monto
    db.actualizar_saldo_cuenta(cuenta[0], nuevo_saldo)

def _sumar_cuenta_(cuenta, monto):
    db = Database()
    saldo_cuenta = float(cuenta[3])
    divisa_cuenta = cuenta[2]

    if divisa_cuenta == "pesos":
        nuevo_saldo = saldo_cuenta + monto
        db.actualizar_saldo_cuenta(cuenta[0], nuevo_saldo)
    else:
        monto = _to_divisa_(monto, "pesos", cuenta[2])
        nuevo_saldo = saldo_cuenta + monto
        db.actualizar_saldo_cuenta(cuenta[0], nuevo_saldo)

def _log_movimiento_(id_usuario, cuenta_origen, cuenta_destino, descripcion, monto):
    fecha = datetime.now().isoformat(sep=' ')
    db = Database()
    db.logear_movimiento(id_usuario, cuenta_origen, cuenta_destino, descripcion, monto, fecha)

def volver(request):
    id_usuario = request.session["id"]
    db = Database()
    usuario = db.get_user(id_usuario)
    nombre = usuario[0]

    return render(request, "operaciones.html", {"id_usuario": id_usuario, "nombre": nombre.capitalize(), "operacion": "", "flag": True})

def agregar_tarjeta2(request):
    id = request.session["id"]
    numero = request.POST["numero"]
    codigo = request.POST["codigo"]
    tipo_tarj = request.POST["tipo"]
    archivo = f"nombre_del_proyecto/jsons/{id}_tarjetas.json"
    Datos = {
        "Numero": numero,
        "Codigo": codigo,
        "Tipo_Tarjeta": tipo_tarj
    }
    try:
        if os.path.exists(archivo):
            file = open(archivo, "r")
            data = json.loads(file.read())
            data.append(Datos)
            nuevo_json = json.dumps(data)
            file.close()
        else:
            nuevo_json = json.dumps([Datos])
        jsonfile = open(archivo, "w")
        jsonfile.write(nuevo_json)
        jsonfile.close()
        return render(request, "mensaje.html", {"mensaje": "Su tarjeta fue agregada con exito", "Datos": Datos, "flag": True})
    except Exception as e:
        print(e.with_traceback)
        return render(request, "mensaje.html", {"mensaje": "No se pudo agregar la tarjeta con exito", "flag": False})

def video(request):
    return StreamingHttpResponse(gen(Camara()), content_type='multipart/x-mixed-replace; boundary=frame')

def scan_template(request):
    id = request.session["id"]
    try:
        cam = Camara()

    except:
        pass
    return render(request, "scan.html", {"id": id})

class Camara():
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.ret, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        imagen = self.frame
        _, jpeg = cv2.imencode('.jpg', imagen)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.ret, self.frame) = self.video.read()

def gen(camara):
    while True:
        frame = camara.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


