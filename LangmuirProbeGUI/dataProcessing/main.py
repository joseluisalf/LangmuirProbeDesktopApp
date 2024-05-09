
from joinData import data_table
from returnData import return_all_data
from returnTransposeData import df_all_data_function


root = "testFiles/20W.ldf"
root_files = "testFiles"

#all_data = return_all_data(root)
#print(all_data[0])

data__ = df_all_data_function(root)
print(data__[1])

#dat = data_table(root_files)
#print(dat)