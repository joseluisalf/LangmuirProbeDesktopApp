def extract_data_from_ldf(root_extract):

    data_i = []
    data_v = []
    data_std_i = []
    data_std_v = []

    aux_1 = 0
    aux_2 = 0
    aux_3 = 0
    aux_4 = 0
    find = "class=\"correctedData\">"
    
    with open(root_extract, 'r', encoding='utf-8') as infile:
        for line in infile:
            if aux_1==1:
                if aux_2==1:    
                    if aux_3==1: 
                        if aux_4==1:    
                            line = line.lstrip("            <vec label=\"stdV\">;")
                            line=line[:-8]
                            data_std_v.append(line)
                            break   
                        line = line.lstrip("            <vec label=\"stdI\">;")
                        line=line[:-8]
                        data_std_i.append(line)
                        aux_4 = 1 
                    if aux_3 == 0:
                        line = line.lstrip("            <vec label=\"V\">;")
                        line=line[:-8]
                        data_v.append(line)
                        aux_3 = 1
                if aux_2 == 0:
                    line = line.lstrip("            <vec label=\"I\">;")
                    line=line[:-8]
                    aux_2 = 1
                    data_i.append(line)
            if aux_1 == 0:
                line = line.rstrip().split(" ")
                if find in line:
                    aux_1 = 1
    datai_ = [float(i) for i in data_i[0].split(";")]
    datav_ = [float(v) for v in data_v[0].split(";")]
    datastdi_ = [float(stdi) for stdi in data_std_i[0].split(";")]
    datastdv =  [float(stdv) for stdv in data_std_v[0].split(";")]

    return [datai_, datav_, datastdi_, datastdv]