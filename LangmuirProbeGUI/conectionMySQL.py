
import mysql.connector

class Conexion():
    # Conectar a MySQL
    def __init__(self):
        try:
            # Establecer conexión a MySQL
            self.con = mysql.connector.connect(
                                                host='localhost',
                                                user='root',
                                                password='Joseluisce20214509'
                                            )
            
            # Crear una nueva base de datos si no existe
            cur = self.con.cursor()
            cur.execute("CREATE DATABASE IF NOT EXISTS LANGPROBE_DB")
            # Seleccionar la base de datos recién creada o existente
            cur.execute("USE LANGPROBE_DB")
            cur.close()
            
            self.CreatetTableUser()
            
        except Exception as ex:
            print(ex)
            
    def CreatetTableUser(self):

        # Crear una tabla llamada 'usuarios' si no existe
        sql_create_table = """
                            CREATE TABLE IF NOT EXISTS Users (
                            ID INT AUTO_INCREMENT PRIMARY KEY,
                            Name VARCHAR(255),
                            User VARCHAR(255) UNIQUE,
                            Password VARCHAR(255)
                            )
                            """
        cur = self.con.cursor()                    
        cur.execute(sql_create_table)
        cur.close()
        self.CreateAdmin()
            
    def CreateAdmin(self):
        try:
            sql_insert_admin = """INSERT IGNORE INTO Users (Name, User, Password) VALUES (%s,%s,%s)"""
            values = ("Administrator","admin","josel1234")
            cur = self.con.cursor()
            cur.execute(sql_insert_admin,values)
            self.con.commit()
            cur.close()
            #self.con.close()
        except Exception as ex:
            print(ex)
    
    def Connect(self):
        return self.con

#con = Conexion()