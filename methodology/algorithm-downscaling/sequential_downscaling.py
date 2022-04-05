import utils
from pyam import IamDataFrame


def sequential_downscaling(
    generation=None, needs=None, pop_density=None, population=None
):

    """

    Algorithm 1: Sequential downscaling algorithm
    This algorithm is intended to downscaling heat generation by
    technology/source from the country level (NUTS0) to the
    small sub-region level (NUTS3).


    Parameters
    ----------
    generation : IamDataFrame, required
        Includes the heat generation by technology/source.
        So far, it is necessary to include values of one scenario here.
        This will be updated in further extensions.
        The default is None.
    needs : dict, required
        Includes the heat network infrastructure requirements of the different
        heat generation technologies. This dictionary should include a specific
        value for each technology/source.
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
    local_heat_generation : IamDataFrame
        Heat generation per technology/source at the local level.

    """

    if utils.validate_input_data(generation, pop_density, population):

        _model = generation.model
        _unit = generation.unit
        _year = generation.year

        technologies = generation.variable
        requirements = utils.initialization(technologies, needs)
        loc_demand = utils.pop_based_downscaling(generation, population)

        _dict_gen = utils.iamdf_to_dict(df=generation, keys=["scenario", "variable"])
        _dict_pot = utils.iamdf_to_dict(df=pop_density, keys=["region"])

        _res = dict()

        for _sce in generation.scenario:
            _loc_gen = utils.sequential_algorithm(
                _dict_gen, loc_demand, requirements, _dict_pot, _sce
            )
            _res = {**_res, **_loc_gen}

        col_names = ["Scenario", "Variable", "Region", "Value"]
        df = utils.dict_to_df(_res, col_names)

        df.insert(1, "model", _model[0])
        df.insert(1, "unit", _unit[0])
        df.insert(1, "year", _year[0])

        local_heat_generation = IamDataFrame(df)
        return local_heat_generation

    else:
        return None
