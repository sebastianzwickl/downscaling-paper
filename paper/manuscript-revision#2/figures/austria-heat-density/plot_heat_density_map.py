import pyam
import geopandas
import numpy
import matplotlib
import matplotlib.pyplot as plt
from pyproj import Geod
from matplotlib.lines import Line2D
from shapely import geometry, ops
from matplotlib_scalebar.scalebar import ScaleBar

plt.style.use(["science"])
plt.rcParams['xtick.labelsize'] = 6
plt.rcParams['ytick.labelsize'] = 6
plt.rcParams["figure.figsize"] = (4.5, 3)

data = pyam.IamDataFrame('high-heat-density-lau-10.xlsx').data
maxval = max(data["value"]) 

shp = geopandas.read_file('lau-shp/at-laus.shp')
shp.rename(columns={'YEAR': 'Heat Density'}, inplace=True)

for index, row in shp.iterrows():
    heat_density = data[data['region'] == int(row['LAU_ID'])]['value']
    if heat_density.empty:
        shp.loc[index, 'Heat Density'] = 0
    else:
        shp.loc[index, 'Heat Density'] = heat_density.item()

fig, axes = plt.subplots(nrows=1, ncols=1)
shp.boundary.plot(ax=axes, linewidth=0.02, color='black')
axes.axis('off')

cvals  = [0, 45]
colors = ['white', '#3E497A']

norm=plt.Normalize(min(cvals),max(cvals))
norm1 = matplotlib.colors.Normalize(vmin=0, vmax=45)
tuples = list(zip(map(norm1,cvals), colors))

cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", tuples)


# cmap = matplotlib.cm.get_cmap("binary", numpy.ceil(maxval))


shp.plot(ax=axes, legend=False, cmap=cmap, norm=norm, column='Heat Density')

shp_filter = shp[shp['Heat Density'] != 0]
shp_filter.boundary.plot(ax=axes, linewidth=0.25, color='black')

cbar_ax = fig.add_axes([0.05, 0.7, 0.3, 0.015])
cb1 = matplotlib.colorbar.ColorbarBase(ax=cbar_ax, cmap=cmap, norm=norm1, orientation="horizontal")
cbar_ax.set_xlabel(r"in $\frac{GWh}{km^2}$", fontsize=8)
cbar_ax.xaxis.set_label_coords(0.5, 5)
cbar_ax.xaxis.set_ticks([0,15, 30, 45])
cbar_ax.tick_params(axis='x', labelsize= 8, pad=2)

polygon = shp.geometry.unary_union
gdf2 = geopandas.GeoDataFrame(geometry=[polygon])
gdf2.boundary.plot(ax=axes, linewidth=0.25, color='black')

LineString = geometry.LineString([[9, 0], [10,0]])
geod = Geod(ellps="WGS84")
Ref_Length = geod.geometry_length(LineString) / 1000
    
scale1 = ScaleBar(
    dx=1,
    location='lower left',
    label_loc='left', scale_loc='bottom',
    label_formatter=lambda value, unit: '50km',
    height_fraction=0.005,
    length_fraction=0.08,
    font_properties={'size': 6},
    pad=0)

axes.text(x=0.95, y=0.165, s='Scenario: Directed Transition', transform=fig.transFigure, fontsize=6, ha='right')
    
axes.add_artist(scale1)
axes.set_title('Heat density of district heating in 2050', fontsize=10)

plt.tight_layout()
fig.savefig("austria-laus.eps", format="eps")
fig.savefig("austria-laus.png", dpi=500)