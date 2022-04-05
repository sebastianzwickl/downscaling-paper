import matplotlib.pyplot as plt
import pandas as pd
import os
import geopandas as gpd
import pyam

from datetime import datetime
from itertools import combinations
from pathlib import Path

from utils import make_networkx_from_shapefile
from utils import add_quantities_to_nodes
from utils import calculate_cluster_coefficient
from utils import calculate_distance_coefficient
from utils import calculate_total_indicator_value


def iterative_downscaling(init_quantities=None, lines=None):

    """

    Parameters
    ----------
    init_quantities : Shapefile, required
        Includes the quantities of centralized and decentralized
        heat generation per region on the local (LAU) level.
        The quantities need to be from the same scenario and NUTS3 region.
        The default is None.
    lines : Shapefile, required
        Includes the connection lines between the nodes on the local level (LAU).
        The default is None.

    Returns
    -------
    final_cen_generation : Shapefile
        Includes the shapefile with the final centralized heat generation.
    final_lines : Shapefile
        Includes the shapefile with final connection lines between nodes.
    benchmark_df : DataFrame
        Includes the benchmark indicator values of nodes.

    """

    # Add connection lines with switched start and end nodes
    _inverted_lines = lines.rename(columns={"START": "END", "END": "START"})
    lines = lines.append(_inverted_lines)

    # Create networkx graph from shapefiles
    graph = make_networkx_from_shapefile(lines)
    graph = add_quantities_to_nodes(graph, init_quantities)

    # nodes = len(graph._node.keys())

    _benchmarks = list()
    _removed_pop = list()
    _pop_lau_level = pd.read_excel("data\Population_on_LAU_level_in_2050.xlsx")
    _lau_and_code = pd.read_excel("data\LAU_and_CODE.xlsx")
    
    

    while True:
        cluster_coefficient = calculate_cluster_coefficient(graph)
        distance_coefficient = calculate_distance_coefficient(graph)
        indicators = calculate_total_indicator_value(
            cluster_coefficient, distance_coefficient
        )

        _benchmarks.append(list(indicators.values()))

        for key in indicators.keys():
            if indicators[key] == min(indicators.values()):
                node_to_drop = key
        # print("Node that is removed from graph: " + node_to_drop)
        _lau_name = node_to_drop.split("|")[1]
        _lau_code = _lau_and_code.loc[_lau_and_code.LAU_NAME == _lau_name]["LAU_CODE"].item()
        # print(_lau_code)
        _pop = _pop_lau_level.loc[_pop_lau_level.region == _lau_code][2050].item()
        # print(_pop)
        _removed_pop.append(_pop)
        
        
        
        
        # print("Population disconnected from district heating: " + _pop_lau_level.loc[])

        total_decentralized = sum(
            graph._node[_key]["Decentralized"]
            for _key in graph._node.keys()
            if _key is not node_to_drop
        )

        if total_decentralized < graph._node[node_to_drop]["Centralized"]:
            print(
                "Stop heat generation reallocation (decentralized lower than centralized)"
            )
            break
        else:
            reduced_graph = graph
            shift = (
                reduced_graph._node[node_to_drop]["Centralized"] / total_decentralized
            )
            del reduced_graph._node[node_to_drop]
            del reduced_graph._adj[node_to_drop]

            remove = dict()
            for node1 in reduced_graph._node.keys():
                for node2 in reduced_graph._adj[node1].keys():
                    if node2 == node_to_drop:
                        remove[node1] = node2

                reduced_graph._node[node1]["Centralized"] += (
                    shift * reduced_graph._node[node1]["Decentralized"]
                )
                reduced_graph._node[node1]["Decentralized"] -= (
                    shift * reduced_graph._node[node1]["Decentralized"]
                )

            for region in remove.keys():
                del reduced_graph._adj[region][remove[region]]
                if remove[region] in reduced_graph._adj.keys():
                    del reduced_graph.adj[remove[region]]

            graph = reduced_graph

    final_graph = graph
    benchmark_df = pd.DataFrame(_benchmarks).T

    final_nodes = list(final_graph._node.keys())
    final_lines = lines.loc[
        (lines["START"].isin(final_nodes)) & (lines["END"].isin(final_nodes))
    ]
    final_generation = init_quantities.loc[init_quantities["region"].isin(final_nodes)]
    final_cen_generation = final_generation.loc[
        final_generation["variable"] == "Centralized"
    ]

    for item in final_cen_generation["region"]:
        final_cen_generation.loc[
            final_cen_generation["region"] == item, ["value"]
        ] = final_graph._node[item]["Centralized"]
    
    df = pd.DataFrame(_removed_pop)
    df.to_excel("Removed_population.xlsx")

    return final_cen_generation, final_lines, benchmark_df


def files_to_results_folder(generation=None, lines=None, benchmark=None, folder=None, boundary=None):

    """

    Parameters
    ----------
    generation : GeoDataFrame, required
        Includes the centralized heat generation quantities. The default is None.
    lines : GeoDataFrame, required
        Includes the implemented connection lines. The default is None.
    benchmark : DataFrame, required
        Includes the benchmark indicator values. The default is None.
    folder : string, required
        Includes the name of the result folder. The default is None.

    -------
    results_directory : String
        Includes the name of the results folder.

    """

    time = datetime.now().strftime("%Y%m%dT%H%M")
    results_directory = os.path.join(
        "iterative-downscaling-results", "{}-{}".format(folder, time)
    )
    if not os.path.exists(results_directory):
        os.makedirs(results_directory)

    if not lines.empty:
        lines.to_file(results_directory + "\lines.shp")
    _values = gpd.GeoDataFrame(generation)
    _values.to_file(results_directory + "\generation.shp")
    
    boundary.to_file(results_directory + "\polygons.shp")

    
    benchmark.to_excel(excel_writer=results_directory + "\indicator_values.xlsx")

    return results_directory


def plot_final_network_graph(generation=None, lines=None, total_area=None, folder=None):

    """

    Parameters
    ----------
    generation : TYPE, optional
        DESCRIPTION. The default is None.
    lines : TYPE, optional
        DESCRIPTION. The default is None.
    total_area : TYPE, optional
        DESCRIPTION. The default is None.
    folder : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    None.

    """

    plt.style.use("science")
    fig, ax = plt.subplots(nrows=1, ncols=1)

    ax.axis("off")

    _gen = gpd.GeoDataFrame(generation)
    _a1 = sum(_gen.geometry.area)

    _area = gpd.GeoDataFrame(total_area)
    
    _a2 = sum(_area.geometry.area)
    
    print(_a2 / _a1 / 2)

    

    
    _centroids = _gen.centroid.to_frame()
    _area.boundary.plot(ax=ax, linewidth=0.5, color="#D1D9D9", linestyle="dashed")
    _centroids["value"] = _gen.value
    centroids = gpd.GeoDataFrame(_centroids)
    centroids.rename(columns={0: "geometry"}, inplace=True)
    centroids.plot(
        ax=ax,
        marker="o",
        color="#053742",
        markersize=1.5 * centroids["value"],
        legend=True,
    )
    lines.plot(ax=ax, color="#FBC7F7", linewidth=0.5)
    fig.savefig(folder + "\centralized-heat-network.png", dpi=500)
    return


def create_initial_network_topology(
    country="AT",
    shapefile="shapefiles\LAU shapefile\LAU_RG_01M_2019_3035.shp",
    matching="data\Allocating_LAU_to_NUTS3_1.1.2020.xlsx",
):

    """

    Parameters
    ----------
    country : String, optional
        Country code. The default is "AT".
    shapefile : String, optional
        Includes the path to the shapefiles on the LAU level. The default is "shapefiles\LAU shapefile\LAU_RG_01M_2019_3035.shp".
    matching : String, optional
        Includes the file that is used for the allocation of LAU level areas to the NUTS3 level. The default is "data\Allocating_LAU_to_NUTS3_1.1.2020.xlsx".

    Returns
    -------
    Results : GeoDataFrame
        Nodal centralized and decentralized heat generation (including geometry) on the LAU level. 

    """
    
    eu_nuts3_regions = gpd.read_file(shapefile)
    country_nuts3_regions = eu_nuts3_regions.loc[
        eu_nuts3_regions["CNTR_CODE"] == country
    ]

    mapping = pd.read_excel(matching)
    mapping.rename(columns={"Unnamed: 3": "LAU_NAME"}, inplace=True)
    mapping.drop(labels=[0, 1, 2], axis=0, inplace=True)

    _lau_nuts3_at = mapping.merge(country_nuts3_regions, on="LAU_NAME")
    _lau_nuts3_at["region"] = (
        _lau_nuts3_at["Zuordnung NUTS 3 zu Gemeinden"] + "|" + _lau_nuts3_at["LAU_NAME"]
    )

    _pop_small_sub_region = pd.read_excel("data\Population_on_LAU_level_in_2050.xlsx")
    _pop_small_sub_region = _pop_small_sub_region.merge(
        mapping, left_on="region", right_on="Unnamed: 2"
    )
    _val = _pop_small_sub_region.groupby(["Unnamed: 1"]).sum().reset_index()

    _val = _val.merge(mapping, on="Unnamed: 1")
    _val = _val[[2050, "Zuordnung NUTS 3 zu Gemeinden"]].drop_duplicates()
    _val.rename(
        columns={2050: "Total population", "Zuordnung NUTS 3 zu Gemeinden": "NUTS 3"},
        inplace=True,
    )

    _population = _pop_small_sub_region.merge(
        _val, left_on="Zuordnung NUTS 3 zu Gemeinden", right_on="NUTS 3"
    )
    _population["Share"] = _population[2050] / _population["Total population"]
    _population.drop(labels=2050, axis=1, inplace=True)

    RESULTS_FOLDER = Path("sequential-downscaling-results")  
    _generation = pd.read_excel(
        RESULTS_FOLDER / "results_centralized+decentralized_heat_generation.xlsx"
    )

    full_data_set = _population.merge(
        _generation, left_on="Zuordnung NUTS 3 zu Gemeinden", right_on="Region"
    )
    full_data_set["Year"] = 2050
    full_data_set["Value"] = full_data_set["2050"] * full_data_set["Share"]
    full_data_set["region"] = (
        full_data_set["Zuordnung NUTS 3 zu Gemeinden"] + "|" + full_data_set["LAU_NAME"]
    )
    full_data_set = full_data_set[
        ["Model", "Scenario_y", "region", "Variable", "Year", "Value", "Unit"]
    ]
    full_data_set.rename(columns={"Scenario_y": "Scenario"}, inplace=True)
    _share = pyam.IamDataFrame(full_data_set)
    # _share.to_excel("lau_share_gen_pop.xlsx", iamc_index=False, include_meta=False)

    _rel_at130 = pyam.IamDataFrame("data\Population_in_Vienesse_districts.xlsx")
    _share.append(_rel_at130, inplace=True)
    _130 = _share.downscale_region(
        variable=["Centralized", "Decentralized"],
        region="AT130|Wien",
        proxy="Relative share of population",
    )
    _share.append(_130, inplace=True)

    values = _share.data.merge(_lau_nuts3_at, on="region")
    nuts3_at130 = gpd.read_file("shapefiles\Vienesse_districts\ZAEHLBEZIRKOGDPolygon.shp")
    _130 = nuts3_at130.dissolve(by="BEZNR", aggfunc="sum").reset_index()
    _130["region"] = "AT130|Wien|" + _130["BEZNR"].astype(int).apply(str)
    new_val = _share.data.merge(_130, on="region")
    Results = values.append(new_val)
    Results = gpd.GeoDataFrame(Results)
    Results.drop(
        [
            "LAU_NAME",
            "Unnamed: 1",
            "Unnamed: 2",
            "GISCO_ID",
            "CNTR_CODE",
            "POP_2019",
            "POP_DENS_2",
            "AREA_KM2",
            "YEAR",
            "FID",
            "BEZNR",
            "ZBEZNR",
            "FLAECHE",
            "UMFANG",
            "SE_SDO_ROW",
        ],
        axis=1,
        inplace=True,
    )
    Results.rename(
        columns={"Zuordnung NUTS 3 zu Gemeinden": "NUTS3_CODE"}, inplace=True
    )
    return Results


def create_connection_lines(shapefile=None, subregion=None, scenario=None):

    """

    Parameters
    ----------
    shapefile : GeoDataFrame, required
        Includes the nodal heat generation and its geometry. The default is None.
    subregion : String, required
        Includes the name of the sub-region. The default is None.
    scenario : String, required
        Includes the name of the scenario. The default is None.

    Returns
    -------
    all_lines : Shapefile
        Includes the available connection lines.

    """

    # shapefile["unit"] = "GWh"
    # shapefile["value"] *= 1000

    _var = shapefile.loc[
        (shapefile["NUTS3_CODE"] == subregion)
        & (shapefile["scenario"] == scenario)
        & (shapefile["variable"] == "Centralized")
    ]

    _centroids = _var.centroid.to_frame()
    _centroids["value"] = _var.value
    centroids = gpd.GeoDataFrame(_centroids)
    centroids.rename(columns={0: "geometry"}, inplace=True)

    _geo_series_lines = None

    _comb = list(combinations(centroids.index, 2))

    for _c in _comb:
        _a1 = gpd.GeoSeries(_var.loc[_c[0]].geometry)
        _a2 = gpd.GeoSeries(_var.loc[_c[1]].geometry)
        _p = _a1.centroid
        _p = _p.append(_a2.centroid)

        _intersec = _a1.intersection(_a2).length
        _con = gpd.GeoSeries(_p.unary_union.convex_hull)

        if _intersec.values[0] > 0:
            _con = gpd.GeoDataFrame(_con)
            _con["START"] = _var.loc[_c[0]].region
            _con["END"] = _var.loc[_c[1]].region
            if _geo_series_lines is None:
                _geo_series_lines = _con
            else:
                _geo_series_lines = _geo_series_lines.append(_con)

    all_lines = _geo_series_lines.rename(columns={0: "geometry"})

    return all_lines
