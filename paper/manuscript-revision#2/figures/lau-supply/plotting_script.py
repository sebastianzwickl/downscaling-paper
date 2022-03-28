"""Plotting script the net present value of the six different sceanrios."""
import pyam
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mlp
import matplotlib.ticker as tkr
import geopandas as gpd
import pandas as pd
from pyproj import Geod
from matplotlib.lines import Line2D
from matplotlib_scalebar.scalebar import ScaleBar
from shapely import geometry, ops
import numpy as np
import matplotlib.patches as mpatches


plt.style.use(['science'])
plt.rcParams['xtick.labelsize'] = 5
plt.rcParams['ytick.labelsize'] = 5
plt.rc('legend', fontsize=5)

lau = gpd.read_file('lau-shp/at-laus.shp')

list_m = {
    '50101' : '*',
    '50205' : "+",
    '50301' : "s",
    '50309' : "3",
    '50314' : "."
    }

list_size = {
    '50101' : 12,
    '50205' : 8,
    '50301' : 5,
    '50309' : 10,
    '50314' : 14
    }




fig = plt.figure(constrained_layout=False)
gs = fig.add_gridspec(2, 3)

fig11 = fig.add_subplot(gs[0, 0])
fig11.minorticks_off()
fig12 = fig.add_subplot(gs[0, 1:3])
fig12.minorticks_off()


fig21 = fig.add_subplot(gs[1, 0])
fig21.minorticks_off()
fig22 = fig.add_subplot(gs[1, 1:3])
fig22.minorticks_off()




nuts3_lau = pd.read_excel('Allocating_LAU_to_NUTS3_1.1.2020.xlsx')
sel_nuts3 = nuts3_lau[nuts3_lau['NUTS3 NAME'] == 'Salzburg und Umgebung']
sel_nuts3['LAU ID'] = sel_nuts3['LAU ID'].astype('str')
lau_salzburg = lau[lau.LAU_ID.isin(sel_nuts3['LAU ID'])]


# """directed transition"""
data = pyam.IamDataFrame("dt-heat-density.xlsx")
regions = data.data['region']

col_reg = dict(zip(regions, len(regions)*['#3E497A']))

list_of_markers = [list_m.get(x, "d") for x in lau_salzburg.LAU_ID]

lau_salzburg.plot(ax=fig11, color=[col_reg.get(int(x), '#ECECEC') for x in lau_salzburg.LAU_ID])
lau_salzburg.boundary.plot(ax=fig11, color='black', linewidth=0.05)

# for element in list_m.keys():
temp = lau_salzburg[lau_salzburg.LAU_ID == '50101']
temp.boundary.plot(ax=fig11, color='orange')

temp = lau_salzburg[lau_salzburg.LAU_ID == '50201']
temp.boundary.plot(ax=fig11, color='green')



fig11.set_xlabel("")
fig11.set_ylabel("")

LineString = geometry.LineString([[4,0], [5,0]])
geod = Geod(ellps="WGS84")
Ref_Length = geod.geometry_length(LineString) / 1000

scale1 = ScaleBar(
    dx=1,
    location='lower left',
    label_loc='left', scale_loc='bottom',
    label_formatter=lambda value, unit: '10km',
    height_fraction=0.005,
    length_fraction=0.2,
    font_properties={'size': 4},
    pad=-0.5)
    
fig11.add_artist(scale1)

fig11.spines["top"].set_visible(False)
fig11.spines["right"].set_visible(False)
fig11.spines["bottom"].set_visible(False)
fig11.spines["left"].set_visible(False)
fig11.get_xaxis().set_ticks([])
fig11.get_yaxis().set_ticks([])

_color = {
    "Biomass": "#b3de69",
    "Direct electric": "#ffffb3",
    "Geothermal": "#C69B7B",
    "Synthetic gas" : "#d9d9d9",
    "Heat pump (air) large": "#A2D2FF",
    "Heat pump (air) small": "#577BC1",
    "Heat pump (ground)": "#8dd3c7",
    "Hydrogen": "#fccde5",
    "Waste":"#712B75",
    
    }

_str = "#04009A"
_patches = []
_patches.append(mpatches.Patch(facecolor="#3E497A", label="Urban LAU with DH", edgecolor="orange",
                               linewidth=0.5))

_patches.append(mpatches.Patch(facecolor="#ECECEC", label="Rural LAU with no DH", edgecolor="green",
                               linewidth=0.5))
_patches.append(mpatches.Patch(facecolor="None", label="", edgecolor="green",
                               linewidth=0))
_patches.append(mpatches.Patch(facecolor="None", label="Heat sources / technologies", edgecolor="green",
                               linewidth=0))


for _key in _color.keys():
    if _key != "Oil":
        if _key == "Biomass":
            _label = _key
        elif _key == "Direct electric":
            _label = "Direct electric"
        elif _key == "Heat pump (air) large":
            _label = "Large-scale HP (air)"
        elif _key == "Heat pump (air) small":
            _label = "Small-scale HP (air)"
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




leg = fig21.legend(
    handles=_patches,
    loc="center",
    fontsize=4,
    framealpha=1,
    handlelength=1,
    handletextpad=1,
    borderpad=0.75,
    columnspacing=1,
    edgecolor="#161616",
    frameon=True,
    ncol=1,
)

fig21.spines["top"].set_visible(False)
fig21.spines["right"].set_visible(False)
fig21.spines["bottom"].set_visible(False)
fig21.spines["left"].set_visible(False)
fig21.get_xaxis().set_ticks([])
fig21.get_yaxis().set_ticks([])

leg.get_frame().set_linewidth(0.15)

fig12.set_title('Heat supply in urban LAU with DH in '+r'$TWh$', fontsize=5)
fig22.set_title('Heat supply in rural LAU with no DH in '+r'$MWh$', fontsize=5)


fig12.set_xticks([0, 1, 2, 3])
fig12.set_xticklabels(labels=['DT', 'SC', 'TF', 'GD'])
# fig12.set_xlim([-0.6, 1.6])

# fig13.set_xticks([0, 1])
# fig13.set_xticklabels(labels=['Urban', 'Rural'])
# fig13.set_xlim([-0.6, 1.6])

fig22.set_xticks([0, 1, 2, 3])
fig22.set_xticklabels(labels=['DT', 'SC', 'TF', 'GD'])


# fig23.set_xticks([0, 1])
# fig23.set_xticklabels(labels=['Urban', 'Rural'])
# fig23.set_xlim([-0.6, 1.6])


dt_urb_total = 0.89
fig12.bar(0, dt_urb_total*0.68, color='#A2D2FF', width=0.5)
fig12.bar(0, dt_urb_total*0.06, bottom=dt_urb_total*0.68, color='#fccde5', width=0.5)
fig12.bar(0, dt_urb_total*0.12, bottom=dt_urb_total*0.74, color='#712B75', width=0.5)
fig12.bar(0, dt_urb_total*0.12, bottom=dt_urb_total*0.86, color='#C69B7B', width=0.5)
rect = fig12.bar(0, dt_urb_total*0.02, bottom=dt_urb_total*0.98, color='#d9d9d9', width=0.5)
fig12.bar_label(rect, padding=0.5, fontsize=5)
fig12.set_ylim([0, 1.1])


sc_urb_total = 0.84
fig12.bar(1, sc_urb_total*0.51, color='#A2D2FF', width=0.5)
fig12.bar(1, sc_urb_total*0.14, bottom=sc_urb_total*0.51, color='#fccde5', width=0.5)
fig12.bar(1, sc_urb_total*0.13, bottom=sc_urb_total*0.65, color='#712B75', width=0.5)
fig12.bar(1, sc_urb_total*0.13, bottom=sc_urb_total*0.78, color='#C69B7B', width=0.5)
rect = fig12.bar(1, sc_urb_total*0.09, bottom=sc_urb_total*0.91, color='#d9d9d9', width=0.5)
fig12.bar_label(rect, padding=0.5, fontsize=5)



tf_urb_total = 0.87
fig12.bar(2, tf_urb_total*0.48, color='#A2D2FF', width=0.5)
fig12.bar(2, tf_urb_total*0.27, bottom=tf_urb_total*0.48, color='#fccde5', width=0.5)
fig12.bar(2, tf_urb_total*0.07, bottom=tf_urb_total*0.75, color='#712B75', width=0.5)
fig12.bar(2, tf_urb_total*0.07, bottom=tf_urb_total*0.82, color='#C69B7B', width=0.5)
rect = fig12.bar(2, tf_urb_total*0.11, bottom=tf_urb_total*0.89, color='#d9d9d9', width=0.5)
fig12.bar_label(rect, padding=0.5, fontsize=5)



gd_urb_total = 0.91
fig12.bar(3, gd_urb_total*0.21, color='#A2D2FF', width=0.5)
fig12.bar(3, gd_urb_total*0.38, bottom=gd_urb_total*0.21, color='#fccde5', width=0.5)
fig12.bar(3, gd_urb_total*0.09, bottom=gd_urb_total*0.59, color='#712B75', width=0.5)
fig12.bar(3, gd_urb_total*0.09, bottom=gd_urb_total*0.68, color='#C69B7B', width=0.5)
rect = fig12.bar(3, gd_urb_total*0.23, bottom=gd_urb_total*0.77, color='#d9d9d9', width=0.5)
fig12.bar_label(rect, padding=0.5, fontsize=5)


dt_rur_total = 34.01
fig22.bar(0, dt_rur_total*0.51, bottom=0, color='#8dd3c7', width=0.5)
fig22.bar(0, dt_rur_total*0.33, bottom=0.51*dt_rur_total, color='#577BC1', width=0.5)
fig22.bar(0, dt_rur_total*0.06, bottom=dt_rur_total*0.84, color='#ffffb3', width=0.5)
rect = fig22.bar(0, dt_rur_total*0.1, bottom=dt_rur_total*0.9, color='#b3de69', width=0.5)
fig22.bar_label(rect, padding=0.5, fontsize=5)

sc_rur_total = 31.96
fig22.bar(1, sc_rur_total*0.6, bottom=sc_rur_total*0.0, color='#8dd3c7', width=0.5)
fig22.bar(1, sc_rur_total*0.24, bottom=sc_rur_total*0.60, color='#577BC1', width=0.5)
fig22.bar(1, sc_rur_total*0.06, bottom=sc_rur_total*0.84, color='#ffffb3', width=0.5)
rect = fig22.bar(1, sc_rur_total*0.1, bottom=sc_rur_total*0.9, color='#b3de69', width=0.5)
fig22.bar_label(rect, padding=0.5, fontsize=5)

tf_rur_total = 33.11
fig22.bar(2, tf_rur_total*0.21, color='#8dd3c7', width=0.5)
fig22.bar(2, tf_rur_total*0.57, bottom=tf_rur_total*0.21, color='#577BC1', width=0.5)
fig22.bar(2, tf_rur_total*0.07, bottom=tf_rur_total*0.78, color='#ffffb3', width=0.5)
rect = fig22.bar(2, tf_rur_total*0.15, bottom=tf_rur_total*0.85, color='#b3de69', width=0.5)
fig22.bar_label(rect, padding=0.5, fontsize=5)

gd_rur_total = 34.63
fig22.bar(3, gd_rur_total*0.66, color='#8dd3c7', width=0.5)
fig22.bar(3, gd_rur_total*0.17, bottom=gd_rur_total*0.66, color='#577BC1', width=0.5)
fig22.bar(3, gd_rur_total*0.06, bottom=gd_rur_total*0.83, color='#ffffb3', width=0.5)
rect = fig22.bar(3, gd_rur_total*0.11, bottom=gd_rur_total*0.89, color='#b3de69', width=0.5)
fig22.bar_label(rect, padding=0.5, fontsize=5)

fig22.set_ylim([0, 45])

plt.tight_layout()
fig.savefig("supply-salzburg-lau.eps", format="eps")
fig.savefig("supply-salzburg-lau.png", dpi=900)
