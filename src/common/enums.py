from enum import Enum, StrEnum, auto

### Good source about how to use Enum:: https://codereview.stackexchange.com/questions/267948/using-python-enums-to-define-physical-units


class SystemType(StrEnum):
  SIMPLE = auto()
  COMPLEX = auto()


class Resolution(Enum):
  YEARLY = 'y'
  MONTHLY = 'm'
  WEEKLY = 'w'
  HOURLY = 'H'
  HALFHOURLY = '30min'


class SimParameters(Enum):
  """Simulation Parameters"""
  COST = 1, "GBP"
  TIMESTEP = 30, "minutes"
  SIMULATION_UNIT = 1, "kW"
  PRICE_UNIT = 1, "GBP/kWh"
  EMISSION_UNIT = 1, "kgCO2e/kWh"

  @property
  def magnitude(self) -> int:
    """Get the magnitude which is most commonly used for this unit."""
    return self.value[0]

  @property
  def units(self) -> str:
    """Get the units for which this unit is relevant."""
    return self.value[1]


class PhysicalQuantity(Enum):
  """List of physical quantities recognized."""
  TEMPERATURE = auto()
  ENERGY = auto()
  TIME = auto()
  MASS = auto()
  LENGTH = auto()
  POWER = auto()
  UNCATEGORIZED = auto()

  @classmethod
  def _missing_(cls, value):
    return cls.UNCATEGORIZED


class EnergyCarrier(Enum):
  """Defines the energy carriers considered"""

  ELECTRICITY = auto()
  NATURALGAS = auto()
  HEATING = auto()
  COOLING = auto()
  UNCATEGORIZED = auto()
  NONE = auto()

  @classmethod
  def _missing_(cls, value):
    return cls.NONE


class Destination(Enum):
  """Defines the possible destinations of the flux"""

  IMPORT = auto()
  EXPORT = auto()
  ONSITE = auto()
  INPUT = auto()
  OUTPUT = auto()
  DEMAND = auto()


class TechnologyType(Enum):
  """Defines the possible destinations of the energy"""

  PV = "Photovoltaics panels"
  WINDTURBINE = "Wind turbine"
  CHPPLANT = "Combined heat and power plant"
  BOILERPLANT = "Boiler"
  UNCATEGORIZED = "Uncategorized"
  HEATPUMP = "Heat-pump"
  GRID = "Main grid"
  SITE = "Site"


class Charts(Enum):
  HH_LABEL = "half-hourly"
  DAILY_LABEL = "daily"
  WEEKLY_LABEL = "weekly"
