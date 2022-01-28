import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pyam as py
import numpy as np

c_heat_density = "#284E78"
c_background = "#FF96AD"
c_edge = "#161616"

plt.style.use("ggplot")

fig, ax = plt.subplots()
val_pop=0.55
val_seq=1.04
val_ite=4.71
#ax.bar(x=3.75, height=2.58-0.43, bottom=0.43, width=0.2, alpha=0.9, color=c_heat_density, edgecolor="black", linewidth=0)
values = [val_pop, val_seq-val_pop, val_ite-val_seq, 10-val_ite]
bars = ax.bar(x=[1,2,3,3.5], height=values, bottom=[0, val_pop, val_seq, val_ite], width=[0.8,0.8,0.8,0.2], color=[c_heat_density,c_heat_density,c_heat_density,c_background], edgecolor="black", linewidth=[0.5, 0.5, 0.5, 1])

# plt.rcParams.update({'hatch.color': '#B2B1B9'})
plt.rcParams['hatch.linewidth'] = 1
bars[3].set_hatch('//')
bars[3].set_edgecolor('#FFF5FD')


height = [val_pop, val_seq, val_ite]

_red = [0, val_pop, 1.5]

for i, v in enumerate(height):
    ax.text(i+1, v+0.25, str(np.round(v-_red[i],2)), color=c_heat_density, ha="center", va="center", fontsize=10)

ax.plot([1.4, 1.6], 2*[val_pop], linestyle="--", linewidth=1, color="gray")
ax.plot([2.4, 2.6], 2*[val_seq], linestyle="--", linewidth=1, color="gray")
#ax.plot([3.4, 3.6], 2*[2.58], linestyle="--", linewidth=1, color="gray")

#ax.plot([2.35, 3.65], 2*[0.43], linestyle="--", linewidth=1, color="gray")

ax.plot([1, 2,3,3.5], 4*[10], linestyle="dashed", linewidth=2, color="#161616", marker="o", markersize=6)
# ax.add_patch(Rectangle((1, 10), 2.5, 1, fill=True, hatch="//", edgecolor=c_heat_density, alpha=0.5))
#ax.fill_between(x=[1,2,3,3.5], y1=10, y2=11, color="black", alpha=0.1, linewidth=0)



ax.text(x=2, y=8.75, s='Gap of heat density between 2050\'s\nand today\'s district heating',
        rotation=0, fontsize=7, color='#000000',
        ha='center', va='center', bbox=dict(facecolor="#FFF5FD", edgecolor=c_background, boxstyle='round,pad=1', linestyle='solid',
                                              linewidth=1.), zorder=100)

ax.annotate(
    '',
    fontsize=0,
    color="red",
    multialignment='center',
    xy=(3.5, 7.5), xycoords='data',
    xytext=(2.5, 8.75), textcoords='data',
    arrowprops=dict(headlength=8, 
                    headwidth=4,
                    width=0.75,
                    connectionstyle="arc3,rad=-.2",
                    color="#000000"))





ax.annotate(
    '',
    fontsize=0,
    color="red",
    multialignment='center',
    xy=(2, val_seq+0.8), xycoords='data',
    xytext=(1, val_pop+0.8), textcoords='data',
    arrowprops=dict(headlength=8, 
                    headwidth=4,
                    width=0.5,
                    connectionstyle="arc3,rad=-.2",
                    color="#2C394B"))

ax.text(x=1.5, y=2.8, s='Prioritized preferences\nof heat sources', rotation=5, fontsize=7, color='#2C394B',
          ha='center', va='center')


ax.annotate(
    '',
    fontsize=0,
    color="red",
    multialignment='center',
    xy=(3, val_ite+0.8), xycoords='data',
    xytext=(2, val_seq+0.8), textcoords='data',
    arrowprops=dict(headlength=8, 
                    headwidth=4,
                    width=0.5,
                    connectionstyle="arc3,rad=-.4",
                    color="#2C394B"))

ax.text(x=2.35, y=5.6, s='Network topology\nbenchmarking & reallocation', rotation=30, fontsize=7, color='#2C394B',
          ha='center', va='center')



ax.set_xticks([1,2,3])
ax.set_xticklabels(["Population-based\ndownscaling", "Sequential\ndownscaling", "Iterative\ndownscaling"], fontsize=7)

ax.xaxis.set_tick_params(labelsize=10, rotation=0)
ax.yaxis.set_tick_params(labelsize=10, rotation=0)
ax.set_ylabel("Heat density "+r"in $\frac{GWh}{km^2}$", labelpad=-5, fontsize=10)
ax.set_xlim([0.5,3.7])

from matplotlib.lines import Line2D
_patches = []
_line = Line2D([1], [2], label = "Minimum heat density of today\'s\ndistrict heating networks\nwith 90% connection rate",color=c_edge, linewidth=2, marker="o", markersize=6, markeredgecolor=c_edge, markeredgewidth=0, linestyle="solid")
_patches.extend([_line])
_line = Line2D([0], [0], label = "Heat density of district heating\nnetwork in 2050 (Techno-Friendly)",color=c_heat_density, linewidth=6)
_patches.extend([_line])


leg = ax.legend(handles=_patches, loc='upper left', fontsize=6.5, framealpha=1, handlelength=1, handletextpad=1, borderpad=1, columnspacing=1, edgecolor=c_edge, frameon=True, bbox_to_anchor=(0.01, 0.725))
leg.get_frame().set_linewidth(0.25)

ax.set_title("Heat density of district heating in Linz-Wels (AT312) in 2050\nobtained by different downscaling techniques", fontsize=12)


plt.tight_layout()

fig.savefig("HD_cleaned1.png", dpi=500)
fig.savefig("HD_cleaned1.eps", format="eps")