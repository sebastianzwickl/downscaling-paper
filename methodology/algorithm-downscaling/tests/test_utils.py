import pyam
import pandas as pd
from utils import validate_input_data
from utils import initialization
from utils import pop_based_downscaling
from utils import iamdf_to_dict
from utils import sequential_algorithm
from utils import dict_to_df


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


def test_validate_input_data():
    _gen = _create_gen_iamdf()
    _pop_den = _create_pop_den_iamdf()
    _pop = _create_population_iamdf()
    _bin = validate_input_data(generation=_gen, pop_density=_pop_den, population=_pop)
    assert _bin == True


def test_validate_input_data_fail():
    _gen = _create_gen_iamdf()
    _pop_den = _create_pop_den_iamdf()
    _pop = _create_population_iamdf()
    # make IamDataframe incomplete
    _pop.filter(region="Region A", inplace=True)
    _bin = validate_input_data(generation=_gen, pop_density=_pop_den, population=_pop)
    assert _bin == False


def test_requirements_initialization():
    _gen = _create_gen_iamdf()
    _needs = {"Biomass": 5, "Hydrogen": 8}
    _val = initialization(_gen.variable, _needs)
    _sol = {"Hydrogen": 8, "Biomass": 5, "Direct-electric": 0}
    assert (_sol == _val) == True


def test_pop_based_downscaling():
    _gen = _create_gen_iamdf()
    _pop = _create_population_iamdf()
    _local_demand = pop_based_downscaling(_gen, _pop)
    _sol = {
        ("scen_a", "Region A"): 1.875,
        ("scen_a", "Region B"): 3.75,
        ("scen_a", "Region C"): 0.375,
    }
    assert _local_demand == _sol


def test_pop_based_downscaling2():
    _gen_a = _create_gen_iamdf()
    _pop_a = _create_population_iamdf()

    _gen_bsl = _create_gen_iamdf(scenario="BSL")
    _pop_bsl = _create_population_iamdf(scenario="BSL")

    _gen = _gen_a.append(_gen_bsl)
    _pop = _pop_a.append(_pop_bsl)

    _local_demand = pop_based_downscaling(_gen, _pop)
    _sol = {
        ("scen_a", "Region A"): 1.875,
        ("scen_a", "Region B"): 3.75,
        ("scen_a", "Region C"): 0.375,
        ("BSL", "Region A"): 1.875,
        ("BSL", "Region B"): 3.75,
        ("BSL", "Region C"): 0.375,
    }
    assert _local_demand == _sol


def test_pop_based_downscaling_fail():
    _gen_a = _create_gen_iamdf()
    _pop_a = _create_population_iamdf()

    _gen_bsl = _create_gen_iamdf(scenario="BSL")
    _pop_bsl = _create_population_iamdf(scenario="BSL")

    _gen = _gen_a.append(_gen_bsl)
    _pop = _pop_a.append(_pop_bsl)

    _local_demand = pop_based_downscaling(_gen, _pop)
    _sol = {
        ("scen_a", "Region A"): 1.875,
        ("scen_a", "Region B"): 3.75,
        ("scen_a", "Region C"): 0.375,
        ("BSL", "Region A"): 0.875,
        ("BSL", "Region B"): 3.75,
        ("BSL", "Region C"): 1.375,
    }
    assert not (_local_demand == _sol)


def test_iamdf_to_dict():
    _gen = _create_gen_iamdf()
    _dict = iamdf_to_dict(df=_gen, keys=["scenario", "region", "variable"])
    _sol = {
        ("scen_a", "Europe", "Hydrogen"): 3,
        ("scen_a", "Europe", "Biomass"): 2,
        ("scen_a", "Europe", "Direct-electric"): 1,
    }
    assert _dict == _sol


def test_sequential_algorithm():
    _dict_gen = {("Scenario A", "Hydrogen"): 80, ("Scenario A", "Direct-electric"): 120}
    _dict_dem = {
        ("Scenario A", "West Austria"): 50,
        ("Scenario A", "Middle Austria"): 50,
        ("Scenario A", "East Austria"): 100,
    }
    _dict_req = {"Hydrogen": 100, "Direct-electric": 0}
    _dict_pot = {"West Austria": 5, "Middle Austria": 50, "East Austria": 100}
    _gen_local = sequential_algorithm(
        _dict_gen, _dict_dem, _dict_req, _dict_pot, "Scenario A"
    )
    _sol = {
        ("Scenario A", "Hydrogen", "East Austria"): 80,
        ("Scenario A", "Direct-electric", "East Austria"): 20,
        ("Scenario A", "Direct-electric", "Middle Austria"): 50,
        ("Scenario A", "Direct-electric", "West Austria"): 50,
    }
    assert _gen_local == _sol


def test_dict_to_df():
    dictionary = {("Scenario A", "Hydrogen", "Austria"): 100}
    column_names = ["Scenario", "Variable", "Region", "Value"]
    df = dict_to_df(dictionary, column_names)

    DF = pd.DataFrame(
        [
            ["Scenario A", "Hydrogen", "Austria", 100],
        ],
        columns=column_names,
    )
    assert DF.equals(df)
