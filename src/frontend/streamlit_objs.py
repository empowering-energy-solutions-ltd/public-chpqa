import sys

sys.path.insert(0, '..//CHPQA')

from typing import Optional

import pandas as pd
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from utils import TextSchema, verify_login

from src.frontend import streamlit_content as sc
from src.models import report


def description_box() -> DeltaGenerator:
  """ Create a description container at the top of the streamlit app.
  
  Returns:
      desc_container (DeltaGenerator): Streamlit container with the description of the app."""
  desc_container = st.container(border=True)
  desc_container.markdown(TextSchema.app_desc)
  desc_container.markdown(TextSchema.total_elec)
  desc_container.markdown(TextSchema.total_heat)
  desc_container.markdown(TextSchema.total_input_fuel)
  desc_container.markdown(TextSchema.total_dump_heat)
  return desc_container


def qi_score_box(qi_score: float, max_capacity: float,
                 monthly_data: pd.DataFrame,
                 annual_data: pd.DataFrame) -> DeltaGenerator:
  """Create a container with the Quality Index score and the calculated Qualifying Input Fuel.
  
  Args:
      qi_score (float): Quality Index score  
      max_capacity (float): Maximum capacity of the CHP unit  
      monthly_data (pd.DataFrame): Monthly data of the CHP unit  
      annual_data (pd.DataFrame): Annual data of the CHP unit  
    
  Returns:
      DeltaGenerator: Streamlit container with the Quality Index score and the calculated Qualifying Input Fuel."""
  qi_score_container = st.container(border=True)
  qi_score_container.subheader(TextSchema.chpqa_score + str(max_capacity) +
                               " from " + str(monthly_data.index.date.min()) +
                               " to " + str(monthly_data.index.date.max()))
  qi_score_container.subheader(f"**{round(qi_score, 1)}**")
  qi_score_container.caption(TextSchema.qi_threshold_note)
  qi_fuel = sc.calculate_qi_fuel(annual_data)
  if qi_score >= 100:
    text = TextSchema.high_qi + str(qi_fuel) + "</u>."
  else:
    text = TextSchema.low_qi + str(qi_fuel) + "</u>."

  qi_score_container.markdown(text, unsafe_allow_html=True)
  return qi_score_container


def plot_box(monthly_data: pd.DataFrame) -> DeltaGenerator:
  """Create a container with the Quality Index and efficiency plots.

  Args:
      monthly_data (pd.DataFrame): Monthly data of the CHP unit
  
  Returns:
      DeltaGenerator: Streamlit container with the Quality Index and efficiency plots."""

  plot_container = st.container(border=True)
  plot_container.subheader(TextSchema.plot_subheader)
  plot_container.pyplot(fig=sc.generate_qi_plot(monthly_data))
  plot_container.pyplot(fig=sc.generate_h_eff_plot(monthly_data))
  plot_container.pyplot(fig=sc.generate_p_eff_plot(monthly_data))
  return plot_container


def login_box() -> DeltaGenerator:
  """Create a container with the login form.

  Returns:
      DeltaGenerator: Streamlit container with the login form."""

  login_container = st.container(border=True)
  login_container.markdown(TextSchema.enter_creds)
  email = login_container.text_input("Email")
  password = login_container.text_input("Password", type="password")
  log_btn = login_container.button("Login")
  if log_btn:
    verified = verify_login(email, password)
    if verified:
      st.session_state['logged_in'] = True
    else:
      st.error(TextSchema.bad_creds)
  return login_container


def logged_in_content():
  """Create the main content of the app for a logged in user.
  """

  description_box()
  report_obj: Optional[report.CHPQA_report] = None
  with st.sidebar:
    st.subheader(TextSchema.user_docs)
    bms_uploadfile = st.file_uploader(TextSchema.upload_docs,
                                      accept_multiple_files=True)
    max_capacity = st.number_input(TextSchema.max_cap,
                                   min_value=0.0,
                                   value=0.0,
                                   step=0.01)
    if bms_uploadfile and max_capacity:
      process_btn = st.button(TextSchema.process)
      if process_btn:
        with st.spinner(TextSchema.processing):
          report_obj = sc.generate_chpqa_report(bms_uploadfile, max_capacity)
  if report_obj is not None:
    annual_data = sc.generate_annual_qi_data(report_obj)
    qi_score = annual_data['QI'][0]
    monthly_data = sc.generate_qi_and_eff_data(report_obj)
    qi_score_box(qi_score, max_capacity, monthly_data, annual_data)
    plot_box(monthly_data)
