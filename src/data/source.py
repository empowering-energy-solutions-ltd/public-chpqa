from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import pandas as pd

from . import schema


@dataclass
class DataManager:
  """Stores the BMS data for the systems on site.
  
  Attributes:
    name (str): Name for the data manager object
  
  Methods:
    transform_new_data: Transform the new data into a tidy dataframe.
    all_profile_ids: Get all the profile ids
    create_empty_database: Create an empty database
    load_new_data: Load new data. input_dataf is is in the format column=[name of each meter] and index=datetime
    append_new_data: Append new data to the existing database
    filter_data: Filter the data based on the start and end time and the profile ids
    
  """
  name: str
  _data: pd.DataFrame = field(init=False)

  def __post_init__(self) -> None:
    self.create_empty_database()

  def transform_new_data(self, input_dataf: pd.DataFrame,
                         profile_ID_map: dict[str, int]) -> pd.DataFrame:
    """Transform the new data into a tidy dataframe.
    
    Args:
        input_dataf (pd.DataFrame): A pandas dataframe to transform.  
        profile_ID_map (dict[str, int]): A dictionary with the mapping of the profile names to the profile ids.
        
    Returns:
        pd.DataFrame: A pandas dataframe tp append to the existing database.
    """
    df_to_append = input_dataf.stack().to_frame().reset_index()
    df_to_append.columns = [
        schema.DataSchema.DATE, schema.DataSchema.ID, schema.DataSchema.VALUE
    ]
    df_to_append[schema.DataSchema.ID] = df_to_append[
        schema.DataSchema.ID].map(profile_ID_map)
    return df_to_append

  @property
  def all_profile_ids(self) -> list[int]:
    """Get all the profile ids
    
    Returns:
        list[int]: A list of all the profile ids.
    """
    return self._data[schema.DataSchema.ID].unique().tolist()

  def create_empty_database(self) -> None:
    """Create an empty database.
    """
    columns = [(schema.DataSchema.DATE, "datetime64[ns]"),
               (schema.DataSchema.ID, int), (schema.DataSchema.VALUE, float)]
    self._data = pd.DataFrame({
        col_name: pd.Series(dtype=col_type)
        for col_name, col_type in columns
    })

  def load_new_data(self, input_dataf: pd.DataFrame) -> dict[str, int]:
    """Load new data. input_dataf is in the format column=[name of each meter] and index=datetime
    
    Args:
        input_dataf (pd.DataFrame): A pandas dataframe.
    
    Returns:
        dict[str, int]: A dictionary with the mapping of the profile names to the profile ids.
    """
    profile_ID_lookup: dict[str, int] = {}

    for column_name in input_dataf.columns:
      temp_profile_ID = hash(column_name)
      profile_ID_lookup[column_name] = temp_profile_ID

    new_data_to_append = self.transform_new_data(input_dataf,
                                                 profile_ID_lookup)
    self.append_new_data(new_data_to_append)
    return profile_ID_lookup

  def append_new_data(self, new_data: pd.DataFrame) -> None:
    """Append new data to the existing database.
    
    Args:
        new_data (pd.DataFrame): A pandas dataframe to append to the existing database.
    """
    self._data = pd.concat([self._data, new_data], axis=0)
    self._data.reset_index(inplace=True, drop=True)

  def filter_data(self,
                  start_time: Optional[datetime] = None,
                  end_time: Optional[datetime] = None,
                  profile_ids: Optional[list[int]] = None) -> pd.DataFrame:
    """Filter the data based on the start and end time and the profile ids.

    Args:
        start_time (Optional[datetime]): Start time for the filter.  
        end_time (Optional[datetime]): End time for the filter.  
        profile_ids (Optional[list[int]]): List of profile ids to filter the data.  

    Returns:
        pd.DataFrame: A pandas dataframe with the filtered data.
    """
    if start_time is None:
      start_time = self._data[schema.DataSchema.DATE].min()
    if end_time is None:
      end_time = self._data[schema.DataSchema.DATE].max()
    if profile_ids is None:
      profile_ids = self.all_profile_ids
    filt = (self._data[schema.DataSchema.ID].isin(profile_ids)
            & self._data[schema.DataSchema.DATE].between(
                start_time, end_time, inclusive="both"))

    return self._data.loc[filt].copy()
