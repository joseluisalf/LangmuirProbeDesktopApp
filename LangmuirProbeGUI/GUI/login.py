
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from GUI.main import MainWindow
from data.user import userdata
from model.user import User

class Login():
    def __init__(self):
        self.login = uic.loadUi("GUI/login.ui")
        self.initGUI()
        self.login.lblMessage.setText("")
        self.login.show()
        
    def access(self):
        if len(self.login.txtUser.text()) < 2:
            self.login.lblMessage.setText("Ingrese un usuario válido")
            self.login.txtUser.setFocus()
        elif len(self.login.txtPassword.text()) < 3:
            self.login.lblMessage.setText("Ingrese una contraseña válida")
            self.login.txtPassword.setFocus()
        else:
            self.login.lblMessage.setText("")
            usu = User(User=self.login.txtUser.text(), Password=self.login.txtPassword.text())
            #print(usu._user,usu._password)
            usuData = userdata()
            res = usuData.login(usu)
            if res:
                #self.login.lblMessage.setText("OK")
                self.main = MainWindow(usu._user)
                self.login.hide()
            else:
                self.login.lblMessage.setText("Datos de acceso incorrecto")
            
    def initGUI(self):
        self.login.btnAccess.clicked.connect(self.access)
                    
            