import matplotlib.pyplot as plt
import numpy as np
import numpy as np


labels = ["Vienna\n(AT130)", "Graz\n(AT221)", "Linz-Wels\n(AT312)", "Rheintal-Bodensee\n(AT342)"]

DT_min = [10.17, 4.0, 4.4, 1.65]
DT_max = [18.27, 10.9, 11.8, 3.9]


SC_min = [13.75, 5.24, 5, 2.6]
SC_max = [18.07, 11.1, 10.6, 3.8]


TF_min = [24.37,2.7, 2.73, 3.5]
TF_max = [25.4,5, 4.66, 4.1]

GD_min = [26.6,2.6, 2.34, 3.54]
GD_max = [26.8,2.8, 2.71, 3.65]




circle = [10.17, 13.75, 24.37, 26.79, 4.9, 8.1, 5, 2.8, 4.92, 7.7, 4.66, 2.71, 1.65, 2.6, 3.82, 3.65]
diamond = [18.27, 18.07, 25.4, 26.83, 4.0, 5.24, 2.7, 2.6, 4.4, 5, 2.84, 2.34, 3.9, 3.8, 3.5, 3.54]




# labels = ['G1', 'G2', 'G3', 'G4', 'G5']
# men_means = [20, 34, 30, 35, 27]
# women_means = [25, 32, 34, 20, 25]

x = np.arange(len(labels))  # the label locations
width = 0.25  # the width of the bars
x_circle = [-3/4*width, -1/4*width, +1/4*width, 3/4*width, -3/4*width+1, -1/4*width+1, +1/4*width+1, 3/4*width+1, -3/4*width+2, -1/4*width+2, +1/4*width+2, 3/4*width+2, -3/4*width+3, -1/4*width+3, +1/4*width+3, 3/4*width+3]
fig, ax = plt.subplots()

ax.yaxis.grid(color='lightgray', linestyle='-.', linewidth=0.5, zorder=-100)



rects1 = ax.bar(x-3/4 * width, np.subtract(DT_max,DT_min), width/2, label='Directed Transition', bottom=DT_min, color="#502064")
rects2 = ax.bar(x - width/4, np.subtract(SC_max, SC_min), width/2, label='Societal Commitment', bottom=SC_min, color="#8267BE")
rects3 = ax.bar(x + width/4, np.subtract(TF_max,TF_min), width/2, label='Techno-Friendly', bottom=TF_min, color="#3FA796")
rects4 = ax.bar(x + 3/4*width, np.subtract(GD_max,GD_min), width/2, label='Gradual Development', bottom=GD_min, color="#FFBD35")

ax.plot(x_circle, circle, marker="o", markersize=5, label="Heat pump (air) on-site", linewidth=0, color="black")
ax.plot(x_circle, diamond, marker="d", markersize=5, label="Heat pump (air) in DH", linewidth=0, color="black")

ax.plot([0.6, 0.75], [10.9, 10.9], linewidth=0.5, color="black")
ax.plot([0.6, 0.6], [10.9, 11.7], linewidth=0.5, color="black")
ax.text(x=0.2, y=12, s="Maximum", fontsize=10)

ax.plot([0.6, 0.75], [4, 4], linewidth=0.5, color="black")
ax.plot([0.6, 0.6], [4, 4.8], linewidth=0.5, color="black")
ax.text(x=0.2, y=5.1, s="Minimum", fontsize=10)

# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax.set_ylabel('Scores')
ax.set_title("Heat density of district heating (DH) "+r"in $\frac{GWh}{km^2}$", pad=10, fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(labels=labels)

ax.tick_params(axis='y', which='major', labelsize=10)
ax.tick_params(axis='x', which='major', labelsize=10)

# import matplotlib.patches as mpatches
# _patches = []
# _patches.append(mpatches.Patch(facecolor='#502064', label='Directed Transition', edgecolor="none", linewidth=1))
# _patches.append(mpatches.Patch(facecolor='#8267BE', label='Societal Commitment', edgecolor="none", linewidth=1))
# _patches.append(mpatches.Patch(facecolor='#3FA796', label='Techno-Friendly', edgecolor="none", linewidth=1))
# _patches.append(mpatches.Patch(facecolor='#FFBD35', label='Gradual Development', edgecolor="none", linewidth=1))


leg = ax.legend(loc='upper right', fontsize=9, framealpha=1, handlelength=1, handletextpad=0.75, frameon=True, fancybox=True, shadow=False, edgecolor="black",  ncol=1, columnspacing=0.5)
leg.get_frame().set_linewidth(0.5)


fig.tight_layout()

fig.savefig("4x4.png", dpi=1000)
fig.savefig("4x4.eps", format="eps")