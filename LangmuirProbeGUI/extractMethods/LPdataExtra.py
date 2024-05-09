
def extract_extradata_from_ldf(root_extract,name_file,description,comment):
    
    extra_data_list = []
    extra_value_list = []
    
    with open(root_extract, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
        for i in range(3): # 3: total extra data
            line = lines[4+i].split("<")
            line = ''.join(line).split(">")
            extra_name = line[0].strip()
            extra_data_list.append(extra_name)
            
            if line[1].split("/")[0].isdigit():
                extra_value = float(line[1].split("/")[0])
                extra_value_list.append(extra_value)
                
            else:
                extra_value = line[1].split("/")[0].strip()
                extra_value_list.append(extra_value)
                
    extra_information = ['Name file', 'Description', 'Comment']
    extra_value_information = [name_file, description, comment]
    extra_data_list = extra_data_list + extra_information
    extra_value_list = extra_value_list + extra_value_information
    
    return [extra_data_list, extra_value_list]