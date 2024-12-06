import numpy as np

def ReadData(filename):
    xdata, ydata = np.loadtxt(filename, delimiter='\t', unpack = True, comments='&')
    return xdata, ydata

file = r'/Users/maxbehrens/OneDrive - UAM/Solid State/Solid-State-Project/Data/data_for_max.txt'
print(ReadData(filename=file))