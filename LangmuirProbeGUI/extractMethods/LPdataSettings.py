def extract_settings_from_ldf(root_extract):
                                                             
    setting_name_list = []
    setting_unit_list = [None,None,None,None,None,None,"[K]","[g/mol]",None,None,None,"[Torr]","[m]","[m]","[m]","[Ohm]","[V]",None,None,None]
    setting_value_list = []
    with open(root_extract, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
        for i in range(20): # 20: total settings
            line = lines[89+i].split("<")
            line = ''.join(line).split(">")
            setting_name = line[0].strip()
            setting_name_list.append(setting_name)
            
            if line[1].split("/")[0] !='nan':
                setting_value = float(line[1].split("/")[0])
                setting_value_list.append(setting_value)
                
            else:
                setting_value = line[1].split("/")[0]
                setting_value_list.append(setting_value)
                
    return [setting_name_list, setting_unit_list, setting_value_list]