import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.style.use("ggplot")
fig = plt.figure(constrained_layout=False)
gs = fig.add_gridspec(nrows=3, ncols=2, height_ratios=[0.8, 1.2, 0.5],
                      width_ratios=[1,1])

fig_init = fig.add_subplot(gs[0, 0])
_sce = "Directed Transition"
heat_gen_lau = gpd.read_file("init_state_algorithm2.shp")
heat_gen_lau = heat_gen_lau.loc[heat_gen_lau.scenario == _sce]
_boundary = heat_gen_lau.loc[heat_gen_lau["NUTS3_CODE"] == "AT127"]
_boundary = gpd.GeoDataFrame(_boundary)
_boundary.plot(ax=fig_init, linewidth=0, color="#B6C9F0", linestyle="solid", alpha=1)
_boundary.boundary.plot(ax=fig_init, linewidth=0.05, color="black", linestyle="solid")


fig_init.set_title("Initial condition\n(large area - difficult topology)", fontsize=10)
fig_init.set_xticks([])
fig_init.set_yticks([])
fig_init.set_xlabel("$75$ communities ($i=1$)", fontsize=8)


fig_bench = fig.add_subplot(gs[0, 1])
_boundary.boundary.plot(
    ax=fig_bench, linewidth=0.1, color="black", linestyle="solid", zorder=1
)
_boundary.plot(
    ax=fig_bench, linewidth=0, color="#F6F5F5", linestyle="solid", alpha=1, zorder=-50
)

_boundary = gpd.read_file("generation.shp")
_boundary = _boundary.loc[_boundary["NUTS3_CODE"] == "AT127"]
_boundary = gpd.GeoDataFrame(_boundary)
_boundary.plot(
    ax=fig_bench, linewidth=0.25, color="#0F52BA", linestyle="solid", zorder=-1
)
_boundary.boundary.plot(
    ax=fig_bench, linewidth=0.5, color="#D1D9D9", linestyle="solid", zorder=0
)
# fig_bench.axis("off")
# fig_bench.set_title("Final condition\n with $47$ sub-areas ($i=29$)")
fig_bench.set_title("Final condition\n(smaller area - improved topology)", fontsize=10)
fig_bench.set_xticks([])
fig_bench.set_yticks([])
fig_bench.set_xlabel("$47$ communities ($i=29$)", fontsize=8)
# fig_bench.set_facecolor("white")


fig_box = fig.add_subplot(gs[1, 0:2])
data = pd.read_excel("Directed Transition1.xlsx")

fig_box.annotate(
    "",
    fontsize=10,
    color="black",
    multialignment="center",
    xy=(1.3, 2),
    xycoords="data",
    xytext=(7, 4),
    textcoords="data",
    arrowprops=dict(
        headlength=8,
        headwidth=4,
        width=0.75,
        connectionstyle="arc3,rad=.2",
        color="#000000",
    ),
)

# fig_box.text(x=5.8, y=3.8, s='Initial supply area\n($\Pi_{mean,75}=0.33$)', rotation=0, fontsize=9, color='#000000',
#           ha='center', va='center')

fig_box.text(
    x=7.8,
    y=5.2,
    s="Initial condition\n($\pi_{mean,75}=0.33$)",
    rotation=0,
    fontsize=9,
    color="black",
    ha="center",
    va="center",
    bbox=dict(
        facecolor="#B6C9F0",
        edgecolor="black",
        boxstyle="round,pad=1",
        linestyle="solid",
        linewidth=0.5,
        alpha=1,
    ),
    zorder=100,
)


fig_box.annotate(
    "",
    fontsize=10,
    color="black",
    multialignment="center",
    xy=(28.7, 3),
    xycoords="data",
    xytext=(20, 5.6),
    textcoords="data",
    arrowprops=dict(
        headlength=8,
        headwidth=4,
        width=0.75,
        connectionstyle="arc3,rad=-.25",
        color="#000000",
    ),
)

# fig_box.text(x=21., y=6, s='Final supply area\n($\Pi_{mean,47}=1.94$)', rotation=0, fontsize=9, color='#000000',
#           ha='center', va='center')

fig_box.text(
    x=17.5,
    y=5.2,
    s="Final condition\n($\pi_{mean,47}=1.94$)",
    rotation=0,
    fontsize=9,
    color="#0F52BA",
    ha="center",
    va="center",
    bbox=dict(
        facecolor="#F6F5F5",
        edgecolor="#0F52BA",
        boxstyle="round,pad=1",
        linestyle="solid",
        linewidth=1.5,
        alpha=1,
    ),
    zorder=100,
)

# fig_box.set_title("Increasing number of iterations improves benchmark indicator mean value and reduces supply area")

values = list()
for c in data.columns:
    if c != "Unnamed: 0":
        val = data[c].values
        a = np.array([1000])
        c = np.setdiff1d(val, a)
        values.append(c)

_boxplot = fig_box.boxplot(values, notch=True, vert=True, patch_artist=True)
for patch in _boxplot["boxes"]:
    patch.set_facecolor("#47597E")
    patch.set_edgecolor("#232323")

for whisker in _boxplot["whiskers"]:
    whisker.set(color="#232323", linewidth=1, linestyle=":")

for median in _boxplot["medians"]:
    median.set(color="#FF7600", linewidth=2.5)

for flier in _boxplot["fliers"]:
    flier.set(marker="D", color="#e7298a", markersize=2.5)

# fig_box.set_xlabel("Number of iteration ($i$)")
fig_box.set_ylabel("Benchmark\nindicator value ($\pi$)", fontsize=8)
fig_box.xaxis.set_tick_params(labelsize=8, rotation=0)


fig_area = fig.add_subplot(gs[2, 0:2])
fig_area.xaxis.set_ticks_position("top")
x = range(1, 30, 1)
fig_area.set_xticks(x)


y = [
    386.1526,
    385.0396,
    384.1386,
    383.5106,
    382.3626,
    381.5936,
    380.1686,
    378.6236,
    377.0086,
    375.3786,
    374.2006,
    372.5556,
    370.8006,
    369.2926,
    367.7356,
    366.7976,
    365.9026,
    363.8326,
    361.7806,
    357.6386,
    356.1896,
    353.2076,
    351.9586,
    343.9516,
    341.7446,
    339.8976,
    338.4146,
    336.4926,
    334.7466,
]

fig_area.plot(x, y, marker="d", linestyle="dashed", color="gray")
fig_area.set_xlim([0.5, 29.5])
fig_area.set_xticklabels(labels=[])
fig_area.set_yticks([325, 350, 375])
fig_area.set_ylim([300, 400])
fig_area.set_ylabel("Connected\npopulation", fontsize=8)
fig_area.set_xlabel("Number of iteration ($i$)", fontsize=10)
fig_area.set_yticklabels(labels=["325k", "350k", "375k"], fontsize=6)

fig_area.annotate(
    "$386$k connected population",
    fontsize=10,
    color="black",
    multialignment="center",
    xy=(1, 375),
    xycoords="data",
    xytext=(3, 330),
    textcoords="data",
    arrowprops=dict(
        headlength=8,
        headwidth=4,
        width=0.75,
        connectionstyle="arc3,rad=-.4",
        color="#000000",
    ),
)

fig_area.annotate(
    "$-13.3\%$",
    fontsize=10,
    color="black",
    multialignment="center",
    xy=(29, 345),
    xycoords="data",
    xytext=(24, 370),
    textcoords="data",
    arrowprops=dict(
        headlength=8,
        headwidth=4,
        width=0.75,
        connectionstyle="arc3,rad=-.4",
        color="#000000",
    ),
)


fig.suptitle(
    "Centralized heat network topology improves by reducing supply area",
    y=0.975,
)
plt.tight_layout(w_pad=0, h_pad=-0)
fig.savefig("ext_boxplot.png", dpi=500)
fig.savefig("ext_boxplot.eps", format="eps")
