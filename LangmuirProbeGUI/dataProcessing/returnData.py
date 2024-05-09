
import pandas as pd

from extractMethods.LPdataExtra import extract_extradata_from_ldf
from extractMethods.LPdataIV import extract_data_from_ldf
from extractMethods.LPdataParameters import extract_parameters_from_ldf
from extractMethods.LPdataSettings import extract_settings_from_ldf

#####################################################################################################
def return_all_data(root_extract,name_file,description,comment):

    data_iv_ = extract_data_from_ldf(root_extract)
    data_parameters_ = extract_parameters_from_ldf(root_extract)
    data_settings_ = extract_settings_from_ldf(root_extract)
    data_extra_ = extract_extradata_from_ldf(root_extract,name_file,description,comment)
    
    data_IV = pd.DataFrame({'Voltage': data_iv_[0],     
                            'Current': data_iv_[1], 
                            'std Voltage': data_iv_[2], 
                            'std Current': data_iv_[3]})
    
    data_parameters = pd.DataFrame({'Parameters': data_parameters_[0], 
                                    'Unit': data_parameters_[1], 
                                    'Value': data_parameters_[2], 
                                    'Error': data_parameters_[3]})
    
    data_settings = pd.DataFrame({'Setting': data_settings_[0], 
                                  'Unit': data_settings_[1],
                                  'Value': data_settings_[2]})
    
    data_extra = pd.DataFrame({'Extra data': data_extra_[0], 
                               'Value': data_extra_[1]})
    
    return [data_IV, data_parameters, data_settings, data_extra]