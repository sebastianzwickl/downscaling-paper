import pyam as py
import logging
import pandas as pd
import numpy as np
import networkx as nx


logger = logging.getLogger(__name__)

###
# Below, the utils of the sequential downscaling are defined.
###


def validate_input_data(generation=None, pop_density=None, population=None):

    """

    Parameters
    ----------
    generation : IamDataFrame, required
        Includes the heat generation by technology/source.
        So far, it is necessary to include values of one scenario here.
        This will be updated in further extensions.
        The default is None.
    pop_density : IamDataFrame, required
        Includes the population density of the regions (areas to be downscaled).
        The scenario should be the same as the one of the generation parameter.
        The default is None.
    population : IamDataFrame, required
        Includes the population per region.
        The scenario should be the same as the one of the 'generation' parameter.
        The default is None.

    Returns
    -------
    check : binary (True/False)
        This variable is set to 'True' if all the input data is in the appropiate format.
        Otherwise, it is set to 'False'.

    """

    _string = []
    check = True

    if not isinstance(generation, py.IamDataFrame):
        _string.append("Generation")
    if not isinstance(pop_density, py.IamDataFrame):
        _string.append("Population density")
    if not isinstance(population, py.IamDataFrame):
        _string.append("Population")

    n = len(_string)

    if n != 0:
        msg = (
            "{} input data is not in the IamDataFrame format"
            if n == 1
            else "{} input data are not in the IamDataFrame format"
        )
        logger.warning(msg.format(n, _string))
        check = False
    else:
        logger.info("All input data is in the IamDataFrame format")

        _sce = generation.scenario
        for _s in _sce:
            _pop_den_regions = pop_density.filter(scenario=_s).region
            _pop_regions = population.filter(scenario=_s).region
            if not set(_pop_den_regions) == set(_pop_regions):
                _string.append(_s)

        n = len(_string)
        if n != 0:
            msg = (
                "{} scenario has incomplete input data set"
                if n == 1
                else "Scenarios {} do not have complete input data set"
            )
            logger.warning(msg.format(_string))
            check = False

    return check


def initialization(technologies=None, requirements=None):

    """

    Parameters
    ----------
    technologies : list, required
        A list of heat generation technologies/sources.
        The default is None.
    requirements : dict, required
        Includes the heat network infrastructure requirements of the different
        heat generation technologies. This dictionary should include a specific
        value for each technology/source. If not, the corresponding value is
        set to zero for the technology/source.
        Note that the requirements correspond to the required local population
        density in the current version of the script.
        The default is None.

    Returns
    -------
    full_req : dict
        Includes a complete (full) dictionary related to all technology/source
        specific heat network infrastructure requirements.
        As mentioned, unspecified requirements are set to zero for the
        corresponding technology/source.

    """

    for _t in technologies:
        if not _t in requirements.keys():
            print(f"No requirements defined for {_t}! (is set to 0)")
            requirements[_t] = 0
    full_req = dict(sorted(requirements.items(), key=lambda x: x[1], reverse=True))

    return full_req


def pop_based_downscaling(generation=None, population=None):

    """

    Parameters
    ----------
    generation : IamDataFrame, required
        Includes the heat generation by technology/source.
        So far, it is necessary to include values of one scenario here.
        This will be updated in further extensions.
        The default is None.
    population : IamDataFrame, required
        Includes the population per region.
        The scenario should be the same as the one of the 'generation' parameter.
        The default is None.

    Returns
    -------
    demand : dict
        Includes the population-based downscaled heat demand per region
        (and scenario). Scenario, as part of the dictionary
        key is used for further extensions of the script: for example
        processing multiple scenarios at the same time.

    """

    total_generation = dict()
    demand = dict()
    scenarios = generation.scenario
    for _sce in scenarios:
        total_generation = generation.filter(scenario=_sce).data["value"].sum()
        total_population = population.filter(scenario=_sce).data["value"].sum()
        for _r in population.filter(scenario=_sce).region:
            demand[_sce, _r] = (
                total_generation
                * (
                    population.filter(scenario=_sce, region=_r).data["value"]
                    / total_population
                )[0]
            )

    return demand


def iamdf_to_dict(df=None, keys=None):

    """

    Parameters
    ----------
    df : IamDataFrame, required
        Includes the data in the IAMC format that is tranformed to a dict.
        The default is none.
    keys : list, required
        A list containing the columns of the IamDataFrame used as key.
        The order of elements within the list needs to be same as the columns
        of the IamDataFrame (IAMC format).
        The default is None.

    Returns
    -------
    _dict : dict
        A dictionary with selected keys and corresponding values.

    """

    _dict = dict()
    _pandas_df = df.data
    for index, row in _pandas_df.iterrows():
        _k = []
        if "model" in keys:
            _k.append(row["model"])
        if "scenario" in keys:
            _k.append(row["scenario"])
        if "region" in keys:
            _k.append(row["region"])
        if "variable" in keys:
            _k.append(row["variable"])
        if "unit" in keys:
            _k.append(row["unit"])
        if "year" in keys:
            _k.append(row["year"])

        if len(keys) == 1:
            _dict[_k[0]] = row["value"]
        else:
            _dict[tuple(_k)] = row["value"]

    return _dict


def sequential_algorithm(
    generation=None, demand=None, requirements=None, potential=None, scenario=None
):

    """

    Parameters
    ----------
    generation : dict, required
        A dictionary including the heat generation by technology/source with
        scenario and variable as keys. The scenario-related key is already
        implemented for further extensions of the script.
        The default is None.
    demand : dict, required
        A dictionary including the (downscaled) heat demand on the region
        level with scenario and region as keys.
        The scenario-related key is already
        implemented for further extensions of the script.
        The default is None.
    requirements : dict, required
        Requirements of heat network infrastructure at the local level. The key
        of the dictionary is the heat generation technology/source.
        The default is None.
    potential : dict, required
        Potential of heat network infrastructure at the local level. The key
        of the dictionary is the region.
        The default is None.
    scenario : string, required
        Sets the scenario. This parameter is already considered to help further
        developments of the script related to multiple scenario analyses.
        The default is None.

    Returns
    -------
    quantity : dict
        The heat generation by technology/source at the local level.
        The key of the dict is a tuple including scenario, variable,
        and region (in this order).

    """

    quantity = dict()
    for _k_req in requirements.keys():

        _list = []
        _load = 0
        _all_valid_regions = [
            _k for _k, _v in potential.items() if _v >= requirements[_k_req]
        ]

        for _r in _all_valid_regions:
            if demand[scenario, _r] >= 0:
                _list.append(_r)
                _load += demand[scenario, _r]
        for _l in _list:
            _q = (demand[scenario, _l] / _load) * generation[scenario, _k_req]
            quantity[scenario, _k_req, _l] = _q
            demand[scenario, _l] -= quantity[scenario, _k_req, _l]
            if np.round(demand[scenario, _l], 6) < 0:
                print("Heat demand/generation mismatch - under construction")

    return quantity


def dict_to_df(dictionary=None, col_name=None):

    """

    Parameters
    ----------
    dictionary : dict, required
        Includes a dictionary that is tranformed to the IAMC format and
        IamDataFrame. It is required that the key tuple of the dictionary
        includes the information of the 'scenario', 'variable', and 'region'
        column (in this order).
        The default is None.
    col_name : list, optional
        Includes column names that are used for the IAMC format. If this
        parameter is not passed to the function, the default description,
        as described above in the 'dictionary' description, is used.
        The default is None.

    Returns
    -------
    df : DataFrame

    """

    df = df = pd.DataFrame(dictionary, index=[0]).T.reset_index()

    if col_name == None:
        df.columns = ["Scenario", "Variable", "Region", "Value"]
    else:
        df.columns = col_name

    return df


def calculate_heat_density(heat_generation=None, area=None):

    """

    Parameters
    ----------
    heat_generation : IamDataFrame, required
        Heat generation at the region level. The default is None.
    area : IamDataFrame, required
        Total area at the region level. The default is None.

    Returns
    -------
    hd : IamDataFrame
        Heat density at the local level.

    """
    val_gen = heat_generation.filter(variable="Centralized").data
    for index, row in val_gen.iterrows():
        _a = area.filter(region=row["region"]).data["value"][0] / 1000
        val_gen.loc[index, "value"] = row["value"] / _a
        val_gen.loc[index, "unit"] = "GWh/km**2"
    hd = py.IamDataFrame(val_gen)
    return hd


###
# Below, the utils of the iterative downscaling are defined.
###


def make_networkx_from_shapefile(connection=None):

    """

    Parameters
    ----------
    connection : Shapefile, required
        Includes the available connection lines between nodes.
        The default is None.

    Returns
    -------
    graph : Networkx
        Initial graph with connection lines.

    """

    graph = nx.Graph()
    for index, region in connection.iterrows():
        graph.add_edge(
            u_of_edge=region.END, v_of_edge=region.START, weight=region.geometry.length
        )
    return graph


def add_quantities_to_nodes(graph=None, quantities=None):

    """

    Parameters
    ----------
    graph : Networkx, required
        The default is None.
    quantities : Shapefile, required
        Includes the amount of centralized and decentralized heat generation.
        The default is None.

    Returns
    -------
    graph : Networkx
        The graph with centralized and decentralized heat generation per node.

    """

    for key in graph._node:
        for _type in ["Centralized", "Decentralized"]:
            graph._node[key][_type] = float(
                quantities.loc[
                    (quantities.region == key) & (quantities.variable == _type)
                ].value
            )

    return graph


def calculate_cluster_coefficient(graph=None):

    """

    Parameters
    ----------
    graph : Networkx, required
        Includes the graph with heat generation quantities (centralized and decentralized) and connection lines.
        The default is None.

    Returns
    -------
    Results : dict
        Value of the cluster coefficient per node.

    """

    results = dict()
    max_quantity = max(graph._node[key]["Centralized"] for key in graph._node.keys())

    for key in graph._node.keys():
        # e.g., key = AT127|Achau
        _alpha = dict()
        for node1 in graph._adj[key]:
            # e.g., node1 == AT127|Biedermannsdorf
            # Biedermannsdorf, Hennersdorf, Himberg, Laxenburg, Leopoldsdorf, Maria-Lanzendorf, Münchendorf
            for node2 in graph._adj[node1]:
                # e.g., Achau, Guntramsdorf, Hennersdorf, Laxenburg, Vösendorf, Wiender Neudorf
                if key in graph._adj[node2]:
                    _alpha[node1, node2] = 1

        number = len(_alpha.keys())
        m = len(graph._adj[key])
        q = graph._node[key]["Centralized"]
        if m > 1:
            results[key] = (q / max_quantity) * (number / (m * (m - 1)))
        else:
            results[key] = 0

    return results


def calculate_distance_coefficient(graph=None):

    """

    Parameters
    ----------
    graph : Networkx, required
        Includes a graph with nodes, lines and centralized/decentralized heat quantities.
        The default is None.

    Returns
    -------
    results : dict
        Includes the value of the distance coefficient per node.

    """

    results = dict()
    distances = dict()

    for node1 in graph._node.keys():
        distances[node1] = 0
        for node2 in graph._node.keys():
            if nx.has_path(graph, source=node1, target=node2):
                _d = nx.single_source_dijkstra(
                    graph, source=node1, target=node2, weight="weight"
                )
                if _d[0] > distances[node1]:
                    distances[node1] = _d[0]
                else:
                    distances[node1] = np.Inf

        results[node1] = 1 / (2 * distances[node1])
    min_distance = min(distances[node] for node in distances.keys())
    max_quantity = max(
        graph._node[node]["Decentralized"] for node in graph._node.keys()
    )

    for key in results.keys():
        results[key] *= min_distance
        results[key] *= graph._node[key]["Centralized"]
        results[key] *= 1 / max_quantity

    return


def calculate_total_indicator_value(
    cluster_coefficient=None, distance_coefficient=None
):

    """

    Parameters
    ----------
    cluster_coefficient : dict, required
        Includes the cluster coefficient value per node.
        The default is None.
    distance_coefficient : TYPE, optional
        Includes the distance coefficient value per node.
        The default is None.

    Returns
    -------
    results : dict
        Includes the calculated total indicator value per node.

    """

    results = dict()

    for key in cluster_coefficient.keys():
        results[key] = cluster_coefficient[key]
        # results[key] = cluster_coefficient[key] + distance_coefficient[key]
        # Only the cluster coefficient is used for the benchmark.
        # The distance coefficient will be considered in future work.
    return results
