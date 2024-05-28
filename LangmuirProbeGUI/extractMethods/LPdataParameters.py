def extract_parameters_from_ldf(root_extract):

    def extract_number(line):

        i_0 = 0
        i_f = 0
        line_aux = line[13:-1]
        for i in range(len(line_aux)):
            if line_aux[i] =='>':
                i_0 = i
            if line_aux[i] == '<':
                i_f = i
        if line_aux[i_0+1:i_f] == "nan":
            number = "nan"
        else:
            number = float(line_aux[i_0+1:i_f])
        return number
    
    def extract_name(line):

        i_0 = 0
        i_f = 0
        line_aux = line[12:]
        for i in range(len(line_aux)):
            if line_aux[i] =='<':
                i_0 = i
            if line_aux[i] == '>':
                i_f = i
                break
        name = line_aux[i_0+1:i_f]
        return name

    parameters_name = []
    parameters_unit = ["[A/m^2]","[A/m^2]","[µm]","[m^-3]","[m^-3]","[V]","[V]","[V]","[V]","[eV]","[m^-3]","[eV]","[mA]","[eV]"]
    parameters_value = []
    parameters_error = []
    aux_1 = 0
    i=0

    find = "            <Je"
    with open(root_extract, 'r', encoding='utf-8') as infile:
        for line in infile:
            if i == 14:
                break
            if aux_1 == 0:
                line_aux = line.rstrip().split(">")
                if find in line_aux:
                    parameters_name.append(extract_name(line.rstrip("\n")))
                    parameters_value.append(extract_number(line.rstrip("\n")))
                    aux_1 = 1
            elif aux_1 == 1:
                parameters_error.append(extract_number(line.rstrip("\n")))
                i += 1
                aux_1 = 2
            else:
                parameters_name.append(extract_name(line.rstrip("\n")))
                parameters_value.append(extract_number(line.rstrip("\n")))
                aux_1 = 1

    parameters_value = [float(pv) for pv in parameters_value]

    return [parameters_name, parameters_unit, parameters_value, parameters_error]