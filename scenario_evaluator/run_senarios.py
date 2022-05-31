import logging
from typing import Iterator, Tuple, Callable, List

import pandas as pd
from tqdm import tqdm

from df_objects.df_objects import DemandDf, ProductionDf, SimulationResults
from hourly_simulation.parameters import Params
from hourly_simulation.simulation import simulate_use


def check_reached_edges_of_iterator(solar_panel_power_it_mw: Iterator, num_batteries_it: Iterator,
                                    optimal_power, optimal_num_batteries) -> Tuple[bool, str]:
    """
    Checks whether the one of the optimal values reached the minimum / maximum of the iterator.

    :param solar_panel_power_it_mw: iterator for different solar panels
    :param num_batteries_it: iterator for different battery sizes
    :param optimal_power: simulated optimal solar power
    :param optimal_num_batteries: simulated optimal number of batteries
    :return: Tuple[is reached bounds?, String status of optimal combination in bounds].
    """
    results = ""
    if optimal_power == min(solar_panel_power_it_mw):
        msg = "Reached the 'from' of the Solar panel max MW Range: " + str(optimal_power)
        logging.warning(msg)
        results += msg + '\n'
    elif optimal_power == max(solar_panel_power_it_mw):
        msg = "Reached the 'to' of the Solar panel max MW Range: " + str(optimal_power)
        logging.warning(msg)
        results += msg + '\n'
    if optimal_num_batteries == min(num_batteries_it):
        msg = "Reached the 'from' of the Batteries Range: " + str(optimal_num_batteries)
        logging.warning(msg)
        results += msg + '\n'
    elif optimal_num_batteries == max(num_batteries_it):
        msg = "Reached the 'to' of the Batteries Range: " + str(optimal_num_batteries)
        logging.warning(msg)
        results += msg + '\n'
    if not results:
        return False, "Optimal Combination is in range"
    return True, results


def run_scenarios(demand: DemandDf, normalised_production: ProductionDf, simulated_year: int,
                  solar_panel_power_it_mw: Iterator, num_batteries_it: Iterator, strategy: Callable, params: Params,
                  progress_bar: List[float], time_span=1) -> Tuple[SimulationResults, pd.DataFrame, Tuple[bool, str]]:
    """
    Run the simulation of various solar panel and battery combinations

    :param demand: DemandDf of pd.DataFrame(columns=['HourOfYear', '$(Year)'])
    :param normalised_production: ProductionDf of pd.DataFrame(columns=['HourOfYear', 'SolarProduction'])
        between 0 and 1
    :param simulated_year: int year to simulate
    :param solar_panel_power_it_mw: iterator for different solar panels in mw
    :param num_batteries_it: iterator for different battery sizes
    :param strategy: function responsible for handling the cost
    :param params: namedtuple simulation params
    :param progress_bar: List reference used to update callee on percentage done.
    :param time_span: time of which the system is expected to work
    :return: Tuple of the best combination of (number of solar panels, size of battery)
    """
    simulation_results = {SimulationResults.PowerSolar: [], SimulationResults.NumBatteries: [],
                          SimulationResults.Cost: []}
    counter = 0
    total_simulations = sum(1 for _ in solar_panel_power_it_mw) * sum(1 for _ in num_batteries_it)
    for solar_panel_power_mw in tqdm(solar_panel_power_it_mw):
        for num_batteries in num_batteries_it:
            simulation_results[SimulationResults.PowerSolar].append(solar_panel_power_mw)
            simulation_results[SimulationResults.NumBatteries].append(num_batteries)
            simulation_results[SimulationResults.Cost].append(
                simulate_use(demand=demand,
                             normalised_production=normalised_production,
                             params=params,
                             solar_panel_power_mw=solar_panel_power_mw,
                             num_batteries=num_batteries,
                             strategy=strategy,
                             simulated_year=simulated_year,
                             time_span=time_span))
            counter += 1
            progress_bar.append(counter / total_simulations)
    df_results = SimulationResults(pd.DataFrame.from_dict(simulation_results))
    optimal_scenario = df_results.df.loc[df_results.df[df_results.Cost].idxmin()]
    in_bounds = check_reached_edges_of_iterator(solar_panel_power_it_mw=solar_panel_power_it_mw,
                                                num_batteries_it=num_batteries_it,
                                                optimal_power=optimal_scenario[df_results.PowerSolar],
                                                optimal_num_batteries=optimal_scenario[df_results.NumBatteries])
    return df_results, optimal_scenario, in_bounds
