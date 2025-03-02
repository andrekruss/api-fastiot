from pydantic import BaseModel

from enums.measurement_type import MeasurementType
from enums.measurement_unit import MeasurementUnit


class DataType(BaseModel):
    
    measurement_type: MeasurementType
    measurement_unit: MeasurementUnit

    def validate_unit(self):
        """Ensures the unit belongs to the correct measurement type."""
        valid_units = {
            MeasurementType.TEMPERATURE: {MeasurementUnit.CELSIUS, MeasurementUnit.FAHRENHEIT, MeasurementUnit.KELVIN},
            MeasurementType.VELOCITY: {MeasurementUnit.METERS_PER_SECOND, MeasurementUnit.KILOMETERS_PER_HOUR},
            MeasurementType.ACCELERATION: {MeasurementUnit.METERS_PER_SECOND_SQUARED},
            MeasurementType.TIME: {MeasurementUnit.SECOND, MeasurementUnit.MINUTE, MeasurementUnit.HOUR},
            MeasurementType.PRESSURE: {MeasurementUnit.PASCAL, MeasurementUnit.BAR},
            MeasurementType.MASS: {MeasurementUnit.KILOGRAM, MeasurementUnit.GRAM},
            MeasurementType.VOLTAGE: {MeasurementUnit.VOLT, MeasurementUnit.MILLIVOLT},
        }
        if self.measurement_unit not in valid_units.get(self.measurement_type, set()):
            raise ValueError(f"Invalid unit '{self.measurement_unit}' for measurement type '{self.measurement_type}'")