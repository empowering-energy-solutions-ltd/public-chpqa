class DataSchema:
  DATE = 'Datetime'
  ID = 'ID'
  VALUE = 'Value'


class MetadataSchema:
  """Schema used to ensure that the metadata information is fully and correclty filled."""
  ENERGY_CARRIER = 'energy_carrier'
  UNIT = 'Unit'
  ORG_NAME = 'original_name'
  ORIGIN_ENTITY_ID = 'origin_ID'
  DESTINATION_ENTITY_ID = 'destination_ID'
  PROFILE_ID = DataSchema.ID
  TYPE = 'Type_of_profile'


class StructureSchema:
  UNIT_ID = 'Unit_ID'
  INPUT_ENERGY_CARRIER = 'Input_energy_carrier'
  OUTPUT_ENERGY_CARRIER = 'Output_energy_carrier'
  ORIGIN_ENTITY_ID = 'Origin_entity_ID'
  DESTINATION_ENTITY_ID = 'Destination_entity_ID'
  TYPE = 'Type'


class ResultsSchema:
  DESTINATION = 'Destination'
  ENERGY_CARRIER = 'Energy carrier'
  UNIT = 'Unit'
  INDEX = 'Datetime_UTC'
  NAME = 'Name of unit'
  ORIGIN = 'Origin'


class TariffSchema:
  YEAR = 'Year'
  Month = 'Month'
  CCL = 'CCL'


class outputSchema:
  """A schema for the initial test of the data"""
  Datetime = 'Datetime'
  CHP_heat_total = 'CHP_total_heat'
  CHP_elec = 'CHP_electricity'
  CHP_heat = 'CHP_heat'
  CHP_dump_heat = 'CHP_heat_dump'
  CHP_gas = 'CHP_gas'
  Boiler_1_heat = 'Boiler_1_heat'
  Boiler_2_heat = 'Boiler_2_heat'
  Boiler_3_heat = 'Boiler_3_heat'
  Boiler_1_gas = 'Boiler_1_gas'
  Boiler_2_gas = 'Boiler_2_gas'
  Boiler_3_gas = 'Boiler_3_gas'
  Total_heat = 'Total_heat_MWh'
  Total_gas = 'Total_gas_MWh'
  Total_out_heat = 'Total heat generated [MWh]'
  Total_out_elec = 'Total electricity generated [MWh]'
  Total_vol_fuel = 'Total input fuel [Sm3]'
  Total_input_fuel = 'Total input fuel [MWh]'


class assetUnits:
  CHPPLANT = 'CHP_plant'
  BOILER = 'Boiler'


class CHPQASchema:
  n_power = 'n_power'
  n_heat = 'n_heat'
  qi_val = 'QI'


class xyvalSchema:
  MWe = 'MWe'
  X_coef = 'X_coeff'
  Y_coef = 'Y_coeff'
  key = 'Key_col'


class qualifyingSchema:
  Total_gas = 'Total_gas_MWh'
  Total_heat = 'Total_heat_MWh'
  CHP_elec = 'CHP_electricity'
  n_power = 'n_power'
  n_heat = 'n_heat'
  n_heat_new = 'n_heat_new'
  qi_val = 'QI'
  heat_power_ratio = 'H:P ratio'
  qi_heat = 'qualifying_output_heat'
  qi_power = 'qualifying_output_power'
  qi_fuel = 'qualifying_input_fuel'
