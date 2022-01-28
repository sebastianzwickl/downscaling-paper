import matplotlib.pyplot as plt
import numpy as np
import pyam as py
import numpy as np


color={"Directed Transition": "#A2D2FF",
       "Societal Commitment": "#FF865E",
       "Gradual Development": "#C8C6C6",
       "Techno-Friendly":"#FEE440"}


c_edge = "#161616"

plt.style.use("seaborn-paper")
data = py.IamDataFrame("Compare-scenarios.xlsx")

scenario = data.data["information"]
plt.rcParams['hatch.linewidth'] = 0.75
fig, ax = plt.subplots()

figures = data.plot.bar(ax=ax, stacked=True, bars="scenario", x="region", legend=False)
for number, _patch in enumerate(figures.patches):
    _scenario = scenario[number]
    _color=color[_scenario]
    _patch.set_color(_color)
    
    if number >= len(scenario)/2:
        _patch.set_hatch("//")
        _patch.set_edgecolor("black")
    else:
        _patch.set_alpha(1)
        

ax.set_xlabel("")
ax.tick_params(axis='x', which='major', pad=2, rotation=0, labelsize=10)
ax.tick_params(axis='y', which='major', labelsize=10)
ax.set_xticklabels(labels=["Vienna (AT130)","Graz\n(AT221)", "Linz-Wels\n(AT312)", "Rheintal-\nBodensee\n(AT342)"])     
ax.set_title("Heat density of district heating in 2050 "+r"in $\frac{GWh}{km^2}$", fontsize=12)


import matplotlib.patches as mpatches
_patches = []
_patches.append(mpatches.Patch(facecolor='#A2D2FF', label='Directed Transition', edgecolor="none", linewidth=1))
_patches.append(mpatches.Patch(facecolor='#FF865E', label='Societal Commitment', edgecolor="none", linewidth=1))
_patches.append(mpatches.Patch(facecolor='#FEE440', label='Techno-Friendly', edgecolor="none", linewidth=1))
_patches.append(mpatches.Patch(facecolor='#C8C6C6', label='Gradual Development', edgecolor="none", linewidth=1))

leg = ax.legend(handles=_patches, loc='upper right', fontsize=8, framealpha=1, handlelength=1, handletextpad=0.5, frameon=True, fancybox=True, shadow=False, edgecolor="black",  ncol=2, title="Scenarios", columnspacing=0.5, title_fontsize=10, bbox_to_anchor=(0.96, 0.975))




leg.get_frame().set_linewidth(0.5)


# ax2 = ax.twinx()
# ax2.get_yaxis().set_visible(False)


# _patches = []
# _patches.append(mpatches.Patch(facecolor='#B2B1B9', label='Plain bars indicate scenario\nwith lowest heat density', edgecolor="none", linewidth=0.75))
# _patches.append(mpatches.Patch(facecolor='#B2B1B9', label='Hatched bars show the difference\nto the scenario with the highest heat density', edgecolor="black", linewidth=0.75, hatch="/////"))
# leg2 = ax2.legend(handles=_patches, loc="upper right", fontsize=8, framealpha=1, handlelength=1, handletextpad=1, frameon=True, fancybox=True, shadow=False, edgecolor="black", ncol=1, bbox_to_anchor=(0.95,0.85))
# leg2.get_frame().set_linewidth(0.25)

axins = ax.inset_axes([.55, .45, .4, .3])
axins.set_xticks([])
axins.set_yticks([])
_data = data.filter(region="AT221")
frame = _data.data
frame["value"]=[2,2]
_data = py.IamDataFrame(frame)
_fig = _data.plot.bar(ax=axins, stacked=True, bars="scenario", x="region", legend=False)
axins.set_title("")
axins.set_ylabel("")
axins.set_xlabel("")
axins.set_xlim(-0.5, 6)
axins.set_ylim(0,5)
# axins.patch.set_facecolor('none')
axins.grid("off")
axins.set_xticks(ticks=[])

_fig.patches[0].set_color("#E6DDC6")
_fig.patches[0].set_alpha(0.9)


ax.tick_params(axis='y', which='major', labelsize=10)
ax.tick_params(axis='x', which='major', labelsize=10)

_fig.patches[1].set_color("#E6DDC6")
_fig.patches[1].set_edgecolor("black")
_fig.patches[1].set_hatch("///")

axins.text(x=1.35, y=1.5, s='Scenario with the lowest\nheat density (bottom bar)', 
        rotation=0, fontsize=8, color='black',
          ha='left', va='center', style="normal")

axins.annotate(
    '',
    fontsize=0,
    color="red",
    multialignment='center',
    xy=(0, 1), xycoords='data',
    xytext=(1.2, 1.5), textcoords='data',
    arrowprops=dict(headlength=5, 
                    headwidth=2,
                    width=0.5,
                    connectionstyle="arc3,rad=-.2",
                    color="black"))

axins.text(x=1.35, y=3.5, s='Max increase in heat density\ncompared to the scenario\nwith the lowest value', 
        rotation=0, fontsize=8, color='black',
          ha='left', va='center', style="normal")

axins.annotate(
    '',
    fontsize=0,
    color="red",
    multialignment='center',
    xy=(0, 3), xycoords='data',
    xytext=(1.2, 3.5), textcoords='data',
    arrowprops=dict(headlength=5, 
                    headwidth=2,
                    width=0.5,
                    connectionstyle="arc3,rad=-.2",
                    color="black"))

ax.set_ylabel("")
plt.tight_layout()
plt.savefig("test.png", dpi=500)
plt.savefig("benchmark.eps", format="eps")
