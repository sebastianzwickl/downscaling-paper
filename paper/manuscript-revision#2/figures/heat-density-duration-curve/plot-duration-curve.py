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

fig = plt.figure(constrained_layout=False)
gs = fig.add_gridspec(2, 3)

figtop = fig.add_subplot(gs[0, :])
figtop.minorticks_off()

figleft = fig.add_subplot(gs[1, 0])
figleft.minorticks_off()

figmid = fig.add_subplot(gs[1, 1])
figmid.minorticks_off()

figright = fig.add_subplot(gs[1, 2])
figright.minorticks_off()

dt = sorted(pyam.IamDataFrame('dt-heat-density.xlsx').data['value'].values, reverse=True)
x_val = range(0, len(dt), 1)

figtop.plot(x_val, dt, marker='+', linewidth=0.75, markersize=2, color='#3E497A')
figtop.plot(x_val, len(dt)*[10], linewidth=0.5, color='#D9534F')
figtop.text(x=0, y=6, s='Required heat density for economic viability', ha='left', fontsize=4, color='#D9534F')
# figtop.text(x=5, y=30.67, s="String", fontsize=2)
figtop.set_ylabel('Heat density '+r"in $\frac{GWh}{km^2}$", fontsize=6)
figtop.set_xlabel('Local administrative units / districts', fontsize=6)

figtop.annotate(
    'High heat density areas (e.g., Salzburg city)',
    fontsize=5,
    color="black",
    multialignment='left',
    va="top",
    xy=(5, 32), xycoords='data',
    xytext=(17.5, 37), textcoords='data',
    arrowprops=dict(headlength=3, 
                    headwidth=1.5,
                    width=0.05,
                    connectionstyle="arc3,rad=.3",
                    color="black",
                    linewidth=0.5))

figtop.annotate(
    'Surrounding areas (e.g., Anif)',
    fontsize=5,
    color="black",
    multialignment='left',
    va="top",
    xy=(82, 9), xycoords='data',
    xytext=(52.5, 25), textcoords='data',
    arrowprops=dict(headlength=3, 
                    headwidth=1.5,
                    width=0.05,
                    connectionstyle="arc3,rad=-0.2",
                    color="black",
                    linewidth=0.5))

# figtop.text(x=105/2, y=30, s='District heating\n network',
#         rotation=0, fontsize=7, color='#A1B57D',
#         ha='center', va='center', bbox=dict(facecolor="white", edgecolor="#444941", boxstyle='round,pad=0.5', linestyle='solid',
#                                               linewidth=0.75), zorder=100)



sc = sorted(pyam.IamDataFrame('sc-heat-density.xlsx').data['value'].values, reverse=True)
figleft.plot(x_val, sc, linewidth=0.75, color='#3E497A')
figleft.plot(x_val, len(sc)*[10], linewidth=0.5, color='#D9534F')
figleft.set_title('Societal Commitment', fontsize=6)

tf = sorted(pyam.IamDataFrame('tf-heat-density.xlsx').data['value'].values, reverse=True)
x_val = range(0, len(tf), 1)
figmid.plot(x_val, tf, linewidth=0.75, color='#3E497A')
figmid.plot(x_val, len(tf)*[10], linewidth=0.5, color='#D9534F')
figmid.set_title('Techno-Friendly', fontsize=6)

gd = sorted(pyam.IamDataFrame('gd-heat-density.xlsx').data['value'].values, reverse=True)
x_val = range(0, len(gd), 1)
figright.plot(x_val, gd, linewidth=0.75, color='#3E497A')
figright.plot(x_val, len(gd)*[10], linewidth=0.5, color='#D9534F')
figright.set_title('Gradual Development', fontsize=6)

figtop.set_title('Directed Transition', fontsize=6)

# fig.suptitle('Heat density of district heating in LAUs '+r"in $\frac{GWh}{km^2}$", y=0.925, fontsize=10)

plt.tight_layout()
fig.savefig("heat-density-duration.eps", format="eps")
fig.savefig("heat-density-duration.png", dpi=900)