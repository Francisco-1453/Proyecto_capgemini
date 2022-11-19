import json 
import pymysql
# definimos un objeto


class Database():

    def __init__(self):
        # creamos el constructor que establece al conexion con la bd
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password="",
            db=''
        )  # chequeo que la conexion de la base funcione, sino no se conecta y lanza un error
        self.cursor = self.connection.cursor()
        print("la coneccion fue exitosa")
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
    def get_user(self, ide):
            sql = "Select * FROM usuarios WHERE ID_usuario = '{}'".format(ide)
            try:
                self.cursor.execute(sql)
                user = self.cursor.fetchone()
                print("ID:", user[0])
                print("nombre: ", user[1])
                print("Constrasenia:", user[2])
                print("Saldo: ",user[3])
            except Exception as e:
                print("No existe ese usuario")
            

    # CRUD
    #crear usuario
    def create_user(self, n_nuevo, n_contrasenia,n_saldo):
        sql = "INSERT INTO usuarios(nombre, contrasenia,saldo) VALUES ('{}','{}','{}')".format( n_nuevo, n_contrasenia,n_saldo)
        try:    
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print("no se creo el usuario")
    #borrar usuario  
    def delete_user(self,ide):
        sql="DELETE FROM usuarios where ID_usuario='{}'".format(ide)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print("no se elimino el usuario")
    #Actualizar el usuario
    def uptade_user(self,ide,n_nombre,n_contrasenia):
        sql="UPDATE usuarios SET nombre= '{}', contrasenia='{}' WHERE ID_usuario= '{}'".format(n_nombre,n_contrasenia,ide)
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
    # try:
        # codigo que queremos probar
    # except:
        # que queremos que haga si falla

#json

# ListaBanco= open("banco.json","r")
# textoBanco=ListaBanco.read()