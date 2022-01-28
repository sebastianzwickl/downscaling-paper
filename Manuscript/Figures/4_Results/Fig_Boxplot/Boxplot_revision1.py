import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


"""PREAMBLE"""
_sce = "Techno-Friendly"
_subregion = "AT312"


"""COLORS AND STYLE"""
_str = "#04009A"
plt.style.use("ggplot")
plt.rcParams['axes.facecolor'] = '#F5F5F5'



"""CREATE FIGURE ENVIRONMENT"""
fig = plt.figure(constrained_layout=False)
gs = fig.add_gridspec(nrows=3, ncols=2, height_ratios=[0.8, 1.2, 0.5],
                      width_ratios=[1,1])


"""PLOT INIT NETWORK TOPOLOGY"""
ax_up_left = fig.add_subplot(gs[0,0])
_data = gpd.read_file("init_state_algorithm2.shp")
generation = _data.loc[(_data.scenario == _sce) & (_data.NUTS3_CODE == _subregion)]
number_init = int(len(generation.index)/2)
polygons = gpd.GeoDataFrame(generation)
polygons.boundary.plot(ax=ax_up_left, linewidth=0.025, color="black", linestyle="solid")
_single_polygon = polygons.geometry.unary_union
single_polygon = gpd.GeoDataFrame(geometry=[_single_polygon])
single_polygon.boundary.plot(ax=ax_up_left, color=_str, linewidth=0.5)
single_polygon.plot(ax=ax_up_left, color="lightgray")
ax_up_left.set_title("Initial condition\n(large area - difficult topology)", fontsize=9, color="#334257")
ax_up_left.set_xticks([])
ax_up_left.set_yticks([])
ax_up_left.set_xlabel(str(number_init)+" communities ($i=1$)", fontsize=8, color="#334257")

fig.text(x=0.0475, y=0.775, s="Linz-Wels\n(AT312)", fontsize=8, rotation=90, color="#334257", va="center", ha="center",
         bbox=dict(facecolor="white", edgecolor="gray", boxstyle='round,pad=1', linestyle='solid',
                                              linewidth=0.25))

"""PLOT IMPROVED NETWORK TOPOLOGY"""
ax_up_right = fig.add_subplot(gs[0, 1])
polygons.boundary.plot(ax=ax_up_right, linewidth=0.025, color="black", linestyle="solid")
ax_up_right.set_title("Final condition\n(smaller area - improved topology)", fontsize=9, color="#334257")
ax_up_right.set_xticks([])
ax_up_right.set_yticks([])
_improved_generation = gpd.read_file("generation.shp")
_single_polygon = _improved_generation.geometry.unary_union
single_polygon = gpd.GeoDataFrame(geometry=[_single_polygon])
single_polygon.boundary.plot(ax=ax_up_right, color=_str, linewidth=0.5)
single_polygon.plot(ax=ax_up_right, color="lightgray")
number = len(_improved_generation.index)
ax_up_right.set_xlabel(str(number)+" communities ($i=65$)", fontsize=8, color="#334257")


"""PLOT BOXPLOT DEVELOPMENT"""
fig_box = fig.add_subplot(gs[1, 0:2])
data = pd.read_excel("indicator_values.xlsx")
values = list()
for c in data.columns:
    if c != "Unnamed: 0":
        val = data[c].values
        a = np.array([1000])
        c = np.setdiff1d(val, a)
        values.append(c)

_boxplot = fig_box.boxplot(values, notch=False, vert=True, patch_artist=True, showfliers=False)
for patch in _boxplot["boxes"]:
    patch.set_facecolor("#47597E")
    patch.set_edgecolor("#232323")

for whisker in _boxplot["whiskers"]:
    whisker.set(color="#232323", linewidth=1, linestyle=":")

for median in _boxplot["medians"]:
    median.set(color="#FF7600", linewidth=1.5)

fig_box.set_ylabel("Benchmark\nindicator value ($\pi$)", fontsize=8)

from matplotlib.lines import Line2D
_patches = []
_line = Line2D([0], [0], label = r'Median',color="#FF7600", linewidth=2)
_patches.extend([_line])
_line = Line2D([0], [0], label = r'$1^{st}$/$3^{rd}$ Quartile',color="#47597E", linewidth=5)
_patches.extend([_line])
_line = Line2D([0], [0], label = "Minimum/Maximum",color="black", linewidth=0.85, linestyle="dotted")
_patches.extend([_line])
leg = fig_box.legend(handles=_patches, loc='upper left', fontsize=5.5, framealpha=1, handlelength=1, handletextpad=0.75, borderpad=0.75, columnspacing=1, edgecolor="black", frameon=True, ncol=3, bbox_to_anchor=(0.025,0.95))
leg.get_frame().set_linewidth(0.25)

diff = number_init - number
xticks = list(range(0, diff, 5))
xticks.append(diff+1)
fig_box.set_xticks(xticks)
fig_box.set_xticklabels(labels=xticks)

fig_box.xaxis.set_tick_params(labelsize=6, rotation=0)
fig_box.yaxis.set_tick_params(labelsize=6)


"""PLOT CONNECTED PEOPLE TO DISTRICT HEATING NETWORK"""
population = pd.read_excel("Removed_population.xlsx")[0]
hard_coded_population = 663623
values = list()
values.append(hard_coded_population)
for pop in population:
    _val = values[-1] - pop
    values.append(_val)
y = values[0:-1]
fig_area = fig.add_subplot(gs[2, 0:2])
fig_area.xaxis.set_ticks_position("top")
fig_area.set_xticks([])

x = range(1, diff+2, 1)

# fig_area.set_xticklabels(labels=xticks, fontsize=0)

fig_area.plot(x, y, marker="d", linestyle="dashed", color="gray", markersize=2)
fig_area.set_xlim([0, diff+1.5])
fig_area.set_xticklabels(labels=[])


fig_area.set_yticks([350000, 500000, 650000])
# fig_area.set_ylim([50000, 400000])
fig_area.set_ylabel("Population of\ncommunities", fontsize=8)
fig_area.set_xlabel("Number of iteration ($i$)", fontsize=8)
fig_area.set_yticklabels(labels=["350k", "500k", "650k"], fontsize=6)

fig_area.annotate(
    "$663$k (total population)",
    fontsize=7,
    color="black",
    multialignment="center",
    xy=(1, 640000),
    xycoords="data",
    xytext=(4, 400000),
    textcoords="data",
    arrowprops=dict(
        headlength=8,
        headwidth=4,
        width=0.75,
        connectionstyle="arc3,rad=-.2",
        color="gray",
    ),
)

fig_area.annotate(
    "397k $(-40\%)$",
    fontsize=7,
    color="black",
    multialignment="center",
    xy=(65, 430000),
    xycoords="data",
    xytext=(52, 580000),
    textcoords="data",
    arrowprops=dict(
        headlength=8,
        headwidth=4,
        width=0.75,
        connectionstyle="arc3,rad=-.2",
        color="#000000",
    ),
)

# fig_box.annotate(
#     "",
#     fontsize=10,
#     color="black",
#     multialignment="center",
#     xy=(51, 0.325),
#     xycoords="data",
#     xytext=(39, 0.48),
#     textcoords="data",
#     arrowprops=dict(
#         headlength=8,
#         headwidth=4,
#         width=0.75,
#         connectionstyle="arc3,rad=-.2",
#         color="#0F52BA",
#     ),
# )

# # fig_box.text(x=5.8, y=3.8, s='Initial supply area\n($\Pi_{mean,75}=0.33$)', rotation=0, fontsize=9, color='#000000',
# #           ha='center', va='center')

# # fig_box.text(
# #     x=10,
# #     y=0.48,
# #     s="Initial condition",
# #     rotation=0,
# #     fontsize=5,
# #     color="black",
# #     ha="left",
# #     va="center",
# #     bbox=dict(
# #         facecolor="#B6C9F0",
# #         edgecolor="black",
# #         boxstyle="round,pad=1",
# #         linestyle="solid",
# #         linewidth=0.5,
# #         alpha=1,
# #     ),
# #     zorder=100,
# # )


# # fig_box.annotate(
# #     "",
# #     fontsize=10,
# #     color="#B6C9F0",
# #     multialignment="center",
# #     xy=(1, 0.325),
# #     xycoords="data",
# #     xytext=(10, 0.48),
# #     textcoords="data",
# #     arrowprops=dict(
# #         headlength=8,
# #         headwidth=4,
# #         width=1.25,
# #         facecolor="#B6C9F0",
# #         connectionstyle="arc3,rad=.2",
# #         edgecolor="black",
# #     ),
# # )

# # fig_box.text(x=21., y=6, s='Final supply area\n($\Pi_{mean,47}=1.94$)', rotation=0, fontsize=9, color='#000000',
# #           ha='center', va='center')

# # fig_box.text(
# #     x=39,
# #     y=0.48,
# #     s="Final condition",
# #     rotation=0,
# #     fontsize=5,
# #     color="#0F52BA",
# #     ha="center",
# #     va="center",
# #     bbox=dict(
# #         facecolor="#F6F5F5",
# #         edgecolor="#0F52BA",
# #         boxstyle="round,pad=1",
# #         linestyle="solid",
# #         linewidth=1.5,
# #         alpha=1,
# #     ),
# #     zorder=100,
# # )

# plt.tight_layout(w_pad=0, h_pad=-0)
fig.savefig("ext_boxplot.png", dpi=500)
fig.savefig("ext_boxplot.eps", format="eps")
