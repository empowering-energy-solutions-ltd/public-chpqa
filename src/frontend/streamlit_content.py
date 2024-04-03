import sys

sys.path.insert(0, '..//')

from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

from src.common import enums
from src.data import metering, schema, source
from src.frontend.utils import (CUSTOMER_SITE, OutputSchema, PlotSchema,
                                ReportSchema, compile_sl_data, prepare_dataf)
from src.models import report, technology


def generate_annual_qi_data(report_obj: report.CHPQA_report) -> pd.DataFrame:
  """ Calculates the qualifying values for the CHP system on an annual basis.
  
  Args:
      report_obj (report.CHPQA_report): A CHPQA report object.
      
  Returns:
      pd.DataFrame: A pandas dataframe with the annual qualifying values."""
  report_obj.resolution = enums.Resolution.YEARLY
  return report_obj.calculate_qualifying_outputs()


def generate_qi_and_eff_data(report_obj: report.CHPQA_report) -> pd.DataFrame:
  """ Calculates the qualifying values for the CHP system on a monthly basis for plotting.
  
  Args:
      report_obj (report.CHPQA_report): A CHPQA report object.
      
  Returns:
      pd.DataFrame: A pandas dataframe with the monthly qualifying values."""
  report_obj.resolution = enums.Resolution.MONTHLY
  report_dataf = report_obj.calculate_qualifying_outputs()
  output = pd.DataFrame(index=report_dataf.index)
  output[OutputSchema.n_power] = report_dataf[ReportSchema.n_power] * 100
  output[OutputSchema.n_heat] = report_dataf[ReportSchema.n_heat] * 100
  output[OutputSchema.qi] = report_dataf[ReportSchema.qi]
  output[OutputSchema.qif] = report_dataf[ReportSchema.qif]
  output[OutputSchema.qop] = report_dataf[ReportSchema.qop]
  return output


def generate_qi_plot(result_dataf: pd.DataFrame) -> plt.Figure:
  """ Plots the monthly Quality Index for the CHP system.
  
  Args:
      result_dataf (pd.DataFrame): A pandas dataframe with the monthly qualifying values.
  
  Returns:
      matplotlib.figure.Figure: A matplotlib figure object."""
  fig, ax = plt.subplots(figsize=(15, 7))
  ax.plot(result_dataf[OutputSchema.qi], marker='o')
  ax.axhline(y=100, color='r', linestyle='--')
  ax.set_title(PlotSchema.qi_title)
  ax.set_ylabel(PlotSchema.qi_y_label)
  ax.set_xlabel(PlotSchema.qi_x_label)
  ax.legend([PlotSchema.qi_title, PlotSchema.qi_legend])
  ax.grid()
  return fig


def generate_h_eff_plot(result_dataf: pd.DataFrame) -> plt.Figure:
  """ Plots the monthly heat efficiency for the CHP system.
  
  Args:
      result_dataf (pd.DataFrame): A pandas dataframe with the monthly qualifying values.
      
  Returns:
      matplotlib.figure.Figure: A matplotlib figure object."""
  fig, ax = plt.subplots(figsize=(15, 7))
  ax.plot(result_dataf[OutputSchema.n_heat], marker='o')
  ax.axhline(y=20, color='r', linestyle='--')
  ax.set_title(PlotSchema.h_eff_title)
  ax.set_ylabel(PlotSchema.h_eff_y_label)
  ax.set_xlabel(PlotSchema.h_eff_x_label)
  ax.legend([PlotSchema.h_eff_title, PlotSchema.h_eff_legend])
  ax.grid()
  return fig


def generate_p_eff_plot(result_dataf: pd.DataFrame) -> plt.Figure:
  """ Plots the monthly power efficiency for the CHP system.
  
  Args:
      result_dataf (pd.DataFrame): A pandas dataframe with the monthly qualifying values.
  
  Returns:
      matplotlib.figure.Figure: A matplotlib figure object."""
  fig, ax = plt.subplots(figsize=(15, 7))
  ax.plot(result_dataf[OutputSchema.n_power], marker='o')
  ax.axhline(y=20, color='r', linestyle='--')
  ax.set_title(PlotSchema.p_eff_title)
  ax.set_ylabel(PlotSchema.p_eff_y_label)
  ax.set_xlabel(PlotSchema.p_eff_x_label)
  ax.legend([PlotSchema.p_eff_title, PlotSchema.p_eff_legend])
  ax.grid()
  return fig


def prep_bms_data(bms_uploadfile: Any) -> pd.DataFrame:
  """ Streamlit allows for data upload. Here we take the data and 
    prepare it for use in the simplified report.
  
  Args:
      bms_uploadfile (Any): The uploaded file.
      
  Returns:
      pd.DataFrame: A pandas dataframe with the prepared data."""
  return compile_sl_data(bms_uploadfile).pipe(prepare_dataf)


def create_meter(meter_name: str, energy_carrier: enums.EnergyCarrier,
                 lookup_dict: dict[str, int]) -> metering.MeterReader:
  """ Create a meter object.
  
  Args:
      meter_name (str): The name of the meter.  
      energy_carrier (enums.EnergyCarrier): The energy carrier.  
      lookup_dict (dict[str, int]): A dictionary with the mapping of the meter names to the meter ids.  
  
  Returns:
      metering.MeterReader: A meter object."""
  meter_id = lookup_dict[meter_name]
  return metering.MeterReader(meter_name, energy_carrier, meter_id)


def create_capacity_dict(
    max_capacity: float) -> dict[str, dict[enums.EnergyCarrier, float]]:
  """ Create a dictionary with the capacity of the CHP system.

  Args:
      max_capacity (float): The maximum capacity of the CHP system.

  Returns:
      dict[str, dict[enums.EnergyCarrier, float]]: A dictionary with the capacity of the CHP system."""
  return {
      schema.assetUnits.CHPPLANT: {
          enums.EnergyCarrier.ELECTRICITY: max_capacity,
          enums.EnergyCarrier.HEATING: max_capacity / 0.944 * 0.8
      }
  }


def create_system(
    capacity_dict: dict[str, dict[enums.EnergyCarrier, float]],
    meter_id_dict: dict[str, int]) -> list[technology.Technology]:
  """ Create a list of technology objects.

  Args:
      capacity_dict (dict[str, dict[enums.EnergyCarrier, float]]): A dictionary with the capacity of the CHP system.  
      meter_id_dict (dict[str, int]): A dictionary with the mapping of the meter names to the meter ids.  
  
  Returns:
      list[technology.Technology]: A list of technology objects.
  """
  CHP_1_gas = create_meter(schema.outputSchema.Total_input_fuel,
                           enums.EnergyCarrier.NATURALGAS, meter_id_dict)
  CHP_1_heat = create_meter(schema.outputSchema.Total_out_heat,
                            enums.EnergyCarrier.HEATING, meter_id_dict)
  CHP_1_elec = create_meter(schema.outputSchema.Total_out_elec,
                            enums.EnergyCarrier.ELECTRICITY, meter_id_dict)

  chp_1 = technology.Technology(schema.assetUnits.CHPPLANT, CHP_1_gas,
                                [CHP_1_elec, CHP_1_heat],
                                capacity_dict[schema.assetUnits.CHPPLANT],
                                enums.TechnologyType.CHPPLANT)

  return [chp_1]


def generate_chpqa_report(bms_uploadfile: Any,
                          max_capacity: float) -> report.CHPQA_report:
  """ Generates a simplified CHPQA report object. This is used to 
    generate plots, and qualifying values.
    
    The simpliefied report is very similar to the original report but 
    only uses the columns Total electricity generated, Total heat generated,
    and Total input fuel. This is because the original report requires Veolia 
    specific data. The simplified report is more flexible.

  Args:
      bms_uploadfile (Any): The uploaded file.  
      max_capacity (float): The maximum capacity of the CHP system.  

  Returns:
      report.CHPQA_report: A CHPQA report object.
    """
  bms_data = prep_bms_data(bms_uploadfile)
  data_source = source.DataManager("Site data manager")
  capacity_dict = create_capacity_dict(max_capacity)
  meter_id_dict = data_source.load_new_data(bms_data)
  list_units = create_system(capacity_dict, meter_id_dict)
  report_obj = report.CHPQA_report("Test Site",
                                   enums.SystemType.COMPLEX,
                                   data_source,
                                   list_units,
                                   web_app=True)
  return report_obj


def calculate_qi_fuel(annual_data: pd.DataFrame) -> float:
  """ Calculates the annual fuel quality index.

  Args:
      annual_data (pd.DataFrame): A pandas dataframe with the annual qualifying values.

  Returns:
      float: The annual fuel quality index."""
  return round(((annual_data[ReportSchema.qif][0] * 1000) * 0.00672), 2)
