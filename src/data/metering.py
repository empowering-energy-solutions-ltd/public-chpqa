from dataclasses import dataclass, field

from src.common import enums


@dataclass
class Sensor:
  uncertainty: float = 1


@dataclass
class MeterReader:
  name: str
  energy_carrier: enums.EnergyCarrier
  id: int
  sensor: Sensor = field(default_factory=Sensor)
