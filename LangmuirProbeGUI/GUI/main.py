
#import sys
#sys.path.append('../dataProcessing')

import os
import pandas as pd
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt6.QtWidgets import QFileDialog

#from dataProcessing.returnData import return_all_data
from model.project import Project
import conectionMySQL as con
from dataBaseTables import langProbeTables, ProjectTable
from dataProcessing.returnData import return_all_data
from dataProcessing.returnTransposeData import df_all_data_function

class MainWindow():
    def __init__(self, user):
        self.main = uic.loadUi("GUI/main.ui")
        self.mainUser = user # Para agregar la información del usuario a la tabla de medidas
        self.initGUI()
        self.main.showMaximized()

#################################### DESPLIEGUE DE VENTANAS ################################ 
    def initGUI(self):
        
        self.main.btnProyectos.triggered.connect(self.OpenManagerProject)
        self.main.btnIngresar_medidas.triggered.connect(self.OpenSaveDataWindow)
        self.projectManager = uic.loadUi("GUI/projectManager.ui")
        self.createProject = uic.loadUi("GUI/createProject.ui")
        self.editProject = uic.loadUi("GUI/editProject.ui")
        self.deleteProject = uic.loadUi("GUI/deleteProject.ui")
        self.noProjectSelected = uic.loadUi("GUI/noProjectSelected.ui")
        self.saveData = uic.loadUi("GUI/saveData2.ui")
        self.noData = uic.loadUi("GUI/noData.ui")
        self.incompleteLoadData = uic.loadUi("GUI/incompleteLoadData.ui")
        self.missingUploadFiles = uic.loadUi("GUI/missingUploadFiles.ui")
        self.successfulChargeDataBase = uic.loadUi("GUI/successfulChargeDataBase.ui")
    
##################################### GESTOR DE PROYECTOS ##################################

    def OpenManagerProject(self):
        # --------------- Ajuste del ancho de las columnas del tableiwdget -----------------
        self.projectManager.tblwProjects.setColumnWidth(0,120)
        self.projectManager.tblwProjects.setColumnWidth(1,120)
        self.projectManager.tblwProjects.setColumnWidth(2,160)
        self.projectManager.tblwProjects.setColumnWidth(3,140)
        self.projectManager.tblwProjects.setColumnWidth(4,196)
        self.projectManager.show()
        ######################### CREACIÓN DE LA TABLA DE PROYECTOS #########################
        conection_ = con.Conexion()
        self.db = conection_.Connect()
        cur = self.db.cursor()
        cur.execute("USE LANGPROBE_DB")
        cur.close()
        projectTable = ProjectTable() # función que contiene la consulta SQL
        cur = self.db.cursor()                    
        cur.execute(projectTable)
        cur.close()
        self.db.close()
        ###################### MOSTRAS LOS REGISTROS EN EL TABLEWIDGET ##############################
        
        conection_ = con.Conexion()
        self.db = conection_.Connect()
        cur = self.db.cursor()
        cur.execute("USE LANGPROBE_DB")
        cur.close() 
        cur = self.db.cursor()
        cur.execute("SELECT * FROM projects")
        records_project = cur.fetchall()
        #print(records_project)
        self.projectManager.tblwProjects.setRowCount(len(records_project))
        #self.projectManager.tblwProjects.setColumnCount(len(records_project[0]))
        self.projectManager.tblwProjects.setColumnCount(5) # 5 columnas configuradas
         # Insertar los datos en el tableWidgget
        for i, row in enumerate(records_project):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.projectManager.tblwProjects.setItem(i, j, item)
        self.db.commit()
        cur.close()
        self.db.close()
        
        #############################################################################################
        self.projectManager.btnNewProject.clicked.connect(self.CreateNewProject)
        self.projectManager.btnModifyProject.clicked.connect(self.ModifyExistingProject)
        self.projectManager.btnDeleteProject.clicked.connect(self.DeleteExistingProject)
        self.filterForUsers()
        self.projectManager.btnFilterProject.clicked.connect(self.FilterProjects)
        
##################################### CREAR PROYECTOS ######################################        
        
    def CreateNewProject(self):
        self.createProject.lblMessage.setText("")
        self.createProject.btnCreateProject.clicked.connect(self.CreateProject)
        self.createProject.show()
        
    def CreateProject(self):
        if len(self.createProject.txtID.text()) < 2:
            self.createProject.lblMessage.setText("Ingrese un ID válido")
            self.createProject.txtID.setFocus()
        elif len(self.createProject.txtUser.text()) < 2:
            ## Aquí tenemosque comparar con los usuarios registrados en la tabla de datos "users"
            self.createProject.lblMessage.setText("Ingrese un Usuario válido")
            self.createProject.txtUser.setFocus()
        elif len(self.createProject.txtNameProject.text()) < 2:
            self.createProject.lblMessage.setText("Ingrese un Nombre válido")
            self.createProject.txtNameProject.setFocus()
        elif len(self.createProject.txtDate.text()) < 2:
            self.createProject.lblMessage.setText("Ingrese una fecha válida")
            self.createProject.txtDate.setFocus()
        elif len(self.createProject.txtDescription.text()) < 2:
            self.createProject.lblMessage.setText("Ingrese una descripción válida")
            self.createProject.txtDescription.setFocus()
        else:
            self.createProject.lblMessage.setText("")
            ## Aquí ingresaremos los datos a la tabla de "projects"
            project = Project(ID=self.createProject.txtID.text(), 
                          User=self.createProject.txtUser.text(),
                          NameProject=self.createProject.txtNameProject.text(),
                          Date=self.createProject.txtDate.text(),
                          Description=self.createProject.txtDescription.text())
            #print(project._nameProject)
            conection_ = con.Conexion()
            self.db = conection_.Connect()
            cur = self.db.cursor()
            cur.execute("USE LANGPROBE_DB")
            cur.close() 
            cur = self.db.cursor()
            sql_insert_project = """
                            INSERT INTO projects (
                                `ID del proyecto`, 
                                Usuario, 
                                `Nombre del proyecto`, 
                                `Fecha de creación`, 
                                Descripción)
                            VALUES (%s, %s, %s, %s, %s)
                        """
            # Definimos los valores a insertar
            values_project = (project._id, project._user, project._nameProject, project._date, project._description)
            cur.execute(sql_insert_project,values_project)
            self.db.commit()
            cur.close()
        
            cur = self.db.cursor()
            cur.execute("SELECT * FROM projects")
            records_project = cur.fetchall()
            #print(records_project)
            self.projectManager.tblwProjects.setRowCount(len(records_project))
            self.projectManager.tblwProjects.setColumnCount(len(records_project[0]))
            # Insertar los datos en el tableWidgget
            for i, row in enumerate(records_project):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.projectManager.tblwProjects.setItem(i, j, item)
            self.db.commit()
            cur.close()
            self.db.close()
            
            self.createProject.txtID.clear()
            self.createProject.txtUser.clear()
            self.createProject.txtNameProject.clear()
            self.createProject.txtDate.clear()
            self.createProject.txtDescription.clear()
            self.createProject.close()    
    
##################################### MODIFICAR PROYECTOS ##################################

    def ModifyExistingProject(self):
        self.selected_row = self.projectManager.tblwProjects.currentRow()
        if self.selected_row != -1:  # Verificar si se ha seleccionado una fila
            # Obtener los valores de la fila seleccionada
            row_values = [self.projectManager.tblwProjects.item(self.selected_row, column).text() for column in range(self.projectManager.tblwProjects.columnCount())]
            self.editProject.txtID.setText(row_values[0])
            self.editProject.txtUser.setText(row_values[1])
            self.editProject.txtNameProject.setText(row_values[2])
            self.editProject.txtDate.setText(row_values[3])
            self.editProject.txtDescription.setText(row_values[4])
            self.old_id = self.editProject.txtID.text()
            
            self.editProject.lblMessage.setText("")
            self.editProject.btnCreateProject.clicked.connect(self.ModifyProject)
            self.editProject.show()
        else:
            self.noProjectSelected.show()

    def ModifyProject(self):
    
            if len(self.editProject.txtID.text()) < 2:
                self.editProject.lblMessage.setText("Ingrese un ID válido")
                self.editProject.txtID.setFocus()
            elif len(self.editProject.txtUser.text()) < 2:
            ## Aquí tenemosque comparar con los usuarios registrados en la tabla de datos "users"
                self.editProject.lblMessage.setText("Ingrese un Usuario válido")
                self.editProject.txtUser.setFocus()
            elif len(self.editProject.txtNameProject.text()) < 2:
                self.editProject.lblMessage.setText("Ingrese un Nombre válido")
                self.editProject.txtNameProject.setFocus()
            elif len(self.editProject.txtDate.text()) < 2:
                self.editProject.lblMessage.setText("Ingrese una fecha válida")
                self.editProject.txtDate.setFocus()
            elif len(self.editProject.txtDescription.text()) < 2:
                self.editProject.lblMessage.setText("Ingrese una descripción válida")
                self.editProject.txtDescription.setFocus()
            else:
                self.editProject.lblMessage.setText("")
                ## Aquí ingresaremos los datos a la tabla de "projects"
                edited_project = Project(ID=self.editProject.txtID.text(), 
                            User=self.editProject.txtUser.text(),
                            NameProject=self.editProject.txtNameProject.text(),
                            Date=self.editProject.txtDate.text(),
                            Description=self.editProject.txtDescription.text())
                #print(project._nameProject)
                conection_ = con.Conexion()
                self.db = conection_.Connect()
                cur = self.db.cursor()
                cur.execute("USE LANGPROBE_DB")
                cur.close() 
                cur = self.db.cursor()
                sql_edit_row = "UPDATE projects SET `ID del proyecto` = %s, Usuario = %s, `Nombre del proyecto` = %s, `Fecha de creación` = %s, Descripción = %s WHERE `ID del proyecto` = %s"
                new_values = (edited_project._id,
                              edited_project._user,
                              edited_project._nameProject,
                              edited_project._date,
                              edited_project._description)
                cur.execute(sql_edit_row, (*new_values, self.old_id))  # Se asume que la columna de ID es la primera
                self.db.commit()
                cur.close()
                #self.db.close()
                cur = self.db.cursor()
                cur.execute("SELECT * FROM projects")
                records_project = cur.fetchall()
                #print(records_project)
                self.projectManager.tblwProjects.setRowCount(len(records_project))
                self.projectManager.tblwProjects.setColumnCount(len(records_project[0]))
                # Insertar los datos en el tableWidgget
                for i, row in enumerate(records_project):
                    for j, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        self.projectManager.tblwProjects.setItem(i, j, item)
                self.db.commit()
                cur.close()
                self.db.close()
                self.editProject.txtID.clear()
                self.editProject.txtUser.clear()
                self.editProject.txtNameProject.clear()
                self.editProject.txtDate.clear()
                self.editProject.txtDescription.clear()
                self.editProject.close()

##################################### ELIMNAR PROYECTOS ####################################

    def DeleteExistingProject(self):
        self.selected_row_ = self.projectManager.tblwProjects.currentRow()
        if self.selected_row_ != -1:
            self.deleteProject.btnDelete.clicked.connect(self.DeleteProject)
            self.deleteProject.btnNoDelete.clicked.connect(self.deleteProject.close)
            self.deleteProject.show()
        else:
            self.noProjectSelected.show()

    def DeleteProject(self):
        conection_ = con.Conexion()
        self.db = conection_.Connect()
        cur = self.db.cursor()
        cur.execute("USE LANGPROBE_DB")
        cur.close()
        cur = self.db.cursor()                    
        row_values = [self.projectManager.tblwProjects.item(self.selected_row_, column).text() for column in range(self.projectManager.tblwProjects.columnCount())]
        sql_delete = "DELETE FROM projects WHERE `ID del proyecto` = %s"
        cur.execute(sql_delete, [row_values[0]])
        self.db.commit()
        cur.close()
        
        cur = self.db.cursor()
        cur.execute("SELECT * FROM projects")
        records_project = cur.fetchall()
        #print(records_project)
        self.projectManager.tblwProjects.setRowCount(len(records_project))
        self.projectManager.tblwProjects.setColumnCount(len(records_project[0]))
        # Insertar los datos en el tableWidgget
        for i, row in enumerate(records_project):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.projectManager.tblwProjects.setItem(i, j, item)
        self.db.commit()
        self.db.close()
        self.deleteProject.close()

###################################### FILTRAR MEDIDAS ####################################

    def filterForUsers(self):
        
        conection_ = con.Conexion()
        self.db = conection_.Connect()
        cur = self.db.cursor()
        cur.execute("USE LANGPROBE_DB")
        cur.close() 
        cur = self.db.cursor()
        cur.execute("SELECT Usuario FROM projects")
        records_users = cur.fetchall()
        self.projectManager.dpwComboBox.clear()
        self.projectManager.dpwComboBox.addItem("-----Seleccione un archivo-----")
        if records_users:
            for i in range(len(records_users)):
                self.projectManager.dpwComboBox.addItem(records_users[i][0])
        self.db.close()
        
    def FilterProjects(self):
        idValueFilter = self.projectManager.txtIdProject.text()
        userValueFilter =self.projectManager.dpwComboBox.currentText()
        #print(idValueFilter,userValueFilter)conection_ = con.Conexion()
        conection_ = con.Conexion()
        self.db = conection_.Connect()
        cur = self.db.cursor()
        cur.execute("USE LANGPROBE_DB")
        cur.close() 
        
        
        if idValueFilter:
            if userValueFilter != "-----Seleccione un archivo-----":
                cur = self.db.cursor()
                query = "SELECT * FROM projects WHERE `ID del proyecto` = %s AND Usuario = %s"
                cur.execute(query, [idValueFilter,userValueFilter])
                records_project = cur.fetchall()
                if records_project:
                #print(records_project)
                    self.projectManager.tblwProjects.setRowCount(len(records_project))
                    self.projectManager.tblwProjects.setColumnCount(len(records_project[0]))
                    # Insertar los datos en el tableWidgget
                    for i, row in enumerate(records_project):
                        for j, value in enumerate(row):
                            item = QTableWidgetItem(str(value))
                            self.projectManager.tblwProjects.setItem(i, j, item)
                    self.db.commit()
                else:
                    self.projectManager.tblwProjects.clearContents()
                    self.projectManager.tblwProjects.setRowCount(0)
                cur.close()
                # Consultar con el texto de ambos campos
            else:
                cur = self.db.cursor()
                query = "SELECT * FROM projects WHERE `ID del proyecto` = %s"
                cur.execute(query, [idValueFilter])
                records_project = cur.fetchall()
                #print(records_project)
                self.projectManager.tblwProjects.setRowCount(len(records_project))
                self.projectManager.tblwProjects.setColumnCount(len(records_project[0]))
                # Insertar los datos en el tableWidgget
                for i, row in enumerate(records_project):
                    for j, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        self.projectManager.tblwProjects.setItem(i, j, item)
                self.db.commit()
                cur.close()
                # Consultar solo con idValueFilter    
        else:
            if userValueFilter != "-----Seleccione un archivo-----":
                cur = self.db.cursor()
                query = "SELECT * FROM projects WHERE Usuario = %s"
                cur.execute(query, [userValueFilter])
                records_project = cur.fetchall()
                #print(records_project)
                self.projectManager.tblwProjects.setRowCount(len(records_project))
                self.projectManager.tblwProjects.setColumnCount(len(records_project[0]))
                # Insertar los datos en el tableWidgget
                for i, row in enumerate(records_project):
                    for j, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        self.projectManager.tblwProjects.setItem(i, j, item)
                self.db.commit()
                cur.close()
                # Consultar solo con userValueFilter
            else:
                cur = self.db.cursor()
                cur.execute("SELECT * FROM projects")
                records_project = cur.fetchall()
                #print(records_project)
                self.projectManager.tblwProjects.setRowCount(len(records_project))
                self.projectManager.tblwProjects.setColumnCount(len(records_project[0]))
                # Insertar los datos en el tableWidgget
                for i, row in enumerate(records_project):
                    for j, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        self.projectManager.tblwProjects.setItem(i, j, item)
                self.db.commit()
                cur.close()
                
        self.db.close()

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        
###################################### INGRESAR MEDIDAS ####################################

    def OpenSaveDataWindow(self):
        self.saveData.show()
        ######################### CREACIÓN DE LAS TABLAS DE DATOS #########################
        conection_ = con.Conexion() 
        self.db = conection_.Connect()
        cur = self.db.cursor()
        cur.execute("USE LANGPROBE_DB")
        cur.close()
        tables = langProbeTables()
        for table in tables:
            cur = self.db.cursor()                    
            cur.execute(table)
            cur.close()
        self.db.close()
        #####################################################
        self.saveData.dpwComboBox.clear()
        self.saveData.dpwComboBox.addItem("------SELECCIONE UN PROYECTO------")
        conection_ = con.Conexion()
        self.db = conection_.Connect()
        cur = self.db.cursor()
        cur.execute("USE LANGPROBE_DB")
        cur.close() 
        cur = self.db.cursor()
        cur.execute("SELECT `Nombre del proyecto` FROM projects WHERE Usuario = %s", [self.mainUser])
        records_project = cur.fetchall()
        if records_project:
            for project in records_project:
                self.saveData.dpwComboBox.addItem(project[0])
        cur.close()
        self.db.close()
        
        #####################################################
        self.saveData.btnOpenExplorer.clicked.connect(self.OpenExplorer)
        self.saveData.btnModifiedPreData.clicked.connect(self.ModifiedPreData)
        self.saveData.btnChargeDataBase.clicked.connect(self.ChargeDataBase)
        
        meta_method_RawData = self.saveData.ltwRawData.metaObject().method(self.saveData.ltwRawData.metaObject().indexOfMethod("currentIndexChanged(int)"))
        is_conected_RawData = self.saveData.ltwRawData.isSignalConnected(meta_method_RawData)
        if is_conected_RawData:
            self.saveData.ltwRawData.itemSelectionChanged.disconnect(self.SelectedProjectRawData)
        self.saveData.ltwRawData.itemSelectionChanged.connect(self.SelectedProjectRawData)
            
        meta_method_PreData = self.saveData.ltwPreData.metaObject().method(self.saveData.ltwPreData.metaObject().indexOfMethod("currentIndexChanged(int)"))
        is_conected_PreData = self.saveData.ltwPreData.isSignalConnected(meta_method_PreData)
        if is_conected_PreData:
            self.saveData.ltwPreData.itemSelectionChanged.disconnect(self.SelectedProjectPreData)
        self.saveData.ltwPreData.itemSelectionChanged.connect(self.SelectedProjectPreData)
        
        self.itemselectedRaw = None
        self.itemselectedPre = None
        self.root_directory = None
        self.dicData = {}
        self.dfListDataIV = []
        self.dfListDataParameters = []
        self.dfListDataSettings = []
        self.dfListDataExtra = []
        self.globaltableParameter = pd.DataFrame()
        self.globaltableSettings = pd.DataFrame()
        self.globaltableDataExtra = pd.DataFrame()
        self.saveData.btnPreModified.clicked.connect(self.ModifiedRawData)
        self.saveData.btnUploadToDataBase.clicked.connect(self.UploadToDataBase)

    ############################# EXPLORADOR DE ARCHIVOS ###################################
    
    def SelectedProjectRawData(self):
        indexes = self.saveData.ltwRawData.selectedIndexes()
        if indexes:
            index = indexes[0]
            self.indexInt= indexes[0].row()
            self.itemselectedRaw = self.saveData.ltwRawData.itemFromIndex(index).text()
            # Borrar lo que hay en los campos
        self.saveData.txtNameFile.setText("")
        self.saveData.txtDescription.setText("")
        self.saveData.txtComment.setText("")
    
    def SelectedProjectPreData(self):
        indexes = self.saveData.ltwPreData.selectedIndexes()
        if indexes:
            index = indexes[0]
            #self.indexInt= indexes[0].row()
            self.itemselectedPre = self.saveData.ltwPreData.itemFromIndex(index).text()
            # Borrar lo que hay en los campos
        self.saveData.txtNameFile.setText(self.dfListDataExtra[self.dicData[self.itemselectedPre]].iloc[3,1])
        self.saveData.txtDescription.setText(self.dfListDataExtra[self.dicData[self.itemselectedPre]].iloc[4,1])
        self.saveData.txtComment.setText(self.dfListDataExtra[self.dicData[self.itemselectedPre]].iloc[5,1])
            
    def ModifiedRawData(self):
        if self.itemselectedRaw:
            name_file = self.saveData.txtNameFile.text()
            description = self.saveData.txtDescription.text()
            comment = self.saveData.txtComment.text()
            if name_file and description and comment:
                preDfProject = return_all_data(self.root_directory + "/" + self.itemselectedRaw,name_file,description,comment)
                self.dfListDataParameters.append(preDfProject[1])
                self.dfListDataSettings.append(preDfProject[2])
                self.dfListDataExtra.append(preDfProject[3])
                self.saveData.txtNameFile.setText("")
                self.saveData.txtDescription.setText("")
                self.saveData.txtComment.setText("")
                #################### DICCIONARIO ############################
                self.dicData[self.itemselectedRaw] = len(self.dfListDataParameters) - 1
                ##############################################################
                print(self.dicData)
                print(self.dfListDataExtra[self.dicData[self.itemselectedRaw]])
                self.saveData.ltwRawData.itemSelectionChanged.disconnect(self.SelectedProjectRawData)
                selectedValue = self.saveData.ltwRawData.takeItem(self.indexInt)
                self.saveData.ltwPreData.addItem(selectedValue)
                self.saveData.ltwRawData.clearSelection()
                self.saveData.ltwRawData.itemSelectionChanged.connect(self.SelectedProjectRawData)
                self.itemselectedRaw = None
            else:
                self.noData.show()  
        else:
            print("Ningún archivo seleccionado")
            
    def UploadToDataBase(self):
        # Transponer los df y agregarlos a los 4 df's globales    
        if self.itemselectedPre:
            
            dfParameter = self.dfListDataParameters[self.dicData[self.itemselectedPre]]
            dfSettings = self.dfListDataSettings[self.dicData[self.itemselectedPre]]
            dfDataExtra = self.dfListDataExtra[self.dicData[self.itemselectedPre]]
            vecParameter = []
            vecSettings = []
            vecDataExtra = []
            
            for df, vec in zip([dfParameter,dfSettings,dfDataExtra],[vecParameter,vecSettings,vecDataExtra]):
                for i in range(df.shape[1]):
                    Column = df.iloc[:,i].values
                    vec.append(Column)
            
            transposeTables = df_all_data_function(vecParameter, vecSettings, vecDataExtra)
            
            dfConcatParameter = pd.concat([self.additionalColumnID,transposeTables[0]], axis=1)
            dfConcatSettings = pd.concat([self.additionalColumnID,transposeTables[1]], axis=1)
            dfConcatDataExtra = pd.concat([self.additionalColumnID,transposeTables[2]], axis=1)
            self.globaltableParameter = pd.concat([self.globaltableParameter,dfConcatParameter], ignore_index=True)
            self.globaltableSettings = pd.concat([self.globaltableSettings,dfConcatSettings], ignore_index=True)
            self.globaltableDataExtra = pd.concat([self.globaltableDataExtra,dfConcatDataExtra], ignore_index=True)
            print(self.globaltableSettings)
            self.saveData.ltwPreData.itemSelectionChanged.disconnect(self.SelectedProjectPreData)
            selectedValue = self.saveData.ltwPreData.takeItem(self.indexInt)
            self.saveData.ltwFinalData.addItem(selectedValue)
            self.saveData.ltwPreData.clearSelection()
            self.saveData.ltwPreData.itemSelectionChanged.connect(self.SelectedProjectPreData)
            self.itemselectedPre = None
        pass
    
    def OpenExplorer(self):
        #self.saveData.dpwComboBox.currentIndexChanged.disconnect(self.SelectionValue)
        self.selectedProject = self.saveData.dpwComboBox.currentText()
        if self.selectedProject != "------SELECCIONE UN PROYECTO------":
            file_dialog = QFileDialog()
            self.root_directory = file_dialog.getExistingDirectory(None, 'Seleccionar Carpeta')
            if self.root_directory:
                listFiles = os.listdir(self.root_directory)
                for file in listFiles:
                    self.saveData.ltwRawData.addItem(file)
            self.additionalColumnID = pd.DataFrame({'ID del proyecto': [self.selectedProject]})
        else:
            self.noProjectSelected.show()
        #self.AddData()
        
    def ModifiedPreData(self):
        if self.itemselectedPre:
            self.dfListDataExtra[self.dicData[self.itemselectedPre]].iloc[3,1] = self.saveData.txtNameFile.text()
            self.dfListDataExtra[self.dicData[self.itemselectedPre]].iloc[4,1] = self.saveData.txtDescription.text()
            self.dfListDataExtra[self.dicData[self.itemselectedPre]].iloc[5,1] = self.saveData.txtComment.text()
            #print(self.dfListDataExtra[self.dicData[self.itemselectedPre]])
        else:
            print("Ningún archivo seleccionado")
    
    def ChargeDataBase(self):
        if self.saveData.ltwRawData.count() == 0 and self.saveData.ltwPreData.count() == 0:
            items_ltwFinalData = [self.saveData.ltwFinalData.item(i).text() for i in range(self.saveData.ltwFinalData.count())]
            if all(label in self.dicData for label in items_ltwFinalData):                 
                conection_ = con.Conexion()                     
                self.db = conection_.Connect()
                cur = self.db.cursor()
                cur.execute("USE LANGPROBE_DB")
                cur.close()                    
                ############### SUBIMOS LA TABLA PARAMETERS ##################
                cur = self.db.cursor()
                tableNameParameters = "dataparameters"
                columnsParameters = ','.join([f"`{element}`" for element in self.globaltableParameter.columns])
                placeholdersParameters = ','.join(['%s']*len(self.globaltableParameter.columns))
                sql_query_Parameters = f"INSERT INTO {tableNameParameters} ({columnsParameters}) VALUES ({placeholdersParameters})"
                valuesParameters = [tuple(v) for v in self.globaltableParameter.values]
                for record in valuesParameters:
                    cur.execute(sql_query_Parameters,record)
                    self.db.commit()
                
                cur.close()
                ############### SUBIMOS LA TABLA SETTINGS ##################
                cur = self.db.cursor()
                tableNameSettings = "datasettings"
                columnsSettings = ','.join([f"`{element}`" for element in self.globaltableSettings.columns])
                placeholdersSettings = ','.join(['%s']*len(self.globaltableSettings.columns))
                sql_query_Settings = f"INSERT INTO {tableNameSettings} ({columnsSettings}) VALUES ({placeholdersSettings})"
                valuesSettings = [tuple(v) for v in self.globaltableSettings.values]
                for record in valuesSettings:
                    cur.execute(sql_query_Settings,record)
                    self.db.commit()
                
                cur.close()
                ############### SUBIMOS LA TABLA DATAEXTRA ##################
                cur = self.db.cursor()
                tableNameDataExtra = "dataextra"
                columnsDataExtra = ','.join([f"`{element}`" for element in self.globaltableDataExtra.columns])
                placeholdersDataExtra = ','.join(['%s']*len(self.globaltableDataExtra.columns))
                sql_query_DataExtra = f"INSERT INTO {tableNameDataExtra} ({columnsDataExtra}) VALUES ({placeholdersDataExtra})"
                valuesDataExtra = [tuple(v) for v in self.globaltableDataExtra.values]
                for record in valuesDataExtra:
                    cur.execute(sql_query_DataExtra,record)
                    self.db.commit()
                
                cur.close()
                #############################################################
                self.db.close()
                self.successfulChargeDataBase.show()
                self.saveData.ltwFinalData.clear()
                self.saveData.close()
            else:
                self.missingUploadFiles.show()
        else:
            self.incompleteLoadData.show()
    