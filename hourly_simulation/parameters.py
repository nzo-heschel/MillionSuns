import csv
from collections import namedtuple
from typing import Dict

import pandas as pd

from df_objects.df_objects import CostElectricityDf

# Non changing Params
PARAMS_PATH = "data/parameters.csv"
MW_TO_KW_DIVIDE = {
    "/mw": "/kw",
    "/Mw": "/Kw",
    "/MW": "/KW"
}
MW_TO_KW_MULTIPLY = {
    "mw": "kw",
    "Mw": "Kw",
    "MW": "KW"
}


def mw_to_kw(value, unit, as_mw):
    if any([w in unit for w in MW_TO_KW_DIVIDE.keys()]) and not as_mw:
        value = float(value) / 1000
    elif any([w in unit for w in MW_TO_KW_MULTIPLY.keys()]) and not as_mw:
        value = float(value) * 1000
    return float(value)


def get_simulation_parameters(csv_path, with_units=False, as_mw=False) -> Dict:
    """
    Retrieves the parameters from csv_path as dictionary

    :param csv_path: str path of parameters_backup.csv file
    :param with_units: boolean should return the units (third column) as well?
    :return: if with_units: dictionary(str -> float). else: dictionary(str -> (float, str))
    """
    params = {}
    with open(csv_path, newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if with_units:
                params[row[0].strip()] = (mw_to_kw(row[1], row[2], as_mw), row[2])
            else:
                params[row[0].strip()] = mw_to_kw(row[1], row[2], as_mw)
    return params


__simulation_params_dict = get_simulation_parameters(PARAMS_PATH)
Params = namedtuple('Params', __simulation_params_dict.keys())
simulation_params = Params(**__simulation_params_dict)

# Electricity

ELECTRICITY_COST_PATH = 'data/electricity_cost.csv'
ELECTRICITY_COST_BINARY_PATH = 'data/shifted_electricity_cost_binary.csv'
ELECTRICITY_SELLING_INCOME_PATH = 'data/electricity_sell_income.csv'
ELECTRICITY_COST = CostElectricityDf(pd.read_csv(ELECTRICITY_COST_PATH, index_col=0))
ELECTRICITY_SELLING_INCOME = CostElectricityDf(pd.read_csv(ELECTRICITY_SELLING_INCOME_PATH))  # ILS per Kw
BINARY_SELLING_COST = CostElectricityDf(pd.read_csv(ELECTRICITY_COST_BINARY_PATH, index_col=0))
