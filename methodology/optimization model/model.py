import pandas as pd
import pyam
import utils
import geopandas as gpd
import csv
import pyomo.environ as py
import pyomo
from datetime import datetime
import os


def init_heat_demand_per_lau(model, lau):
    scenario = model.scenario
    return model.demand_per_lau[scenario, int(lau)]


def init_area_eff_factor(model, lau):
    if int(lau) in model.phi_l.keys():
        category = model.phi_l[int(lau)]
        
        if category == 'IV':
            return 1
        elif category == 'III':
            return 1
        elif category == 'II':
            return 0.5
        elif category == 'I':
            return 0.5

    elif int(lau) == 90001:
        return 0.65
    else:
        return 1


def init_per_area_per_lau(model, lau):
    if int(lau) in model.area_l.keys():
        return model.area_l[int(lau)]
    else:
        return 10e10

def init_per_area_env_l(model, lau):
    area = 0
    data = model.subset_per_lau
    data = data[data[0] == int(lau)][1].item()
    data = data.replace('[', '')
    data = data.replace(']', '')
    data = data.split(",")
    for i in data:
        i = i.replace("['", "")
        i = i.replace("'", "")
        i = i.replace("'", "")
        i = i.replace("]", "")
        i = i.replace('"', "")
        
        lau_id = int(i)
        
        if lau_id in model.area_l.keys():
            area += model.area_l[lau_id] * model.p_phi_l[lau]
        
    return area


def write_IAMC(output_df, model, scenario, region, variable, unit, time, values):
    if isinstance(values, list):
        _df = pd.DataFrame(
            {
                "model": model,
                "scenario": scenario,
                "region": region,
                "variable": variable,
                "unit": unit,
                "year": time,
                "value": values,
            }
        )
    else:
        _df = pd.DataFrame(
            {
                "model": model,
                "scenario": scenario,
                "region": region,
                "variable": variable,
                "unit": unit,
                "year": time,
                "value": values,
            },
            index=[0],
        )
    output_df = output_df.append(_df)
    return output_df


""" (A) READ INPUT DATA """

area_eff = pd.read_excel('data/eff-area.xlsx')
per_area_set = pd.read_excel('data/per-area-lau.xlsx')
pop = pd.read_excel('data/pop-lau.xlsx')

genesysmod = pyam.IamDataFrame('data/genesys-mod.xlsx')

at_laus = gpd.read_file('data/lau-shp/at-laus.shp')


""" (B) PREPARE INPUT DATA """

# dh_total ... Heat generation from GENeSYS-MOD's cost-optimal solution used in district heating
# q_total_l ... Total heat demand at local administrative unit 'l'

dh_total, q_total_l = utils.set_dh_total_heat_parameters(genesysmod, pop)

phi_l = dict(zip(area_eff['LAU ID'], area_eff['VALUE']))
area_l = dict(zip(per_area_set['LAU ID'], per_area_set['PERMANENT SETTLEMENT AREA']))

# subset_per_lau = utils.set_environment_for_each_lau(at_laus)
# _file = open('data/lau-env-subset.csv', 'w')
# writer = csv.writer(_file)
# for key, val in subset_per_lau.items():
#     writer.writerow([key, val])
# _file.close()

subset_per_lau = pd.read_csv('data/lau-env-subset.csv', header=None)


""" (C) OPTIMIZATION MODEL """

model = py.ConcreteModel()
model.name = "downscaling"

model.set_laus = py.Set(initialize=at_laus['LAU_ID'])
model.subset_per_lau = subset_per_lau
model.demand_per_lau = q_total_l
model.phi_l = phi_l
model.area_l = area_l

model.scenario = 'Gradual Development'

model.v_q_dh_l = py.Var(model.set_laus, domain=py.NonNegativeReals)
model.v_q_ons_l = py.Var(model.set_laus, domain=py.NonNegativeReals)
model.v_q_env_l = py.Var(model.set_laus, domain=py.NonNegativeReals)


model.p_Q_dh_gen = py.Param(
    initialize=dh_total[model.scenario],
    within=py.NonNegativeReals,
    doc='Total amount of district heating')

model.p_q_total_l = py.Param(
    model.set_laus,
    initialize=init_heat_demand_per_lau,
    within=py.NonNegativeReals,
    doc='Total heat demand per local administrative unit')

model.p_phi_l = py.Param(
    model.set_laus,
    initialize=init_area_eff_factor,
    within=py.NonNegativeReals,
    doc='Reduction factor to obtain effective area of district heating per local administrative unit')

model.p_per_area_l = py.Param(
    model.set_laus,
    initialize=init_per_area_per_lau,
    within=py.NonNegativeReals,
    doc='Permanent settlement area per local administrative unit')

model.p_per_area_env_l = py.Param(
    model.set_laus,
    initialize=init_per_area_env_l,
    within=py.NonNegativeReals,
    doc='Surrounding area per local administrative unit')


def objective_function(model=None):
    first_term = sum(
        model.v_q_dh_l[lau] / (model.p_phi_l[lau] * model.p_per_area_l[lau])
        for lau in model.set_laus)
    second_term = sum(
        model.v_q_env_l[lau] / model.p_per_area_env_l[lau]
        for lau in model.set_laus)
    
    return first_term + second_term


model.objective = py.Objective(expr=objective_function, sense=py.maximize)


def c_sum_per_lau(model, lau):
    return model.v_q_dh_l[lau] + model.v_q_ons_l[lau] == model.p_q_total_l[lau]
model.c_sum_per_lau = py.Constraint(model.set_laus, rule=c_sum_per_lau)


def c_limit_dh_for_all_laus(model):
    return sum(
        model.v_q_dh_l[lau]
        for lau in model.set_laus) <= model.p_Q_dh_gen
model.c_limit_dh_for_all_laus = py.Constraint(rule=c_limit_dh_for_all_laus)


def c_calculate_env_dh_per_lau(model, lau):
    rightside = 0
    data = model.subset_per_lau
    data = data[data[0] == int(lau)][1].item()
    data = data.replace('[', '')
    data = data.replace(']', '')
    data = data.split(",")
    for i in data:
        i = i.replace("['", "")
        i = i.replace("'", "")
        i = i.replace("'", "")
        i = i.replace("]", "")
        i = i.replace('"', "")
        
        lau_id = int(i)
        
        
        if str(lau_id) in model.set_laus:
            rightside += model.v_q_dh_l[str(lau_id)]
        else:
            print(lau_id)
            
            
    return model.v_q_env_l[lau] == rightside
model.c_cal_env_dh = py.Constraint(model.set_laus, rule=c_calculate_env_dh_per_lau)


def c_set_dh_to_zero(model, lau):
    if int(lau) in model.phi_l.keys():
        category = model.phi_l[int(lau)]
        
        if category == 'IV':
            return model.v_q_dh_l[lau] == 0
        elif category == 'III':
            return model.v_q_dh_l[lau] == 0
        else:
            return py.Constraint.Skip
    else:
        return py.Constraint.Skip
    
model.c_set_dh_to_zero = py.Constraint(model.set_laus, rule=c_set_dh_to_zero)
    

model.write('Downscaling.lp', io_options={"symbolic_solver_labels": True})
_file = open("Downscaling.txt", "w", encoding="utf-8")
model.pprint(ostream=_file, verbose=False, prefix="")
_file.close()

Solver = pyomo.opt.SolverFactory("gurobi")
Solver.options["LogFile"] = str(model.name) + ".log"
solution = Solver.solve(model, tee=True)
solution.write()
model.objective.display()

# i = 0
# for lau in model.set_laus:
#     if model.v_q_dh_l[lau].value * 1000 / (model.p_phi_l[lau] * model.p_per_area_l[lau]) > 0.01:
#         i += 1
#         print('{} : {}'.format(lau, model.v_q_dh_l[lau].value * 1000 / (model.p_phi_l[lau] * model.p_per_area_l[lau])))
# print(i)

time = datetime.now().strftime("%Y%m%dT%H%M")
path = os.path.join("solution", "{}-{}".format(model.scenario, time))

if not os.path.exists(path):
    os.makedirs(path)

df_out = pd.DataFrame()
_scenario = model.scenario
_model = model.name

for lau in model.set_laus:
    if model.v_q_dh_l[lau].value * 1000 / (model.p_phi_l[lau] * model.p_per_area_l[lau]) > 0.01:
        df_out = write_IAMC(df_out, _model, _scenario, lau, "Heat density", "GWh / km ** 2", 2050, model.v_q_dh_l[lau].value * 1000 / (model.p_phi_l[lau] * model.p_per_area_l[lau]))
df_out.to_excel(os.path.join(path, "heat-density.xlsx"), index=False)

df_out = pd.DataFrame()
for lau in model.set_laus:
    if lau in ['50101', '50205', '50301', '50309', '50314']:
        df_out = write_IAMC(df_out, _model, _scenario, lau, "District heating", "MWh", 2050, model.v_q_dh_l[lau].value * 1000000)
        df_out = write_IAMC(df_out, _model, _scenario, lau, "On-Site / Dec.", "MWh", 2050, model.v_q_ons_l[lau].value * 1000000)
df_out.to_excel(os.path.join(path, "heat-supply.xlsx"), index=False)

df_out = pd.DataFrame()
df_out_lau_heat_density = pd.DataFrame()
dh_final = 0
dh_out = pd.DataFrame()

nuts3_to_lau = pd.read_excel('data/Allocating_LAU_to_NUTS3_1.1.2020.xlsx')
nuts3 = nuts3_to_lau['NUTS3'].unique()
for nut in nuts3:
    temp = nuts3_to_lau[nuts3_to_lau['NUTS3'] == nut]
    dh = 0
    area = 0
    for lau in temp['LAU ID']:
        if str(lau) in model.set_laus:
            lau = str(lau)
            if model.v_q_dh_l[lau].value * 1000 / (model.p_phi_l[lau] * model.p_per_area_l[lau]) > 0.01:
                dh += model.v_q_dh_l[lau].value * 1000
                area += model.p_phi_l[lau] * model.p_per_area_l[lau]
    if area != 0:
        df_out = write_IAMC(df_out, _model, _scenario, nut, "Heat density", "GWh / km ** 2", 2050, dh / area)
    else:
        df_out = write_IAMC(df_out, _model, _scenario, nut, "Heat density", "GWh / km ** 2", 2050, 0)
        
    if area != 0:
        if dh / area > 10:
            for lau in temp['LAU ID']:
                lau = str(lau)
                if model.v_q_dh_l[lau].value * 1000 / (model.p_phi_l[lau] * model.p_per_area_l[lau]) > 0.01:
                    df_out_lau_heat_density = write_IAMC(df_out_lau_heat_density, _model, _scenario, lau, "Heat density", "GWh / km ** 2", 2050, model.v_q_dh_l[lau].value * 1000 / (model.p_phi_l[lau] * model.p_per_area_l[lau]))
                    dh_final += model.v_q_dh_l[lau].value

dh_out = write_IAMC(dh_out, _model, _scenario, "AT", "District Heating", "TWh", 2050, dh_final)                
df_out_lau_heat_density.to_excel(os.path.join(path, "high-heat-density-lau-10.xlsx"), index=False)            
dh_out.to_excel(os.path.join(path, "final-district-heating.xlsx"), index=False)                      
df_out.to_excel(os.path.join(path, "heat-density-nuts3.xlsx"), index=False)
