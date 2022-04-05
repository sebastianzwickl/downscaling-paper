import pyam
import pandas as pd

from sequential_downscaling import *




def _create_gen_iamdf(scenario=False):
    if scenario is not False:
        _scenario = scenario
    else:
        _scenario = "scen_a"

    _TEST_DF = pd.DataFrame(
        [
            ["model_a", _scenario, "Europe", "Hydrogen", "TWh", 3],
            ["model_a", _scenario, "Europe", "Biomass", "TWh", 2],
            ["model_a", _scenario, "Europe", "Direct-electric", "TWh", 1],
        ],
        columns=["model", "scenario", "region", "variable", "unit", 2050],
    )
    _df = pyam.IamDataFrame(_TEST_DF)
    return _df


def _create_pop_den_iamdf():
    _TEST_DF = pd.DataFrame(
        [
            ["model_a", "scen_a", "Region A", "Population density A", "1/km**2", 5],
            ["model_a", "scen_a", "Region B", "Population density", "1/km**2", 10],
            ["model_a", "scen_a", "Region C", "Population density", "1/km**2", 1],
        ],
        columns=["model", "scenario", "region", "variable", "unit", 2050],
    )
    _df = pyam.IamDataFrame(_TEST_DF)
    return _df


def _create_population_iamdf(scenario=False):
    if scenario is not False:
        _scenario = scenario
    else:
        _scenario = "scen_a"

    _TEST_DF = pd.DataFrame(
        [
            ["model_a", _scenario, "Region A", "Population", "", 5],
            ["model_a", _scenario, "Region B", "Population", "", 10],
            ["model_a", _scenario, "Region C", "Population", "", 1],
        ],
        columns=["model", "scenario", "region", "variable", "unit", 2050],
    )
    _df = pyam.IamDataFrame(_TEST_DF)
    return _df


def test_sequential_downscaling():

    heat_generation = _create_gen_iamdf()
    population_density = _create_pop_den_iamdf()
    population = _create_population_iamdf()

    needs = {"Biomass": 5, "Hydrogen": 8}

    local_generation = sequential_downscaling(
        heat_generation, needs, population_density, population
    )

    is_df = local_generation.data

    _SOL_DF = pd.DataFrame(
        [
            [
                "model_a",
                "scen_a",
                "Region A",
                "Biomass",
                "TWh",
                2050,
                2 * 1.875 / (1.875 + 0.75),
            ],
            [
                "model_a",
                "scen_a",
                "Region A",
                "Direct-electric",
                "TWh",
                2050,
                1.875 - 2 * 1.875 / (1.875 + 0.75),
            ],
            [
                "model_a",
                "scen_a",
                "Region B",
                "Biomass",
                "TWh",
                2050,
                2 * 0.75 / (1.875 + 0.75),
            ],
            [
                "model_a",
                "scen_a",
                "Region B",
                "Direct-electric",
                "TWh",
                2050,
                0.75 - 2 * 0.75 / (1.875 + 0.75),
            ],
            ["model_a", "scen_a", "Region B", "Hydrogen", "TWh", 2050, 3.0],
            ["model_a", "scen_a", "Region C", "Direct-electric", "TWh", 2050, 0.375],
        ],
        columns=["model", "scenario", "region", "variable", "unit", "year", "value"],
        index=range(0, 6),
    )

    assert is_df.equals(_SOL_DF) == True
