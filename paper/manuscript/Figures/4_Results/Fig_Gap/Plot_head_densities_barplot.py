import pyam as py
import matplotlib.pyplot as plt
import matplotlib.colors as c
import numpy as np

_c_list = ["#284E78", "#FF96AD"]
_new_cm = c.ListedColormap(colors=_c_list, name="New cmap")


plt.style.use("seaborn-paper")
fig = plt.figure(constrained_layout=False)
gs = fig.add_gridspec(2, 2)
fig_DT = fig.add_subplot(gs[0, 0])
fig_SC = fig.add_subplot(gs[0, 1])
fig_TF = fig.add_subplot(gs[1, 0])
fig_GD = fig.add_subplot(gs[1, 1])
_fig = [fig_DT, fig_SC, fig_TF, fig_GD]
sce = ["Directed Transition", "Societal Commitment", "Techno-Friendly", "Gradual Development"]
a_tuple = zip(_fig, sce)
data = py.IamDataFrame("Heat_density_algorithm2.xlsx")
data.filter(variable="Heat density", inplace=True)


for _tup in a_tuple:
    plot = data.filter(scenario=_tup[1], keep=True)
    
    val = plot.data["value"]
    
    for i, v in enumerate(val):
        _tup[0].text(i, v+0.5, str(np.round(v,2)), color='black', ha="center", va="center", fontsize=6)
        
    
    # for i, v in enumerate(height):
    # ax.text(i+1, v+0.25, str(np.round(v-_red[i],2)), color='black', ha="center", va="center", fontsize=10)
    
    bars = plot.plot.bar(ax=_tup[0], 
                  x="region", 
                  stacked=True, 
                  bars="variable", 
                  orient="v", 
                  legend=False, 
                  title=None, 
                  cmap=_new_cm,
                  bars_order=["Heat density", "Heat density gap (2050 and today)"],
                  alpha=1)
    # _tup[0].set_ylim([0,10.5])
    _tup[0].set_title(_tup[1], pad=0)
    _tup[0].set_xlabel("")
    _tup[0].set_ylabel("")
    _tup[0].xaxis.set_tick_params(labelsize=6, rotation=0, pad=0)
    _tup[0].tick_params(axis='y', which='major', pad=2)
    _tup[0].tick_params(axis='x', which='major', pad=2)
    _tup[0].set_xticklabels(labels=["South\nViennesse\nenviron\n(AT127)", "Vienna\n(AT130)", "Graz\n(AT221)", "Linz-Wels\n(AT312)", "Salzburg\n(AT323)", "Rheintal-\nBodensee\n(AT342)"])
    # if _tup[1] == "Techno-Friendly":
    #     plt.rcParams['hatch.linewidth'] = 1
    #     bars.patches[8].set_hatch("///")
    #     bars.patches[8].set_edgecolor('#FFF5FD')
    ymin, ymax = _tup[0].get_ylim()
    _tup[0].set_ylim([ymin, ymax+1])

        
    
    
handles, labels = _tup[0].get_legend_handles_labels()
fig.suptitle("Heat density of centralized heat networks in Austrian sub-regions 2050\nin the four different decarbonization scenarios "+r"in $\frac{GWh}{km^2}$", y=0.95)
plt.tight_layout()
fig.savefig("HD1.png", dpi=500)
fig.savefig("HD1.eps", format="eps") 




