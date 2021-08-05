import matplotlib.pyplot as plt
import pyam as py
import numpy as np

c_heat_density = "#284E78"
c_background = "#FF96AD"
c_edge = "#161616"

plt.style.use("ggplot")

fig, ax = plt.subplots()
#ax.bar(x=3.75, height=2.58-0.43, bottom=0.43, width=0.2, alpha=0.9, color=c_heat_density, edgecolor="black", linewidth=0)
values = [0.43, 1.5-0.43, 2.58-1.5, 10-2.58]
bars = ax.bar(x=[1,2,3,3.5], height=values, bottom=[0, 0.43, 1.5, 2.58], width=[0.8,0.8,0.8,0.2], color=[c_heat_density,c_heat_density,c_heat_density,c_background], edgecolor="black", linewidth=[0.5, 0.5, 0.5, 1])

# plt.rcParams.update({'hatch.color': '#B2B1B9'})
plt.rcParams['hatch.linewidth'] = 1
bars[3].set_hatch('//')
bars[3].set_edgecolor('#FFF5FD')


height = [0.43, 1.5, 2.58]



for i, v in enumerate(height):
    ax.text(i+1, v+0.25, str(np.round(v,2)), color='black', ha="center", va="center", fontsize=10)

ax.plot([1.4, 1.6], 2*[0.43], linestyle="--", linewidth=1, color="gray")
ax.plot([2.4, 2.6], 2*[1.5], linestyle="--", linewidth=1, color="gray")
#ax.plot([3.4, 3.6], 2*[2.58], linestyle="--", linewidth=1, color="gray")

#ax.plot([2.35, 3.65], 2*[0.43], linestyle="--", linewidth=1, color="gray")

ax.plot([1, 2,3,3.5], 4*[10], linestyle="dashed", linewidth=2, color="#161616", marker="d", markersize=6)




ax.text(x=1.95, y=8.25, s='Gap of heat density between 2050\'s and today\'s centralized heat networks',
        rotation=0, fontsize=8, color='#000000',
        ha='center', va='center', bbox=dict(facecolor="#FFF5FD", edgecolor=c_background, boxstyle='round,pad=1', linestyle='solid',
                                              linewidth=2.), zorder=100)

ax.annotate(
    '',
    fontsize=0,
    color="red",
    multialignment='center',
    xy=(3.5, 6), xycoords='data',
    xytext=(2., 7.7), textcoords='data',
    arrowprops=dict(headlength=8, 
                    headwidth=4,
                    width=0.75,
                    connectionstyle="arc3,rad=.2",
                    color="#000000"))





ax.annotate(
    '',
    fontsize=0,
    color="red",
    multialignment='center',
    xy=(2, 2.2), xycoords='data',
    xytext=(1, 1.1), textcoords='data',
    arrowprops=dict(headlength=8, 
                    headwidth=4,
                    width=0.5,
                    connectionstyle="arc3,rad=-.3",
                    color="#000000"))

ax.text(x=1.5, y=3.05, s='Prioritized preferences\nof heat sources', rotation=10, fontsize=7, color='#000000',
          ha='center', va='center')


ax.annotate(
    '',
    fontsize=0,
    color="red",
    multialignment='center',
    xy=(3, 3.3), xycoords='data',
    xytext=(2, 2.2), textcoords='data',
    arrowprops=dict(headlength=8, 
                    headwidth=4,
                    width=0.5,
                    connectionstyle="arc3,rad=-.3",
                    color="#000000"))

ax.text(x=2.5, y=4.2, s='Network topology\nbenchmarking & reallocation', rotation=10, fontsize=7, color='#000000',
          ha='center', va='center')



ax.set_xticks([1,2,3])
ax.set_xticklabels(["Population-based\ndownscaling", "Sequential\ndownscaling", "Iterative\ndownscaling"], fontsize=7)

ax.xaxis.set_tick_params(labelsize=10, rotation=0)
ax.yaxis.set_tick_params(labelsize=10, rotation=0)
ax.set_ylabel("Heat density "+r"in $\frac{GWh}{km^2}$", labelpad=-5, fontsize=10)
ax.set_xlim([0.5,3.7])

from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
_patches = []
_line = Line2D([1], [2], label = "Heat density of today\'s\ncentralized heat networks\nwith 90% connection rate",color=c_edge, linewidth=4, marker="d", markersize=8, markeredgecolor=c_edge, markeredgewidth=0, linestyle="--")
_patches.extend([_line])
_line = Line2D([0], [0], label = "Heat density of centralized\nheat network 2050",color=c_heat_density, linewidth=8)
_patches.extend([_line])



# _patches = []
# _line = Line2D([0], [0], label = "2020\'s values (reference year)",color="black", linewidth=3)
# _patches.extend([_line])
# _patches.append(mpatches.Patch(facecolor='#FF4C29', label='Total demand', edgecolor="#52734D", linewidth=0.75, hatch="/////"))
# _patches.append(mpatches.Patch(facecolor='#93D9A3', label='Increasing generation', edgecolor="#52734D", linewidth=0.75))
# _patches.append(mpatches.Patch(facecolor='#FF4C29', label='Decreasing generation', edgecolor="#9C3D54", linewidth=0.75))




ax.legend(handles=_patches, loc='center left', fontsize=8, framealpha=1, handlelength=1, handletextpad=1, borderpad=1, columnspacing=1, edgecolor=c_edge, frameon=True)
ax.set_title("Heat density of the centralized heat network in Graz (AT221) 2050\nobtained by different downscaling techniques", fontsize=12)

#ax.set_title("Heat density of centralized heat network 2050 and\ngap of heat density to today\'s networks "+r"in $\frac{GWh}{km^2}$")
plt.tight_layout()

fig.savefig("HD_cleaned1.png", dpi=500)
fig.savefig("HD_cleaned1.eps", format="eps")