
import conectionMySQL as con
from model.user import User

class userdata():
    
    def login(self, user: User):
        try:
            conection_ = con.Conexion()
            self.db = conection_.Connect()
            #if self.db.is_connected():
            #    print("Conexión exitosa a la base de datos")
            cur = self.db.cursor()
            sql_select_user = """SELECT * FROM Users WHERE User = %s AND Password = %s"""
            values = (user._user, user._password)
            #self.cur.execute(sql_select_user, values)
            #print("Resultado de execute():", res)
            cur.execute(sql_select_user, values)
            row = cur.fetchall()
            #print(cur)
            #print("Resultado de execute():", row)
            if row:
                #print("SIIIIIIII")
                #print(row)
                user = User(Name=row[0][1],User=row[0][2])
                cur.close()
                self.db.close()
                return user
            else:
                #self.db.close()
                #print("PTMR")
                return None
        except Exception as ex:
            print(ex)
        
       