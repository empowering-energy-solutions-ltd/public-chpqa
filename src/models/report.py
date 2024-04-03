import sys

sys.path.insert(0, '..//')

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from src.common import enums
from src.data import schema, source

from . import technology


@dataclass
class CHPQA_report:
  """
  A class to represent a CHPQA report. Calculating efficiencies and Quality index.
  
  Attributes:
    site_name (str): The name of the site.
    type_of_system (enums.SystemType): The type of system.
    data_source (source.DataManager): The data source.
    list_all_units (list[technology.Technology]): A list of all the units.
    number_years_on_scheme (int): The number of years on the scheme.
    resolution (enums.Resolution): The resolution of the data.

  Methods:
    get_total_output: Get the total output of a given energy carrier.
    get_total_input: Get the total input of a given energy carrier.
    get_data_and_pivot: Get the data and pivot it.
    calculate_power_efficiency: Calculate the power efficiency.
    calculate_heat_efficiency: Calculate the heat efficiency.
    calculate_mechanical_efficiency: Calculate the mechanical efficiency.
    get_max_capacity: Get the maximum capacity of the CHP plant.
    get_X_Y_vals: Get the X and Y values for the CHP plant based on the maximum output.
    calculate_quality_index: Calculates the quality index based on the heat and power efficiencies.
    calculate_qualifying_fuel: Calculates the qualifying fuel based on the quality index.
    calculate_qualifying_outputs: Calculates the qualifying outputs based on the quality index.
  """

  site_name: str
  type_of_system: enums.SystemType
  data_source: source.DataManager
  list_all_units: list[technology.Technology]
  number_years_on_scheme: int = 0
  resolution: enums.Resolution = enums.Resolution.HALFHOURLY
  web_app: bool = False

  def get_total_output(self,
                       energy_carrier: enums.EnergyCarrier) -> pd.DataFrame:
    """
    Get the total output of a given energy carrier.

    Args:
        energy_carrier (enums.EnergyCarrier): The energy carrier.

    Returns:
        pd.DataFrame: A pandas dataframe of ids.
    """
    list_ids = []
    for unit in self.list_all_units:
      for output in unit.technology_outputs:
        if output.energy_carrier is energy_carrier:
          list_ids.append(output.id)
    return self.get_data_and_pivot(list_ids)

  def get_total_input(self,
                      energy_carrier: enums.EnergyCarrier) -> pd.DataFrame:
    """
    Get the total input of a given energy carrier.

    Args:
        energy_carrier (enums.EnergyCarrier): The energy carrier.
    
    Returns:
        self.get_data_and_pivot(list_ids) (pd.DataFrame): A pandas dataframe.
    """
    list_ids = []
    for unit in self.list_all_units:
      if unit.technology_input.energy_carrier is energy_carrier:
        list_ids.append(unit.technology_input.id)
    return self.get_data_and_pivot(list_ids)

  def get_data_and_pivot(self, list_ids: list[int]) -> pd.DataFrame:
    """
    Get the data and pivot it.

    Args:
        list_ids (list[int]): A list of ids.
    
    Returns:
        pd.DataFrame: A pandas dataframe.
    """
    dataf = self.data_source.filter_data(profile_ids=list_ids)
    return dataf.pivot_table(index=schema.DataSchema.DATE,
                             columns=schema.DataSchema.ID,
                             values=schema.DataSchema.VALUE)

  def calculate_power_efficiency(self) -> pd.DataFrame:
    """
    Calculate the power efficiency.

    Returns:
        pd.DataFrame: A pandas dataframe.
    """
    resolution_key = self.resolution.value
    total_gas = self.get_total_input(
        enums.EnergyCarrier.NATURALGAS).resample(resolution_key).sum()
    total_power = self.get_total_output(
        enums.EnergyCarrier.ELECTRICITY).resample(resolution_key).sum()
    dataf = pd.concat([total_power.sum(axis=1), total_gas.sum(axis=1)], axis=1)
    dataf.columns = [
        enums.EnergyCarrier.ELECTRICITY.name,
        enums.EnergyCarrier.NATURALGAS.name
    ]
    return (dataf[enums.EnergyCarrier.ELECTRICITY.name] /
            dataf[enums.EnergyCarrier.NATURALGAS.name]).to_frame()

  def calculate_heat_efficiency(self) -> pd.DataFrame:
    """
    Calculate the heat efficiency.

    Returns:
        pd.DataFrame: A pandas dataframe.
    """
    resolution_key = self.resolution.value
    total_gas = self.get_total_input(
        enums.EnergyCarrier.NATURALGAS).resample(resolution_key).sum()
    total_heat = self.get_total_output(
        enums.EnergyCarrier.HEATING).resample(resolution_key).sum()
    dataf = pd.concat([total_heat.sum(axis=1), total_gas.sum(axis=1)], axis=1)
    dataf.columns = [
        enums.EnergyCarrier.HEATING.name, enums.EnergyCarrier.NATURALGAS.name
    ]
    return (dataf[enums.EnergyCarrier.HEATING.name] /
            dataf[enums.EnergyCarrier.NATURALGAS.name]).to_frame()

  def calculate_mechanical_efficiency(self):
    pass

  def get_max_capacity(self) -> float:
    """
    Get the maximum capacity of the CHP plant.

    Returns:
        int: The maximum capacity of the system.
    """
    max_cap = 0
    for unit in self.list_all_units:
      if unit.technology_type is enums.TechnologyType.CHPPLANT:
        if unit.installed_capacity[enums.EnergyCarrier.ELECTRICITY] > max_cap:
          max_cap = unit.installed_capacity[enums.EnergyCarrier.ELECTRICITY]
        else:
          pass
      else:
        pass
    return max_cap

  def get_X_Y_vals(self) -> tuple[Any, Any]:
    """
    Get the X and Y values for the CHP plant based on the maximum output.

    Returns:
        pd.DataFrame: A pandas dataframe made of the x and y values for the sized system installed.
    """
    sheet_path = Path(r"..//src/data/x_y_coeff_vals - Sheet1.csv")
    if self.web_app:
      sheet_path = Path(r"..//CHPQA/src/data/x_y_coeff_vals - Sheet1.csv")
    table = pd.read_csv(sheet_path)
    max_capacity_val = self.get_max_capacity()
    key: int = 0
    if max_capacity_val <= 1:
      key = 1
    elif max_capacity_val > 1 and max_capacity_val <= 10:
      key = 10
    elif max_capacity_val > 10 and max_capacity_val <= 25:
      key = 25
    elif max_capacity_val > 25 and max_capacity_val <= 50:
      key = 50
    elif max_capacity_val > 50 and max_capacity_val <= 100:
      key = 100
    elif max_capacity_val > 100 and max_capacity_val <= 200:
      key = 200
    elif max_capacity_val > 200 and max_capacity_val <= 500:
      key = 500
    elif max_capacity_val > 500:
      key = 501
    row_data = table[table['key_col'] == key]
    return row_data[schema.xyvalSchema.X_coef].values[0], row_data[
        schema.xyvalSchema.Y_coef].values[0]

  def calculate_quality_index(self) -> pd.DataFrame:
    """
    Calculates the quality index based on the heat and power efficiencies.

    Returns:
        pd.DataFrame: A pandas dataframe containing all relevant data (n_power, n_heat & QI val).
    """
    X, Y = self.get_X_Y_vals()
    n_power = self.calculate_power_efficiency()
    n_heat = self.calculate_heat_efficiency()
    dataf = pd.concat([n_power, n_heat], axis=1)
    dataf.columns = [schema.CHPQASchema.n_power, schema.CHPQASchema.n_heat]
    dataf[schema.CHPQASchema.qi_val] = X * dataf[
        schema.CHPQASchema.n_power] + Y * dataf[schema.CHPQASchema.n_heat]
    return dataf

  def calculate_qualifying_fuel(self) -> pd.DataFrame:
    """
    Calculates the qualifying fuel based on the quality index.

    Returns:
        pd.DataFrame: A pandas dataframe containing calculate_quality_index and qualifying input fuel.
    """
    n_power_threshold = 0.2
    resolution_key = self.resolution.value
    dataf = self.calculate_quality_index()
    total_gas = self.get_total_input(
        enums.EnergyCarrier.NATURALGAS).resample(resolution_key).sum()

    filt = dataf[schema.qualifyingSchema.n_power] >= n_power_threshold
    dataf[schema.qualifyingSchema.Total_gas] = total_gas.sum(axis=1)
    dataf[schema.qualifyingSchema.qi_fuel] = dataf[
        schema.qualifyingSchema.Total_gas]
    dataf.loc[~filt, schema.qualifyingSchema.qi_fuel] = (
        (dataf.loc[~filt, schema.qualifyingSchema.n_power] *
         dataf.loc[~filt, schema.qualifyingSchema.Total_gas]) /
        n_power_threshold).values
    return dataf

  def calculate_qualifying_outputs(self) -> pd.DataFrame:
    """
    Calculates the qualifying outputs based on the quality index.

    Returns:
        pd.DataFrame: A pandas dataframe containing calculate_quality_fuel outputs and qualifying output energy.
    """
    qi_threshold = 100
    resolution_key = self.resolution.value
    X, Y = self.get_X_Y_vals()
    dataf = self.calculate_qualifying_fuel()
    filt_2 = dataf[schema.qualifyingSchema.qi_val] >= qi_threshold
    total_power = self.get_total_output(
        enums.EnergyCarrier.ELECTRICITY).resample(resolution_key).sum()
    total_heat = self.get_total_output(
        enums.EnergyCarrier.HEATING).resample(resolution_key).sum()
    dataf[schema.qualifyingSchema.CHP_elec] = total_power.sum(axis=1)
    dataf[schema.qualifyingSchema.Total_heat] = total_heat.sum(axis=1)
    dataf[schema.qualifyingSchema.qi_power] = dataf[
        schema.qualifyingSchema.CHP_elec]
    dataf.loc[~filt_2, schema.qualifyingSchema.n_heat_new] = (
        qi_threshold -
        (X * dataf.loc[~filt_2, schema.qualifyingSchema.n_power])) / Y
    dataf.loc[~filt_2, schema.qualifyingSchema.heat_power_ratio] = dataf.loc[
        ~filt_2, schema.qualifyingSchema.n_heat_new] / dataf.loc[
            ~filt_2, schema.qualifyingSchema.n_power]
    dataf.loc[~filt_2, schema.qualifyingSchema.qi_power] = dataf.loc[
        ~filt_2, schema.qualifyingSchema.Total_heat] / dataf.loc[
            ~filt_2, schema.qualifyingSchema.heat_power_ratio]
    return dataf
