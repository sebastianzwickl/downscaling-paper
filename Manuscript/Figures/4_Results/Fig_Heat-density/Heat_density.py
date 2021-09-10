import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pyam as py
import numpy as np

c_heat_density = "#284E78"
c_background = "#FF96AD"
c_edge = "#161616"

plt.style.use("ggplot")

fig, ax = plt.subplots()
val_pop=1.17
val_seq=1.86
val_ite=5.11
#ax.bar(x=3.75, height=2.58-0.43, bottom=0.43, width=0.2, alpha=0.9, color=c_heat_density, edgecolor="black", linewidth=0)
values = [val_pop, val_seq-val_pop, 5.11-val_seq, 10-5.11]
bars = ax.bar(x=[1,2,3,3.5], height=values, bottom=[0, val_pop, val_seq, 5.11], width=[0.8,0.8,0.8,0.2], color=[c_heat_density,c_heat_density,c_heat_density,c_background], edgecolor="black", linewidth=[0.5, 0.5, 0.5, 1])

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



ax.text(x=2, y=8.75, s='Gap of heat density between\n2050\'s and today\'s centralized heat networks\n(Societal Commitment scenario)',
        rotation=0, fontsize=7, color='#000000',
        ha='center', va='center', bbox=dict(facecolor="#FFF5FD", edgecolor=c_background, boxstyle='round,pad=1', linestyle='solid',
                                              linewidth=2.), zorder=100)

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

ax.text(x=1.4, y=3.35, s='Prioritized preferences\nof heat sources', rotation=10, fontsize=7, color='#2C394B',
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

ax.text(x=2.35, y=6, s='Network topology\nbenchmarking & reallocation', rotation=30, fontsize=7, color='#2C394B',
          ha='center', va='center')



ax.set_xticks([1,2,3])
ax.set_xticklabels(["Population-based\ndownscaling", "Sequential\ndownscaling", "Iterative\ndownscaling"], fontsize=7)

ax.xaxis.set_tick_params(labelsize=10, rotation=0)
ax.yaxis.set_tick_params(labelsize=10, rotation=0)
ax.set_ylabel("Heat density "+r"in $\frac{GWh}{km^2}$", labelpad=-5, fontsize=10)
ax.set_xlim([0.5,3.7])

from matplotlib.lines import Line2D
_patches = []
_line = Line2D([1], [2], label = "Minimum heat density of today\'s\ncentralized heat networks\nwith 90% connection rate",color=c_edge, linewidth=2, marker="o", markersize=6, markeredgecolor=c_edge, markeredgewidth=0, linestyle="solid")
_patches.extend([_line])
_line = Line2D([0], [0], label = "Heat density of centralized\nheat network 2050\n(Techno-Friendly scenario)",color=c_heat_density, linewidth=6)
_patches.extend([_line])



# _patches = []
# _line = Line2D([0], [0], label = "2020\'s values (reference year)",color="black", linewidth=3)
# _patches.extend([_line])
# _patches.append(mpatches.Patch(facecolor='#FF4C29', label='Total demand', edgecolor="#52734D", linewidth=0.75, hatch="/////"))
# _patches.append(mpatches.Patch(facecolor='#93D9A3', label='Increasing generation', edgecolor="#52734D", linewidth=0.75))
# _patches.append(mpatches.Patch(facecolor='#FF4C29', label='Decreasing generation', edgecolor="#9C3D54", linewidth=0.75))

# DT = 8.0
# GD = 8.5
# SC = 8.6
# TF = 7.4

# ax.fill_between(x=[3.625+0.015,3.625-0.015],y1=1.4, y2=2.6, color="gray", alpha=0.8)
# ax.plot(3.625, 1.4, marker="H", markersize=4, color="black")
# ax.plot(3.625, 2.6, marker="*", markersize=6, color="black")
# ax.plot(3.625, 1.5, marker="v", markersize=4, color="black")
# ax.plot(3.625, 2.0, marker="d", markersize=4, color="black")

# ax.fill_between(x=[3.625+0.015,3.625-0.015],y1=1.4, y2=2.6, color="gray", alpha=0.8)
# ax.plot(3.625, 1.4, marker="H", markersize=4, color="black")
# ax.plot(3.625, 2.6, marker="*", markersize=6, color="black")
# ax.plot(3.625, 1.5, marker="v", markersize=4, color="black")
# ax.plot(3.625, 2.0, marker="d", markersize=4, color="black")


# "v" = "Gradual Development"
# "H" = Societal Commitment
# "*" = "Techno-Friendly"
# "d" = Direct-Transition



leg = ax.legend(handles=_patches, loc='upper left', fontsize=6.5, framealpha=1, handlelength=1, handletextpad=1, borderpad=1, columnspacing=1, edgecolor=c_edge, frameon=True, bbox_to_anchor=(0.01, 0.725))
leg.get_frame().set_linewidth(0.25)

ax.set_title("Heat density of the centralized heat network in Graz (AT221) 2050\nobtained by different downscaling techniques", fontsize=12)

# ax2 = ax.twinx()
# ax2.get_yaxis().set_visible(False)
# _patches = []
# _line = Line2D([0], [0], label = "Difference of heat density gap\nbetween scenarios",color="gray", linewidth=3)
# _patches.extend([_line])
# _line = Line2D([0], [0], label = "Directed Transition",color="black", marker="d", markersize=3, linewidth=0)
# _patches.extend([_line])
# _line = Line2D([0], [0], label = "Societal Commitment",color="black", marker="H", markersize=3, linewidth=0)
# _patches.extend([_line])
# _line = Line2D([0], [0], label = "Techno-Friendly",color="black", marker="*", markersize=4, linewidth=0)
# _patches.extend([_line])
# _line = Line2D([0], [0], label = "Gradual Development",color="black", marker="v", markersize=3, linewidth=0)
# _patches.extend([_line])
# leg2 = ax2.legend(handles=_patches, loc="center left", fontsize=6.5, framealpha=1, handlelength=0.5, handletextpad=0.5, frameon=True, fancybox=True, shadow=False, edgecolor="black", bbox_to_anchor=(0.01, 0.475))
# leg2.get_frame().set_linewidth(0.25)

# ax.annotate(
#     '',
#     fontsize=0,
#     color="red",
#     multialignment='center',
#     xy=(3.625, 1.25), xycoords='data',
#     xytext=(3.45, 0.6), textcoords='data',
#     arrowprops=dict(headlength=4, 
#                     headwidth=2,
#                     width=0.15,
#                     connectionstyle="arc3,rad=.3",
#                     color="#000000"))

# ax.text(x=3.1, y=0.5, s='Largest gap in the\nSocietal Commitment scenario', rotation=0, fontsize=7, color='#000000',
#           ha='center', va='center')

plt.tight_layout()

fig.savefig("HD_cleaned1.png", dpi=500)
fig.savefig("HD_cleaned1.eps", format="eps")