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
gs = fig.add_gridspec(4, 4)

fig_left_up = fig.add_subplot(gs[:, 0:2])
fig_left_up.minorticks_off()
fig_right_up = fig.add_subplot(gs[0:2, 2:4])
fig_right_up.minorticks_off()
fig_right_down = fig.add_subplot(gs[2:4, 2:4])
fig_right_down.minorticks_off()

nuts3_lau = pd.read_excel('Allocating_LAU_to_NUTS3_1.1.2020.xlsx')
sel_nuts3 = nuts3_lau[nuts3_lau['NUTS3 NAME'] == 'Salzburg und Umgebung']
sel_nuts3['LAU ID'] = sel_nuts3['LAU ID'].astype('str')
lau_salzburg = lau[lau.LAU_ID.isin(sel_nuts3['LAU ID'])]


"""directed transition"""
data = pyam.IamDataFrame("dt-heat-density.xlsx")


regions = data.data['region']

col_reg = dict(zip(regions, len(regions)*['#3E497A']))

list_of_markers = [list_m.get(x, "d") for x in lau_salzburg.LAU_ID]

lau_salzburg.plot(ax=fig_left_up, color=[col_reg.get(int(x), '#ECECEC') for x in lau_salzburg.LAU_ID])
lau_salzburg.boundary.plot(ax=fig_left_up, color='black', linewidth=0.05)

for element in list_m.keys():
    temp = lau_salzburg[lau_salzburg.LAU_ID == element]
    marker = list_m[element]
    size = list_size[element]
    temp.centroid.plot(ax=fig_left_up, color='white', marker=marker, markersize=size)



fig_left_up.set_xlabel("")
fig_left_up.set_ylabel("")

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
    
fig_left_up.add_artist(scale1)

fig_left_up.spines["top"].set_visible(False)
fig_left_up.spines["right"].set_visible(False)
fig_left_up.spines["bottom"].set_visible(False)
fig_left_up.spines["left"].set_visible(False)
fig_left_up.get_xaxis().set_ticks([])
fig_left_up.get_yaxis().set_ticks([])

fig_left_up.set_title('Salzburg and surroundings\n(AT323)', fontsize=5)

_patches = []
_line = Line2D(
    [0],
    [0],
    label="District Heating",
    color='#3E497A',
    linewidth=2,
    linestyle="solid",
)
_patches.extend([_line])
_line = Line2D(
    [0],
    [0],
    label="On-Site / Dec.",
    color='#ECECEC',
    linewidth=2,
    linestyle="solid",
)
_patches.extend([_line])

leg = fig_left_up.legend(
    handles=_patches,
    loc="lower center",
    fontsize=4,
    framealpha=1,
    handlelength=1,
    handletextpad=1,
    borderpad=0.75,
    columnspacing=1,
    edgecolor="#161616",
    frameon=True,
    bbox_to_anchor=(0.5, -0.2),
    ncol=2,
)

leg.get_frame().set_linewidth(0.15)

fig_right_up.set_title('District heating in $GWh$', fontsize=5)

dt_dh = pyam.IamDataFrame('dt-heat-supply.xlsx').filter(variable='District heating')
sum_dt_dh = np.round(sum(dt_dh.data['value']) / 1000, 0)

sc_dh = pyam.IamDataFrame('sc-heat-supply.xlsx').filter(variable='District heating')
sum_sc_dh = np.round(sum(sc_dh.data['value']) / 1000, 0)

tf_dh = pyam.IamDataFrame('tf-heat-supply.xlsx').filter(variable='District heating')
sum_tf_dh = np.round(sum(tf_dh.data['value']) / 1000, 0)

gd_dh = pyam.IamDataFrame('gd-heat-supply.xlsx').filter(variable='District heating')
sum_gd_dh = np.round(sum(gd_dh.data['value']) / 1000, 0)

y = [sum_dt_dh, sum_sc_dh, sum_tf_dh, sum_gd_dh]

x = [0, 1, 2, 3]

rects = fig_right_up.bar(x, y, color='#3E497A')
fig_right_up.set_ylim([0, 1350])

fig_right_up.bar_label(rects, padding=0, fontsize=5)

fig_right_up.set_xticks(ticks=[0, 1, 2, 3])
fig_right_up.set_xticklabels(labels=['DT', 'SC', 'TF', 'GD'])


fig_right_down.set_title('Heat density '+r"in $\frac{GWh}{km^2}$", fontsize=5)

fig_right_down.scatter(0,30.7,marker='*',color='#3E497A',s=8)
fig_right_down.scatter(0,14.6,marker='+',color='#3E497A',s=10)
fig_right_down.scatter(0,7.3,marker='s',color='#3E497A',s=6)
fig_right_down.scatter(0,6.1,marker='3',color='#3E497A',s=10)
fig_right_down.scatter(0,10.8,marker='.',color='#3E497A',s=8)

fig_right_down.scatter(1,28.8,marker='*',color='#3E497A',s=8)
fig_right_down.scatter(1,13.7,marker='+',color='#3E497A',s=10)
fig_right_down.scatter(1,6.8,marker='s',color='#3E497A',s=6)
fig_right_down.scatter(1,5.7,marker='3',color='#3E497A',s=10)
fig_right_down.scatter(1,10.0,marker='.',color='#3E497A',s=8)

fig_right_down.scatter(2,29.9,marker='*',color='#3E497A',s=8)
fig_right_down.scatter(2,14.2,marker='+',color='#3E497A',s=10)
fig_right_down.scatter(2,7.1,marker='s',color='#3E497A',s=6)
fig_right_down.scatter(2,6.0,marker='3',color='#3E497A',s=10)
fig_right_down.scatter(2,10.3,marker='.',color='#3E497A',s=8)

fig_right_down.scatter(3,31.2,marker='*',color='#3E497A',s=8)
fig_right_down.scatter(3,14.8,marker='+',color='#3E497A',s=10)
fig_right_down.scatter(3,7.4,marker='s',color='#3E497A',s=6)
fig_right_down.scatter(3,6.2,marker='3',color='#3E497A',s=10)
fig_right_down.scatter(3,10.8,marker='.',color='#3E497A',s=8)

fig_right_down.set_xticks([0, 1, 2, 3])
fig_right_down.set_xlim([-0.5, 3.5])
fig_right_down.set_ylim([0, 40])

fig_right_down.set_xticklabels(labels=['DT', 'SC', 'TF', 'GD'])


plt.tight_layout()
fig.savefig("network-salzburg.eps", format="eps")
fig.savefig("network-salzburg.png", dpi=900)
