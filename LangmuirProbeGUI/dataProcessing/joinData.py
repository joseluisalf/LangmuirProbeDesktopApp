
import pandas as pd
import os

from returnTransposeData import df_all_data_function


def concat_all_files_data(root_directory):

    # Lista para almacenar los archivos con la extensión .ldf
    files_ldf = []

    # Iterar sobre los archivos en la carpeta
    for file in os.listdir(root_directory):
        if file.endswith('.ldf'):
            # Agregar el nombre del archivo a la lista
            files_ldf.append(file)

    return files_ldf

def data_table(root_directory):

    files_ldf = concat_all_files_data(root_directory)

    df0 = df_all_data_function(root_directory + "/" + files_ldf[0])[1] # modificar el [1] al final por si se quiere unir datos de otras tablas
    for i in range(1,len(files_ldf)):
        root = root_directory + "/" + files_ldf[i]
        df = df_all_data_function(root)[1]
        df0 = pd.concat([df0, df], ignore_index = True)
        
    return df0