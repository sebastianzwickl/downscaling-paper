import numpy as np


def set_dh_total_heat_parameters(genesysmod=None, population=None):

    dh_total = dict()
    demand = dict()
    q_dem_l = dict()

    total_pop = sum(population[2050])

    for scenario in genesysmod.scenario:

        gen_sce = genesysmod.filter(scenario=scenario).data
        demand[scenario] = sum(gen_sce["value"]) / 3.6
        heatpumphalf = (
            gen_sce[gen_sce["variable"] == "Heat pump (air)"]["value"] / 2 / 3.6
        )
        dh_total[scenario] = np.round(
            (
                sum(
                    gen_sce[
                        gen_sce["variable"].isin(
                            ["Geothermal", "Hydrogen", "Waste", "Synthetic gas"]
                        )
                    ]["value"]
                )
                / 3.6
                + heatpumphalf
            ).item(),
            5,
        )

        for index, row in population.iterrows():
            lau = row['region']
            q_dem_l[scenario, lau] = row[2050] / total_pop * demand[scenario]

    return dh_total, q_dem_l


def set_environment_for_each_lau(lau=None):
    lau_env = dict()
    for index1, row1 in lau.iterrows():
        list_env_lau = []
        for index2, row2 in lau.iterrows():
            if row1.geometry.intersection(row2.geometry):
                if row1['LAU_ID'] != row2['LAU_ID']:
                    list_env_lau.extend([row2['LAU_ID']])
        lau_env[row1['LAU_ID']] = list_env_lau
    
    return lau_env