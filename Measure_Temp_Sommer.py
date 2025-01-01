import os
import pathlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator
from matplotlib import cm
try:
    from ReadData import ReadData
except:
    print('Unable to import ReadData')
    exit()

folder = str(pathlib.Path(__file__).parent.resolve()) + r'/Data/Measure_Temp_Sommer/'
font = {'fontname':'Times New Roman'}

file_list = os.listdir(folder)
te_ti_E = []
for file in file_list:
    tau_e = float(file[1:5])
    tau_i = float(file[7:11])
    time, x, y, Energy = ReadData(folder + file, 'sommer')
    index_cutoff = round(len(x)*0.4)
    E_data = Energy[index_cutoff:]
    mean_E = np.mean(E_data)
    te_ti_E.append([tau_e, tau_i, mean_E])
    
te_ti_E = np.array(te_ti_E)

for data in te_ti_E:
    if data[0] == 5.0:
        plt.plot(data[1], data[2], 'x')

plt.show()

    