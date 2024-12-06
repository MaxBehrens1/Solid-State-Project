import numpy as np

def ReadData(filename):
    xdata, ydata = np.loadtxt(filename, delimiter='\t', unpack = True, comments='&')
    return xdata, ydata
