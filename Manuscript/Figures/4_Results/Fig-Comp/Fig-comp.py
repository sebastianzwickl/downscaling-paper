import matplotlib.pyplot as plt

plt.style.use("seaborn")
fig, ax = plt.subplots()

tech = ["Total demand", "Heat Storage", "Biomass", "Direct electric", "Natural gas", "Hydrogen", "Heat pump (air)", "Heat pump (ground)", "Oil"]
height1 = [-18.15,10.58,-8.87,-2.09,-46.68,2.17,15.7,21.47,-10.29]
bars = ax.bar(x=[1,2,3,4,5,6,7,8,9], height=height1, linewidth=1.)
ax.plot([0.5, 9.5], 2*[0], color="black", linewidth=2.5)
ax.set_xticks(range(1,10,1))
ax.set_xticklabels(labels=[])

for _v in enumerate(height1):
    if _v[1] > 0:
        ax.text(x=_v[0]+1, y=height1[_v[0]]+2, s="+"+str(height1[_v[0]]), va="center", ha="center", fontsize=14)
        ax.text(x=_v[0]+1, y=-1.5, s=str(tech[_v[0]]), va="top", ha="center", fontsize=14, rotation=90)
    else:
        # if _v[0] == 0:
        #     ax.text(x=_v[0]+1, y=height1[_v[0]]-3, s=str(height1[_v[0]]), va="center", ha="center", fontsize=14, 
        #             bbox=dict(facecolor='none', edgecolor='#91091e', boxstyle='round,pad=0.25', linestyle='dashed',
        #                                      linewidth=1))
        #     ax.text(x=_v[0]+1, y=1.5, s=str(tech[_v[0]]), va="bottom", ha="center", fontsize=14, rotation=90)
        # else:
            
        #     ax.text(x=_v[0]+1, y=height1[_v[0]]-3, s=str(height1[_v[0]]), va="center", ha="center", fontsize=14)
        #     ax.text(x=_v[0]+1, y=1.5, s=str(tech[_v[0]]), va="bottom", ha="center", fontsize=14, rotation=90)
        ax.text(x=_v[0]+1, y=height1[_v[0]]-3, s=str(height1[_v[0]]), va="center", ha="center", fontsize=14)
        ax.text(x=_v[0]+1, y=1.5, s=str(tech[_v[0]]), va="bottom", ha="center", fontsize=14, rotation=90)
        
ax.annotate(
    '',
    fontsize=0,
    color="red",
    multialignment='center',
    xy=(1, -23), xycoords='data',
    xytext=(1.4, -30), textcoords='data',
    arrowprops=dict(headlength=8, 
                    headwidth=4,
                    width=0.75,
                    connectionstyle="arc3,rad=-.4",
                    color="#000000"))
ax.text(x=1.5, y=-33, s="Values of the Societal Commitment\nscenario (scenario with lowest\ntotal heat demand)", fontsize=10)

ax.annotate(
    'Scenario with\nhighest value',
    fontsize=10,
    color="black",
    multialignment='center',
    xy=(5.55, -46.8), xycoords='data',
    xytext=(6.1, -35), textcoords='data',
    arrowprops=dict(headlength=8, 
                    headwidth=4,
                    width=0.75,
                    connectionstyle="arc3,rad=-.2",
                    color="#000000"))


ax.annotate(
    'Scenario with\nlowest value',
    fontsize=10,
    color="black",
    multialignment='center',
    xy=(5.55, -53.76), xycoords='data',
    xytext=(6.1, -47.5), textcoords='data',
    arrowprops=dict(headlength=8, 
                    headwidth=4,
                    width=0.75,
                    connectionstyle="arc3,rad=-.2",
                    color="#000000"))




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

leg = ax.legend(handles=_patches, loc='lower left', fontsize=12, framealpha=1, handlelength=0.75, handletextpad=0.5, frameon=True, fancybox=True, shadow=False, edgecolor="black")
leg.get_frame().set_linewidth(1)

ax.fill_between(x=[1.425,1.475],y1=-15.21, y2=-18.15, color="gray", alpha=0.8)
ax.plot(1.45, -18.15, marker="H", markersize=6, color="black")
ax.plot(1.45, -15.21, marker="v", markersize=6, color="black")

ax.fill_between(x=[2.425,2.475],y1=10.58, y2=16.35, color="gray", alpha=0.8)
ax.plot(2.45, 10.58, marker="H", markersize=6, color="black")
ax.plot(2.45, 16.35, marker="*", markersize=8, color="black")

ax.plot(3.45, -8.87, marker="H", markersize=6, color="black")

ax.fill_between(x=[4.425,4.475],y1=-1.94, y2=-2.53, color="gray", alpha=0.8)
ax.plot(4.45, -1.94, marker="d", markersize=6, color="black")
ax.plot(4.45, -2.53, marker="*", markersize=8, color="black")

ax.fill_between(x=[5.425,5.475],y1=-46.68, y2=-53.76, color="gray", alpha=0.8)
ax.plot(5.45, -46.68, marker="H", markersize=6, color="black")
ax.plot(5.45, -53.76, marker="d", markersize=6, color="black")

ax.fill_between(x=[6.425,6.475],y1=1.03, y2=8.65, color="gray", alpha=0.8)
ax.plot(6.45, 1.03, marker="d", markersize=6, color="black")
ax.plot(6.45, 8.65, marker="v", markersize=6, color="black")

ax.fill_between(x=[7.425,7.475],y1=9.67, y2=22.73, color="gray", alpha=0.8)
ax.plot(7.45, 22.73, marker="d", markersize=6, color="black")
ax.plot(7.45, 9.67, marker="v", markersize=6, color="black")

ax.fill_between(x=[8.375+0.05,8.425+0.05],y1=6.69, y2=21.47, color="gray", alpha=0.8)
ax.plot(8.45, 6.69, marker="*", markersize=8, color="black")
ax.plot(8.45, 21.47, marker="H", markersize=6, color="black")

ax.plot(9.45, -10.29, marker="H", markersize=6, color="black")

ax2 = ax.twinx()
ax2.get_yaxis().set_visible(False)
_patches = []
_line = Line2D([0], [0], label = "Directed Transition",color="black", marker="d", markersize=8, linewidth=0)
_patches.extend([_line])
_line = Line2D([0], [0], label = "Societal Commitment",color="black", marker="H", markersize=8, linewidth=0)
_patches.extend([_line])
_line = Line2D([0], [0], label = "Techno-Friendly",color="black", marker="*", markersize=10, linewidth=0)
_patches.extend([_line])
_line = Line2D([0], [0], label = "Gradual Development",color="black", marker="v", markersize=8, linewidth=0)
_patches.extend([_line])
# leg = ax.legend(handles=_patches, loc='lower left', fontsize=14, framealpha=1, handlelength=0.75, handletextpad=0.5, frameon=True, fancybox=True, shadow=False, edgecolor="black")
leg2 = ax2.legend(handles=_patches, loc="lower right", fontsize=12, framealpha=1, handlelength=0.75, handletextpad=0.2, frameon=True, fancybox=True, shadow=False, edgecolor="black")
leg2.get_frame().set_linewidth(1)
# "v" = "Gradual Development"
# "H" = Societal Commitment
# "*" = "Techno-Friendly"
# "d" = Direct-Transition

ax.set_yticklabels(labels=[])
ax.set_title("Absolute differences of heat generation by source\n between 2020 and 2050 in TWh", fontsize=20)
plt.tight_layout()
fig.savefig("Ref-2050.png", dpi=500)
fig.savefig("Ref-2050.eps", format="eps")
