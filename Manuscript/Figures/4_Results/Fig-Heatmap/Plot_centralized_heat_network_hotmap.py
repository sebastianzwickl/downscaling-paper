import geopandas as gpd
import matplotlib.pyplot as plt
import pyam
import matplotlib
import numpy as np

plt.style.use("seaborn-paper")
file = gpd.read_file("Shapefile/NUTS_RG_10M_2021_3035_LEVL_3.shp")
file = file.loc[file["CNTR_CODE"] == "AT"]
_scenarios = ["Directed Transition", "Societal Commitment", "Techno-Friendly", "Gradual Development"]



    
    
centralized = pyam.IamDataFrame('Results_Centralized+Decentralized-Heat-generation.xlsx')
# centralized.filter(variable="Centralized", inplace=True)
    
max_value = max(centralized.filter(variable="Centralized").data["value"]) 



centralized = centralized.data.rename(columns={"region": "NUTS_ID"})
full = centralized.merge(file, on="NUTS_ID")
full.drop(columns=["model", "LEVL_CODE","CNTR_CODE", "NAME_LATN", "NUTS_NAME", "MOUNT_TYPE", "URBN_TYPE", "COAST_TYPE", "FID"], inplace=True)



_plot_heat_map = True
if _plot_heat_map:
    
    fig, _axes = plt.subplots(nrows=2, ncols=2)
    
    cmap = matplotlib.cm.get_cmap("Blues", int(max_value+1))
    norm = matplotlib.colors.Normalize(vmin=0, vmax=int(max_value+1))

    
    
    
    
    cbar_ax = fig.add_axes([0.4, 0.05, 0.3, 0.015])
    cb1 = matplotlib.colorbar.ColorbarBase(ax=cbar_ax, cmap=cmap, norm=norm, orientation="horizontal")
    cbar_ax.set_xlabel("Heat demand supplied in TWh", fontsize=8)
    cbar_ax.xaxis.set_label_coords(0.5, 3.1)
    cbar_ax.xaxis.set_ticks([0,2,4,6,8,10,12])
    
    for _var in tuple(zip(_scenarios, _axes.flat)):
        _to_plot = gpd.GeoDataFrame(full.loc[full["scenario"]==_var[0]])
        _to_plot.boundary.plot(ax=_var[1], linewidth=1, color="#D1D9D9")
        _to_plot = _to_plot.loc[full["variable"]=="Centralized"]
        _to_plot.plot(column="value", ax=_var[1], legend=False, cmap=cmap, vmin=0, vmax=8)
        _var[1].axis('off')
        _var[1].set_title(_var[0],x=0.65)
        
        if _var[0] == "Societal Commitment":
            for _place in _to_plot.itertuples(index=True):
                if _place.NUTS_ID == "AT130":
                    _x = 10000
                    _y = 10000
                    _var[1].annotate("", xy=(_place.geometry.centroid.x, _place.geometry.centroid.y), xytext=(_place.geometry.centroid.x+2*_x, _place.geometry.centroid.y+2*_y), textcoords='data', arrowprops=dict(arrowstyle="-", connectionstyle="arc3", color="black", linewidth=0.5))
                    
                else:
                    _x=0
                    _y=0
                    
                _var[1].text(_place.geometry.centroid.x+2*_x, _place.geometry.centroid.y+2*_y, _place.NUTS_ID, fontsize=6)
                

        

    
    _rectangle_axes = plt.axes([0.378, 0.263, 0.3, 0.3])
    # _rectangle_axes.set_xticks([])
    # _rectangle_axes.set_yticks([])
    _rectangle_axes.axis("off")
    _color="#FB9300"
    _rectangle_axes.plot([0.82,0.82], [1.15,1.165], color=_color, linewidth=0.5)
    _rectangle_axes.plot([0.87,0.87], [1.15,1.165], color=_color, linewidth=0.5)
    _rectangle_axes.plot([0.82,0.87], [1.15,1.15], color=_color, linewidth=0.5)
    _rectangle_axes.plot([0.82,0.87], [1.165,1.165], color=_color, linewidth=0.5)
    _rectangle_axes.plot([0.95,0.95], [1.2,1.25], color=_color, linewidth=0)
    _rectangle_axes.plot([1,1], [1.2,1.25], color=_color, linewidth=0)
    _rectangle_axes.plot([0.95,1], [1.25,1.25], color=_color, linewidth=0)
    
    _rectangle_axes.plot([0.87,0.99025], [1.15,1.1799], color=_color, linewidth=0.5)
    
    
    
    
    
    _rectangle_axes.plot([0.82,0.8622], [1.165,1.2237], color=_color, linewidth=0.5)
    _rectangle_axes.set_ylim([1.145, 1.25])
    _rectangle_axes.set_xlim([0.8125, 1.005])
    
    # plt.plot([0,1], [1,2], color=_color)
    
    
    sub_axes = plt.axes([.455, .325, .2, .2]) 
    # sub_axes.pie([0.6, 0.4]) 
    sub_axes.set_xticks([])
    sub_axes.set_yticks([])
    sub_axes.spines['bottom'].set_color(_color)
    sub_axes.spines['bottom'].set_linewidth(0.5)
    sub_axes.spines['top'].set_color(_color)
    sub_axes.spines['top'].set_linewidth(0.5)
    sub_axes.spines['right'].set_color(_color)
    sub_axes.spines['right'].set_linewidth(0.5)
    sub_axes.spines['left'].set_color(_color)
    sub_axes.spines['left'].set_linewidth(0.5)

    _boundary = gpd.read_file("Shapefile/boundary.shp")
    _boundary.boundary.plot(ax=sub_axes, linewidth=0.2, color="#A7BBC7")
    
    
    
    fig.suptitle("Heat demand supplied by centralized heat networks in TWh")                                  
    plt.tight_layout()
    fig.savefig("Heatmap.eps", format="eps")
    fig.savefig("Heatmap.png", dpi=500)
    
    
        
    
