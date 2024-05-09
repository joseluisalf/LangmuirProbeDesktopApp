
import pandas as pd

#from extractMethods.LPdataExtra import extract_extradata_from_ldf
#from extractMethods.LPdataParameters import extract_parameters_from_ldf
#from extractMethods.LPdataSettings import extract_settings_from_ldf


def df_all_data_function(tb1,tb2,tb3):

    #tb1 = extract_parameters_from_ldf(root)
    #tb2 = extract_settings_from_ldf(root)
    #tb3 = extract_extradata_from_ldf(root)
    
    # este código es para los parámetros y las configuraciones (a esta ultima falta agregar unidades)
    def aux_function(aux_list):   
        value_list = aux_list[0]
        unit_list = aux_list[1]
        value_plus_unit_list =[]
        for i in range(len(unit_list)):
            if unit_list[i] != None:
                #value_list[i]
                value_plus_unit_list.append(value_list[i] + " " + unit_list[i])
            else:
                value_plus_unit_list.append(value_list[i])
        return value_plus_unit_list 

    # Codigo para unir las etiquetas de los parametros, configuraciones, e informacion extra, asi como tambien todos los valores

    #label_list = aux_function(tb1)+ aux_function(tb2) + tb3[0]
    #values_list = tb1[2] + tb2[2] + tb3[1]
    #data_df0 = pd.DataFrame([values_list],columns=label_list)
    data_df1 = pd.DataFrame([tb1[2]],columns=aux_function(tb1))
    data_df2 = pd.DataFrame([tb2[2]],columns=aux_function(tb2))
    data_df3 = pd.DataFrame([tb3[1]],columns=tb3[0])
    #return [data_df0, data_df1, data_df2, data_df3]
    return [data_df1, data_df2, data_df3]