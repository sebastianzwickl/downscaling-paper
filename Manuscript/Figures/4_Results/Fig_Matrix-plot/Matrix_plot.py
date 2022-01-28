import matplotlib.pyplot as plt
import pandas as pd
import pyam as py
import matplotlib.ticker as tkr
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.lines import Line2D
import geopandas as gpd
import matplotlib.patches as patches


_color = {
    "Biomass": "#A6CF98",
    "Direct electric": "#FFAB76",
    "Geothermal": "#D4AC2B",
    "Synthetic gas" : "#D3DEDC",
    "Heat pump (air)": "#A2D2FF",
    "Heat pump (ground)": "#577BC1",
    "Hydrogen": "#B983FF",
    "Waste":"#8B9A46",
    "Oil":"#DA0037",
    }

_str = "#04009A"



def _plot_function(data=None, ax=None):
    Values = data.data.values
    number = Values[:,6]
    number=[number[2], number[3], number[7], number[8], number[0], number[1], number[4], number[5], number[6]]
    _order = ["Geothermal", "Synthetic gas", "Hydrogen", "Waste", "Biomass", "Direct electric", "Heat pump (air)", "Heat pump (ground)", "Oil"]
    _colors = [_color[key] for key in _order]
    ill = ax.pie(x=number, colors=_colors, startangle=200, radius=1, labels=None, frame=False, explode=[0.0, 0.05, 0.05, 0.05,0,0,0,0,0])
    _iter = 0
    _true = [False, True, True, True, False, False, False, False, False]
    for _p in ill[0]:
        if _true[_iter]:
            _p.set_edgecolor(_str)
            _p.set_linewidth(0.5)
            _p.set_ls("solid")
        _iter+=1
    return


def plot_first_column(data=None, ax=None):
    Values = data.data.values
    number = Values[:,6]
    number=[number[2], number[3], number[7], number[8], number[0], number[1], number[4], number[5], number[6]]
    _order = ["Geothermal", "Synthetic gas", "Hydrogen", "Waste", "Biomass", "Direct electric", "Heat pump (air)", "Heat pump (ground)", "Oil"]
    _colors = [_color[key] for key in _order]
    ill = ax.pie(x=number, colors=_colors, startangle=250, radius=0.5, labels=None, frame=True, explode=[0.05, 0.05, 0.05, 0.05,0,0,0,0,0], center=(0.5, 0.5))
    _iter = 0
    _true = [True, True, True, True, False, False, False, False, False]

    for _p in ill[0]:
        if _true[_iter]:
            _p.set_edgecolor(_str)
            _p.set_linewidth(0.5)
            _p.set_ls("solid")
        _iter+=1
    return


Genesysmod = py.IamDataFrame("GeneSys-Mod_Residential_heat_production_IAMC_format.xlsx")

# plt.style.use("seaborn-paper")
fig = plt.figure(constrained_layout=False)
gs = fig.add_gridspec(4, 4)








"""
DIRECTED TRANSITION
"""

fig_genesys_DT_AT = fig.add_subplot(gs[0, 0])
_plot = Genesysmod.filter(scenario="Directed Transition", year=2050)
# _colors = [_color[_key] for _key in _plot.variable]
_norm = sum(_plot.data["value"])*0.27778

_plot = Genesysmod.filter(scenario="Directed Transition", year=2050)
# _size = sum(_plot.data["value"])*0.27778

plot_first_column(_plot, fig_genesys_DT_AT)

# Values = _plot.data.values
# number = Values[:,6]
# number=[number[0], number[4], number[6], number[1], number[2], number[3], number[5], number[7]]
# _colors = ["#A0C334","#D2E603","#76EAD7","#FB7813","#4D4646","#AD9D9D", "#A7BBC7", "#DA0037"]



# ill = fig_genesys_DT_AT.pie(x=number, colors=_colors, startangle=250, radius=0.5, labels=None, frame=True, explode=[0.05, 0.05, 0.05, 0,0,0,0,0], center=(0.5, 0.5))
# _iter = 0
# _true = [True, True, True, False, False, False, False, False]

# for _p in ill[0]:
#     if _true[_iter]:
#         _p.set_edgecolor(_str)
#         _p.set_linewidth(0.5)
#         _p.set_ls("solid")
#     _iter+=1
    

fig_genesys_DT_AT.set_xticks([])
fig_genesys_DT_AT.set_yticks([])
fig_genesys_DT_AT.set_ylabel("Directed\nTransition", fontsize=7, labelpad=6, multialignment='center')
fig_genesys_DT_AT.set_title("Austria (country)", fontsize=10, pad=8)
fig_genesys_DT_AT.text(x=1.15, y=0.5, s=str(np.round(_norm,1))+" TWh", rotation="vertical", fontsize=6, ha="left", va="center")








fig_genesys_DT_NUTS3_LOW = fig.add_subplot(gs[0, 1])
_data = py.IamDataFrame("iamc_q_hat_subreg_plus.xlsx")
_plot = _data.filter(region="AT121", scenario="Directed Transition")

ill = _plot.plot.pie(cmap="tab20c", ax=fig_genesys_DT_NUTS3_LOW, legend=False, labels=None, radius=1, frame=False)
fig_genesys_DT_NUTS3_LOW.set_title("Rural (sub-region)", fontsize=8, pad=8)
_iter = 0
_colors = [_color[_key] for _key in _plot.variable]
for _patch in ill.patches:
    _patch.set_facecolor(_colors[_iter])
    _iter+=1
_norm = sum(_plot.data["value"])/1000000
fig_genesys_DT_NUTS3_LOW.text(x=1.1, y=-0.4, s=str(round(_norm,2))+" TWh", rotation="vertical", fontsize=5)
    
    
_plot = _data.filter(region="AT342", scenario="Directed Transition")
fig_genesys_DT_NUTS3_HIGH = fig.add_subplot(gs[0, 2])

var = _plot.data.variable
val = _plot.data.values
tuples = dict(zip(var, val))
order = ["Geothermal", "Synthetic gas", "Hydrogen", "Waste", "Biomass", "Direct electric", "Heat pump (air)", "Heat pump (ground)", "Oil"]
val_ordered = [tuples.get(x)[6] for x in order]
colors = [_color[key] for key in order]
ill = fig_genesys_DT_NUTS3_HIGH.pie(x=val_ordered, colors=colors, startangle=200, radius=1, labels=None, frame=False, explode=[0.0, 0.05, 0.0, 0.05,0,0,0,0,0])
_true = [False, True, False, True, False, False, False, False, False]
i = 0
for _p in ill[0]:
    if _true[i]:
        _p.set_edgecolor(_str)
        _p.set_linewidth(0.5)
        _p.set_ls("solid")
    i+=1

fig_genesys_DT_NUTS3_HIGH.set_title("Urban (sub-region)", fontsize=8, pad=8)
_norm = sum(_plot.data["value"])/1000000
fig_genesys_DT_NUTS3_HIGH.text(x=1.3, y=-0.4, s=str(round(_norm,2))+" TWh", rotation="vertical", fontsize=5)


fig_genesys_DT_LAU = fig.add_subplot(gs[0, 3], frameon=False)
fig_genesys_DT_LAU.set_xticks([])
fig_genesys_DT_LAU.set_yticks([])

fig_genesys_DT_LAU.set_title("District heating (community)", fontsize=6, pad=8)


_var = gpd.read_file("Directed Transition/generation.shp")
_boundary = gpd.read_file("Directed Transition/polygons.shp")
_cen = _var.centroid.to_frame()
_boundary.boundary.plot(ax=fig_genesys_DT_LAU, linewidth=0.1, color="#A7BBC7")
_cen["value"] = _var.value
_cen = gpd.GeoDataFrame(_cen)
_cen.rename(columns={0: "geometry"}, inplace=True)
_min = min(_cen["value"])
_max = max(_cen["value"]) 
polygon = _var.geometry.unary_union
gdf2 = gpd.GeoDataFrame(geometry=[polygon])
gdf2.boundary.plot(ax=fig_genesys_DT_LAU, color=_str, linewidth=0.5)
gdf2.plot(ax=fig_genesys_DT_LAU, color="lightgray")


"""
SOCIETAL COMMITMENT
"""
fig_genesys_SC_AT = fig.add_subplot(gs[1, 0])
_plot = Genesysmod.filter(scenario="Societal Commitment", year=2050)
_size = sum(_plot.data["value"])*0.27778

plot_first_column(_plot, fig_genesys_SC_AT)


fig_genesys_SC_AT.set_xticks([])
fig_genesys_SC_AT.set_yticks([])
fig_genesys_SC_AT.set_ylabel("Societal\nCommitment", fontsize=7, labelpad=6, multialignment='center')


_norm = sum(_plot.data["value"])*0.27778


fig_genesys_SC_AT.text(x=1.15, y=0.5, s=str(np.round(_norm,1))+" TWh", rotation="vertical", fontsize=6, ha="left", va="center")
fig_genesys_SC_NUTS3_LOW = fig.add_subplot(gs[1, 1])
fig_genesys_SC_NUTS3_LOW.set_xticks([])
fig_genesys_SC_NUTS3_LOW.set_yticks([])
_data = py.IamDataFrame("iamc_q_hat_subreg_plus.xlsx")
_plot = _data.filter(region="AT121", scenario="Societal Commitment")
ill = fig_genesys_SC_NUTS3_LOW.pie(_plot.data["value"], explode=[0,0,0,0,0])
_iter = 0
_colors = [_color[_key] for _key in _plot.variable]
for _patch in ill[0]:
    _patch.set_facecolor(_colors[_iter])
    _iter+=1
    
    
    
_norm = sum(_plot.data["value"])/1000000
fig_genesys_SC_NUTS3_LOW.text(x=1.1, y=-0.4, s=str(round(_norm,2))+" TWh", rotation="vertical", fontsize=5)

fig_genesys_SC_NUTS3_HIGH = fig.add_subplot(gs[1, 2])
fig_genesys_SC_NUTS3_HIGH.set_xticks([])
fig_genesys_SC_NUTS3_HIGH.set_yticks([])
_plot = _data.filter(region="AT342", scenario="Societal Commitment")
var = _plot.data.variable
val = _plot.data.values
tuples = dict(zip(var, val))
order = ["Geothermal", "Synthetic gas", "Hydrogen", "Waste", "Biomass", "Direct electric", "Heat pump (air)", "Heat pump (ground)", "Oil"]
val_ordered = [tuples.get(x)[6] for x in order]
colors = [_color[key] for key in order]
ill = fig_genesys_SC_NUTS3_HIGH.pie(x=val_ordered, colors=colors, startangle=200, radius=1, labels=None, frame=False, explode=[0.0, 0.05, 0.0, 0.05,0,0,0,0,0])
_true = [False, True, False, True, False, False, False, False, False]
i = 0
for _p in ill[0]:
    if _true[i]:
        _p.set_edgecolor(_str)
        _p.set_linewidth(0.5)
        _p.set_ls("solid")
    i+=1



_norm = sum(_plot.data["value"])/1000000
fig_genesys_SC_NUTS3_HIGH.text(x=1.3, y=-0.4, s=str(round(_norm,2))+" TWh", rotation="vertical", fontsize=5)
    
fig_genesys_SC_LAU = fig.add_subplot(gs[1, 3], frameon=False)
fig_genesys_SC_LAU.set_xticks([])
fig_genesys_SC_LAU.set_yticks([])


_var = gpd.read_file("Societal Commitment/generation.shp")
_boundary = gpd.read_file("Societal Commitment/polygons.shp")
_cen = _var.centroid.to_frame()
_boundary.boundary.plot(ax=fig_genesys_SC_LAU, linewidth=0.1, color="#A7BBC7")
_cen["value"] = _var.value
_cen = gpd.GeoDataFrame(_cen)
_cen.rename(columns={0: "geometry"}, inplace=True)
_min = min(_cen["value"])
_max = max(_cen["value"]) 
polygon = _var.geometry.unary_union
gdf2 = gpd.GeoDataFrame(geometry=[polygon])
gdf2.boundary.plot(ax=fig_genesys_SC_LAU, color=_str, linewidth=0.5)
gdf2.plot(ax=fig_genesys_SC_LAU, color="lightgray")








"""TECHNO-FRIENDLY"""
fig_genesys_TF_AT = fig.add_subplot(gs[2, 0])
_plot = Genesysmod.filter(scenario="Techno-Friendly", year=2050)
_size = sum(_plot.data["value"])*0.27778
plot_first_column(_plot, fig_genesys_TF_AT)

fig_genesys_TF_AT.set_xticks([])
fig_genesys_TF_AT.set_yticks([])
fig_genesys_TF_AT.set_ylabel("Techno-\nFriendly", fontsize=7, labelpad=6)
_norm = sum(_plot.data["value"])*0.27778
fig_genesys_TF_AT.text(x=1.15, y=0.5, s=str(np.round(_norm,1))+" TWh", rotation="vertical", fontsize=6, ha="left", va="center")



fig_genesys_TF_NUTS3_LOW = fig.add_subplot(gs[2, 1])
_plot = _data.filter(region="AT121", scenario="Techno-Friendly")
ill = _plot.plot.pie(cmap="tab20c", ax=fig_genesys_TF_NUTS3_LOW, legend=False, labels=None, radius=1, frame=False)
_iter = 0
_colors = [_color[_key] for _key in _plot.variable]
for _patch in ill.patches:
    _patch.set_facecolor(_colors[_iter])
    _iter+=1

_norm = sum(_plot.data["value"])/1000000
fig_genesys_TF_NUTS3_LOW.text(x=1.1, y=-0.4, s=str(round(_norm,2))+" TWh", rotation="vertical", fontsize=5)

fig_genesys_TF_NUTS3_HIGH = fig.add_subplot(gs[2, 2], frameon=False)
fig_genesys_TF_NUTS3_HIGH.set_xticks([])
fig_genesys_TF_NUTS3_HIGH.set_yticks([])


_plot = _data.filter(region="AT342", scenario="Techno-Friendly")
var = _plot.data.variable
val = _plot.data.values
tuples = dict(zip(var, val))
order = ["Geothermal", "Synthetic gas", "Hydrogen", "Waste", "Biomass", "Direct electric", "Heat pump (air)", "Heat pump (ground)", "Oil"]
val_ordered = [tuples.get(x)[6] for x in order]
colors = [_color[key] for key in order]
ill = fig_genesys_TF_NUTS3_HIGH.pie(x=val_ordered, colors=colors, startangle=200, radius=1, labels=None, frame=False, explode=[0.0, 0.05, 0.0, 0.05,0,0,0,0,0])
_true = [False, True, False, True, False, False, False, False, False]
i = 0
for _p in ill[0]:
    if _true[i]:
        _p.set_edgecolor(_str)
        _p.set_linewidth(0.5)
        _p.set_ls("solid")
    i+=1












_norm = sum(_plot.data["value"])/1000000
fig_genesys_TF_NUTS3_HIGH.text(x=1.3, y=-0.4, s=str(round(_norm,2))+" TWh", rotation="vertical", fontsize=5)



fig_genesys_TF_LAU = fig.add_subplot(gs[2, 3], frameon=False)
fig_genesys_TF_LAU.set_xticks([])
fig_genesys_TF_LAU.set_yticks([])
_var = gpd.read_file("Techno-Friendly/generation.shp")
_boundary = gpd.read_file("Techno-Friendly/polygons.shp")
_cen = _var.centroid.to_frame()
_boundary.boundary.plot(ax=fig_genesys_TF_LAU, linewidth=0.1, color="#A7BBC7")
_cen["value"] = _var.value
_cen = gpd.GeoDataFrame(_cen)
_cen.rename(columns={0: "geometry"}, inplace=True)
_min = min(_cen["value"])
_max = max(_cen["value"]) 
# _cen.plot(ax=fig_genesys_TF_LAU, marker="o", color=_str, markersize=15*_cen["value"], legend=False)
# _new_lines = gpd.read_file("Techno-Friendly/lines.shp")
# _new_lines.plot(ax=fig_genesys_TF_LAU, color=_str, linewidth=0.05)

polygon = _var.geometry.unary_union
gdf2 = gpd.GeoDataFrame(geometry=[polygon])
gdf2.boundary.plot(ax=fig_genesys_TF_LAU, color=_str, linewidth=0.5)
gdf2.plot(ax=fig_genesys_TF_LAU, color="lightgray")





fig_genesys_GD_AT = fig.add_subplot(gs[3, 0])
_plot = Genesysmod.filter(scenario="Gradual Development", year=2050)
_size = sum(_plot.data["value"])*0.27778

plot_first_column(_plot, fig_genesys_GD_AT)

fig_genesys_GD_AT.set_xticks([])
fig_genesys_GD_AT.set_yticks([])
fig_genesys_GD_AT.set_ylabel("Gradual\nDevelopment", fontsize=7, labelpad=6, multialignment='center')
fig_genesys_GD_AT.text(x=1.15, y=0.5, s=str(np.round(_size,1))+" TWh", rotation="vertical", fontsize=6, ha="left", va="center")



fig_genesys_GD_NUTS3_LOW = fig.add_subplot(gs[3, 1])
_plot = _data.filter(region="AT121", scenario="Gradual Development")
ill = _plot.plot.pie(cmap="tab20c", ax=fig_genesys_GD_NUTS3_LOW, legend=False, labels=None, radius=1, frame=False)
_iter = 0
_colors = [_color[_key] for _key in _plot.variable]
for _patch in ill.patches:
    _patch.set_facecolor(_colors[_iter])
    _iter+=1


_norm = sum(_plot.data["value"])/1000000
fig_genesys_GD_NUTS3_LOW.text(x=1.1, y=-0.4, s=str(round(_norm,2))+" TWh", rotation="vertical", fontsize=5)







_patches = []
for _key in _color.keys():
    if _key != "Oil":
        if _key == "Biomass":
            _label = _key
        elif _key == "Direct electric":
            _label = "Direct electric"
        elif _key == "Heat pump (air)":
            _label = "HP (air)"
        elif _key == "Heat pump (ground)":
            _label = "HP (ground)"
        elif _key == "Hydrogen":
            _label = _key
        elif _key == "Waste":
            _label = _key
        elif _key == "Geothermal":
            _label = _key
        elif _key == "Synthetic gas":
            _label = _key
        elif True:
            continue
        _patches.append(mpatches.Patch(color=_color[_key], label=_label))

_patches.append(mpatches.Patch(facecolor="lightgray", label="DH", edgecolor=_str,
                               linewidth=0.5))
    

# _line = Line2D([0], [0], label = 'Network-based heat supply',color=_str, linestyle="solid")

# _patches.extend([_line])

fig_genesys_GD_NUTS3_LOW.set_xlabel("AT121 Mostviertel-Eisenwurzen\n"+r'($\approx75~\frac{persons}{km^2}$)', fontsize=5, labelpad=0, multialignment='center')
fig_genesys_GD_NUTS3_HIGH = fig.add_subplot(gs[3, 2], frameon=False)
fig_genesys_GD_NUTS3_HIGH.set_xticks([])
fig_genesys_GD_NUTS3_HIGH.set_yticks([])
fig_genesys_GD_NUTS3_HIGH.set_xlabel("AT342 Rheintal-Bodenseegebiet\n"+r'(>$450~\frac{persons}{km^2}$)', fontsize=5, labelpad=0, multialignment='center')



_plot = _data.filter(region="AT342", scenario="Gradual Development")

var = _plot.data.variable
val = _plot.data.values
tuples = dict(zip(var, val))
order = ["Geothermal", "Synthetic gas", "Hydrogen", "Waste", "Biomass", "Direct electric", "Heat pump (air)", "Heat pump (ground)", "Oil"]
val_ordered = [tuples.get(x)[6] for x in order]
colors = [_color[key] for key in order]
ill = fig_genesys_GD_NUTS3_HIGH.pie(x=val_ordered, colors=colors, startangle=200, radius=1, labels=None, frame=False, explode=[0.0, 0.05, 0.0, 0.05,0,0,0,0,0])
_true = [False, True, False, True, False, False, False, False, False]
i = 0
for _p in ill[0]:
    if _true[i]:
        _p.set_edgecolor(_str)
        _p.set_linewidth(0.5)
        _p.set_ls("solid")
    i+=1








_norm = sum(_plot.data["value"])/1000000
fig_genesys_GD_NUTS3_HIGH.text(x=1.3, y=-0.4, s=str(round(_norm,2))+" TWh", rotation="vertical", fontsize=5)




fig_genesys_GD_LAU = fig.add_subplot(gs[3, 3], frameon=False)
fig_genesys_GD_LAU.set_xticks([])
fig_genesys_GD_LAU.set_yticks([])
fig_genesys_GD_LAU.set_xlabel("AT342 Rheintal-Bodenseegebiet\n(incl. 48 communities)", fontsize=5, labelpad=0, multialignment='center')



_var = gpd.read_file("Gradual Development/generation.shp")
_boundary = gpd.read_file("Gradual Development/polygons.shp")
_cen = _var.centroid.to_frame()
_boundary.boundary.plot(ax=fig_genesys_GD_LAU, linewidth=0.1, color="#A7BBC7")
_cen["value"] = _var.value
_cen = gpd.GeoDataFrame(_cen)
_cen.rename(columns={0: "geometry"}, inplace=True)
_min = min(_cen["value"])
_max = max(_cen["value"]) 
polygon = _var.geometry.unary_union
gdf2 = gpd.GeoDataFrame(geometry=[polygon])
gdf2.boundary.plot(ax=fig_genesys_GD_LAU, color=_str, linewidth=0.5)
gdf2.plot(ax=fig_genesys_GD_LAU, color="lightgray")





fig.suptitle("Heat generation at the country, sub-region, and community levels")
plt.tight_layout(h_pad=0)
fig_genesys_DT_AT.legend(handles=_patches, loc='upper center', fontsize=6, framealpha=1, handlelength=0.7, handletextpad=0.3, ncol=9, bbox_to_anchor=(3.7, 1.675), borderpad=0.35, columnspacing=1)

fig.savefig("Result.png", dpi=500)
fig.savefig("Spatial_results.eps", format="eps")