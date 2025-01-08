import numpy as np
import matplotlib.pyplot as plt

x_data = np.linspace(0, 5, 1000)
mu = 1
T= 2# use T values from 0.1 to 3-4K for good results (this is a mock-up)
y_MB = np.exp(-(x_data-mu)/T)
y_FD = 1/(np.exp((x_data-mu)/T)+1)


ylabel = r'$\bar{n}$'

fig = plt.figure()
ax = fig.add_subplot(111)

ax.grid('on')
ax.spines['right'].set_color((.6, .6, .6))
ax.spines['top'].set_color((.6, .6, .6))
ax.spines['left'].set_color((0, 0, 0))
ax.spines['bottom'].set_color((0, 0, 0))

ax.plot(x_data, y_MB, label = "Maxwell-Boltzmann", color = 'orange')
ax.plot(x_data,y_FD, label = "Fermi-Dirac", color = 'blue')
ax.vlines(mu,0,5, ls='--', color = 'r', alpha = 0.7)
ax.text(mu+0.1, 3.5, f'μ = {mu}eV', color='r', fontsize='14')
ax.set_xlabel("Energy (eV)")
ax.set_ylabel(ylabel)
ax.set_title('Occupation Functions')
ax.set_ylim(0,5)
ax.legend()
plt.savefig("Graphs/hightempcomp.png", dpi=400)
plt.show()

