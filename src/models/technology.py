from dataclasses import dataclass

from src.common import enums
from src.data import metering


@dataclass
class Technology:
  """Model of the energy generators of the site for example a CHP unit or a boiler.

  Attributes:
    name (str): Name for the technology object
    technology_input (metering.MeterReader): Input meter for the technology
    technology_outputs (list[metering.MeterReader]): List of output meters for the technology
    installed_capacity (dict[enums.EnergyCarrier, float]): Installed capacity of the technology, one value for each input/output energy carrier.
    technology_type (enums.TechnologyType): ype of the technology, for example CHP, boiler, etc.
  
  Methods:
    get_technology_ids: Get the list of ids of the technology and its outputs"""
  name: str
  # Technical parameters
  technology_input: metering.MeterReader  # single input string: "electricity", "natural gas", etc.
  # list [] of output energy carriers: electricity, heating, cooling, biogas, etc.
  technology_outputs: list[metering.MeterReader]
  # dict of installed capacity of the technology for a CHP this would be {"electricity": 600, "heating":800}
  installed_capacity: dict[enums.EnergyCarrier, float]

  technology_type: enums.TechnologyType

  def get_technology_ids(self) -> list[int]:
    """Get the list of ids of the technology and its outputs
    Returns:
        list_ids (list[int]): List of ids of the technology and its outputs
    """
    list_ids = []
    list_ids.append(self.technology_input.id)
    for temp_output in self.technology_outputs:
      list_ids.append(temp_output.id)
    return list_ids
