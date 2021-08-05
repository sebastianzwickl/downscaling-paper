import matplotlib.pyplot as plt

plt.style.use("seaborn")
fig, ax = plt.subplots()

tech = ["Total demand", "Storage", "Biomass", "Direct electric", "Natural gas", "Hydrogen", "Heat pump (air)", "Heat pump (ground)", "Oil"]
height1 = [-18.15,10.58,-8.87,-2.09,-46.00,2.17,15.7,21.47,-10.29]
bars = ax.bar(x=[1,2,3,4,5,6,7,8,9], height=height1, linewidth=1.)
ax.plot([0.5, 9.5], 2*[0], color="black", linewidth=2.5)
ax.set_xticks(range(1,10,1))
ax.set_xticklabels(labels=[])

for _v in enumerate(height1):
    if _v[1] > 0:
        ax.text(x=_v[0]+1, y=height1[_v[0]]+2, s="+"+str(height1[_v[0]]), va="center", ha="center", fontsize=14)
        ax.text(x=_v[0]+1, y=-1.5, s=str(tech[_v[0]]), va="top", ha="center", fontsize=14, rotation=90)
    else:
        ax.text(x=_v[0]+1, y=height1[_v[0]]-3, s=str(height1[_v[0]]), va="center", ha="center", fontsize=14)
        ax.text(x=_v[0]+1, y=1.5, s=str(tech[_v[0]]), va="bottom", ha="center", fontsize=14, rotation=90)
        

plt.rcParams['hatch.linewidth'] = 1

bars[0].set_hatch('///')
bars[0].set_facecolor('#FF4C29')
bars[0].set_edgecolor('#548CA8')

bars[1].set_facecolor('#93D9A3')
bars[1].set_edgecolor('#52734D')

bars[5].set_facecolor('#91C788')
bars[5].set_edgecolor('#52734D')

bars[7].set_facecolor('#91C788')
bars[7].set_edgecolor('#52734D')

bars[6].set_facecolor('#91C788')
bars[6].set_edgecolor('#52734D')

bars[2].set_facecolor('#FF4C29')
bars[2].set_edgecolor('#9C3D54')

bars[3].set_facecolor('#FF4C29')
bars[3].set_edgecolor('#9C3D54')

bars[4].set_facecolor('#FF4C29')
bars[4].set_edgecolor('#9C3D54')

bars[8].set_facecolor('#FF4C29')
bars[8].set_edgecolor('#9C3D54')

import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
_patches = []
_line = Line2D([0], [0], label = "2020\'s values (reference year)",color="black", linewidth=3)
_patches.extend([_line])
_patches.append(mpatches.Patch(facecolor='#FF4C29', label='Total demand', edgecolor="#52734D", linewidth=0.75, hatch="/////"))
_patches.append(mpatches.Patch(facecolor='#93D9A3', label='Increasing generation', edgecolor="#52734D", linewidth=0.75))
_patches.append(mpatches.Patch(facecolor='#FF4C29', label='Decreasing generation', edgecolor="#9C3D54", linewidth=0.75))




leg = ax.legend(handles=_patches, loc='lower left', fontsize=14, framealpha=1, handlelength=0.75, handletextpad=0.5, frameon=True, fancybox=True, shadow=False, edgecolor="black")
leg.get_frame().set_linewidth(1)


ax.set_yticklabels(labels=[])
ax.set_title("Relative differences of heat generation by source\nbetween 2020 and 2050", fontsize=20)
plt.tight_layout()
fig.savefig("Ref-2050.png", dpi=500)
fig.savefig("Ref-2050.eps", format="eps")
