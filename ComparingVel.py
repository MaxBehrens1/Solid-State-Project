"""
sommer_file params:
Ex = 0.5e6
Ey = 0
Bz = 0
tau_i = inf
tau_e = 2

"""
try:
    from ReadData import ReadData
except:
    print('Unable to import ReadData')

sommer_file = r'/Users/maxbehrens/OneDrive - UAM/Solid State/Solid-State-Project/Data/sommer_basic.txt'
sommer_datax, sommer_datay = ReadData(filename=sommer_file)