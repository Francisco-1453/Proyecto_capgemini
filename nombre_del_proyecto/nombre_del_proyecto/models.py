import json 
import pymysql
# definimos un objeto


class Database():

    def __init__(self):
        # creamos el constructor que establece al conexion con la bd
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password="46386865",
            db='esquema_homebanking'
        )  # chequeo que la conexion de la base funcione, sino no se conecta y lanza un error
        self.cursor = self.connection.cursor()
# metodos para gestionar la base de datos:

    # metodo para traer todos los usuarios

    def all_users(self):
            sql = 'SELECT * FROM usuarios'

            self.cursor.execute(sql)
            users = self.cursor.fetchall()

            for user in users:
             print("ID:", user[0])
             print("nombre: ", user[1])
             print("Constrasenia:", user[2])
             print("Saldo: ", user[3])

# metodo para crear un usuraio en particular
    def get_user(self,id):
            sql = f'SELECT nombre,apellido,nombre_usuario,DNI,email,telefono FROM usuarios WHERE id_usuario = "{id}"'
            try:
                self.cursor.execute(sql)
                user = self.cursor.fetchone()
                return user
            except Exception as e:
                print("Ocurrio un error")
                return ()
            
    def inicio_sesion(self, usuario, clave):
            sql = f'SELECT * FROM usuarios WHERE nombre_usuario = "{usuario}" AND clave = "{clave}"'
            try:
                self.cursor.execute(sql)
                user = self.cursor.fetchone()
                return user
            except Exception as e:
                print("Error al ejecutar la query")
                return ()

    # CRUD
    #crear usuario
    def create_user(self, nombre, apellido, dni, email, telefono, usuario, clave):
        sql = f'INSERT INTO usuarios(nombre, apellido,dni, email, telefono, nombre_usuario, clave) VALUES ("{nombre}","{apellido}",{dni}, "{email}", "{telefono}", "{usuario}", "{clave}")'
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception:
            return False
        return True

    #borrar usuario  
    def delete_user(self,ide):
        sql="DELETE FROM usuarios where ID_usuario='{}'".format(ide)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print("no se elimino el usuario")

    #Actualizar el usuario
    def update_user(self,id,nombre_usuario,email,telefono):
    
        sql=f"UPDATE usuarios SET nombre_usuario= '{nombre_usuario}', email='{email}', telefono='{telefono}' WHERE ID_usuario= {id}"
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print("no se pudo actualizar el usuario")
    #Actualizar saldo
    def update_credit(self,ide,n_saldo):
        sql="UPDATE usuarios SET Saldo='{}' WHERE ID_usuario='{}'".format(n_saldo,ide)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print("no se pudo actualizar el saldo")


    #Trae la info de las tarjetas
    def traer_Tarjeta(self,id):
        sql=f"SELECT * FROM tarjetas WHERE id_usuario={id}"
        try:
            self.cursor.execute(sql)
            tarjeta=self.cursor.fetchall()
            return tarjeta
        except Exception as e:
            print("No se pudo traer las tarjetas")


    def get_movements(self,id):
        sql=f"SELECT * FROM movimientos WHERE id_usuario={id}"
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            return self.cursor.fetchall()
        except Exception as e:
           return print ("Algo sali?? mal...")
        


    def create_cuenta(self, descripcion, divisa, saldo, id_usuario):
        sql = f'INSERT INTO cuenta(descripcion, divisa, saldo, id_usuario) VALUES ("{descripcion}", "{divisa}", {saldo}, {id_usuario})'
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception:
            return False
        return True

    def get_cuentas(self, id):
        sql = f'SELECT id_cuenta, descripcion, divisa, saldo FROM cuenta WHERE id_usuario = {id}'
        self.cursor.execute(sql)
        self.connection.commit()
        return self.cursor.fetchall()

    def get_cuenta(self, id_cuenta):
        sql = f'SELECT * FROM cuenta WHERE id_cuenta = {id_cuenta}'
        self.cursor.execute(sql)
        self.connection.commit()
        return self.cursor.fetchone()

    def actualizar_saldo_cuenta(self, cuenta, nuevo_saldo):
        sql = f'UPDATE cuenta SET saldo= {nuevo_saldo} WHERE id_cuenta = {cuenta}'
        self.cursor.execute(sql)
        self.connection.commit()

    def logear_movimiento(self, id_usuario, cuenta_origen, cuenta_destino, descripcion, monto, fecha):
        sql = f'INSERT INTO movimientos(monto, descripcion, fecha, id_cuenta_origen, id_cuenta_destino, id_usuario) VALUES ({monto}, "{descripcion}", "{fecha}", {cuenta_origen}, {cuenta_destino}, {id_usuario})'
        print(sql)
        self.cursor.execute(sql)
        self.connection.commit()
