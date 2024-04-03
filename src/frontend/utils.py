import os
from typing import Any

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
CUSTOMER_SITE = "Your Site"

SM3_TO_MWH = (39.3 / 3.6) / 1000


class TextSchema:
  page_header = "Lets check your CHPQA quality"
  emoji = ":factory:"
  app_desc = "This app is designed to calculate the Quality Index for a CHP system this can include or exclude Boilers. Data must be in timeseries format and have columns:"
  total_elec = "**Total electricity generated [MWh]**"
  total_heat = "**Total heat generated [MWh]**"
  total_input_fuel = "**Total input fuel [Sm3]** or **Total input fuel [MWh]**: Provide input fuel either as MWh or meters cubed. If input fuel is provided in meters cubed, it will be converted to MWh using a conversion factor of 39.3 MWh/m3."
  total_dump_heat = "**Total dump heat [MWh]:** can be added if measured. Note: dumped heat is not accepted as part of Total heat generated and must be retracted from the total amount."
  user_docs = "Your documents"
  upload_docs = "Upload your CHP + boiler BMS data here"
  max_cap = "Enter the maximum capacity of your CHP in MWe"
  process = "Process"
  processing = "Processing"
  chpqa_score = "Your CHPQA score for system size "
  qi_threshold_note = "**Note**: Threshold for Quality Index is a score of 100."
  high_qi = "**Congratulations!** You've achieved a high Quality Index. This means that all of your input fuel qualifies. Based on a climate change levy of 0.00672 GBP/kWh you'll be able to claim back approximately <u>£"
  low_qi = "Unfortunetly your systems performance has not reached a Quality index of 100, because of this, you will not be able to claim back the climate change levy on all of your input fuel. Based on a climate change levy of 0.00672 GBP/kWh you'll be able to claim back approximately <u>£"
  plot_subheader = "Lets have a closer look at your systems performance over the period!"
  enter_creds = "Please enter your Auth0 credentials to continue."
  bad_creds = "Incorrect user credentials"


class ReportSchema:
  n_power = "n_power"
  n_heat = "n_heat"
  qi = "QI"
  qif = "qualifying_input_fuel"
  qop = "qualifying_output_power"


class OutputSchema:
  n_power = "Power Eff (%)"
  n_heat = "Heat Eff (%)"
  qi = "Quality Index"
  qif = "QIF (MWh)"
  qop = "QOP (MWh)"


class PlotSchema:
  qi_title = "Quality Index"
  qi_y_label = "Quality Index Value"
  qi_x_label = "Datetime"
  qi_legend = "Quality Index Threshold"
  h_eff_title = "Heat efficiency"
  h_eff_y_label = "Efficiency Value (%)"
  h_eff_x_label = "Datetime"
  h_eff_legend = "Heat Efficiency Threshold"
  p_eff_title = "Power efficiency"
  p_eff_y_label = "Efficiency Value (%)"
  p_eff_x_label = "Datetime"
  p_eff_legend = "Power Efficiency Threshold"


def compile_sl_data(uploaded_files: list[Any]) -> pd.DataFrame:
  """ Compile data from streamlit file uploader and return a pandas dataframe.
  
  Args:
      uploaded_files (list[Any]): A list of uploaded files.
      
  Returns:
      pd.DataFrame: A pandas dataframe with the compiled data."""
  appended_data = []

  for uploaded_file in uploaded_files:
    raw_data = pd.read_csv(uploaded_file)
    appended_data.append(raw_data)

  all_raw_data = pd.concat(appended_data, ignore_index=True)

  return all_raw_data


def prepare_dataf(dataf: pd.DataFrame) -> pd.DataFrame:
  """ Prepare the data for analysis.

  Args:
      dataf (pd.DataFrame): A pandas dataframe.

  Returns:
      pd.DataFrame: A pandas dataframe with the prepared data."""
  dataf.index = pd.DatetimeIndex(dataf['From Timestamp'])
  if 'Total dump heat [MWh]' not in dataf.columns:
    dataf['Total dump heat [MWh]'] = 0
  if 'Total input fuel [MWh]' not in dataf.columns:
    dataf['Total input fuel [MWh]'] = dataf[
        'Total input fuel [Sm3]'] * SM3_TO_MWH
  dataf['Total heat generated [MWh]'] = dataf[
      'Total heat generated [MWh]'] - dataf['Total dump heat [MWh]']
  return dataf


def verify_login(email: str, password: str) -> bool:
  """ Uses requests to query the FastAPI backend to verify the \
        users credentials. If the credentials are correct it \
        returns True, else False.
  
  Args:
      email (str): The users email.  
      password (str): The users password.

  Returns:
      bool: A boolean value indicating if the user is verified.
      """
  verify = False
  try:
    print(os.getenv('AUTH0_DOMAIN_QUOTED'))
    token = requests.get("http://127.0.0.1:8000/streamlit/login",
                         params={
                             "username": email,
                             "password": password
                         })
    print(token)
    access_token = 'Bearer ' + token.text.replace('"', '')
    access = requests.get("http://127.0.0.1:8000/streamlit/verify",
                          headers={"Authorization": access_token})
    if access.status_code == 200:
      verify = True
  except Exception as e:
    st.error(e)
  return verify
