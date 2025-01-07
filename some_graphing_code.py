import seaborn as sns

sns.set_style("darkgrid")
fig = plt.figure()

axes = fig.add_subplot(111)
# =============================================================================
# axes.errorbar(data[:, 0], data[:, 1], yerr=data[:, 2], fmt='o',
#             markersize=3, label='Measured data',
#             alpha=0.85, color='grey')
# axes.plot(x_values, sigma_equation(result[0], x_values, "fitting"),
#         color='orangered', label='fitted curve')
# axes.set_xlabel('Centre-of-mass Energy (GeV)', fontsize=14)
# axes.set_ylabel(r'$\sigma$(nb)', fontsize=14)
# # axes.scatter(result[0][0], result[1], label='Maxima', color='b')
# =============================================================================
plt.legend(loc='bottom left', shadow=True, edgecolor='slategray')

# =============================================================================
# axes.set_title(r'$m_z$ '+ f'= {result[0][0]:4.3e}'
#              + r"$\, \mathrm{GeV/c^2}, \,$"
#              + r'$\Gamma_z$' + f' = {result[0][1]:4.3e}'
#              + r"$\, \mathrm{GeV}$")
# =============================================================================

axes.grid('on')
axes.spines['right'].set_color((.6, .6, .6))
axes.spines['top'].set_color((.6, .6, .6))
axes.spines['left'].set_color((0, 0, 0))
axes.spines['bottom'].set_color((0, 0, 0))
plt.savefig('NAME.png', dpi=400)
plt.show()
plt.close()