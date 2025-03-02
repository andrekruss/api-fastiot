from enum import Enum

class MeasurementUnit(str, Enum):
    # Temperature
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"
    KELVIN = "kelvin"

    # Velocity
    METERS_PER_SECOND = "m/s"
    KILOMETERS_PER_HOUR = "km/h"

    # Acceleration
    METERS_PER_SECOND_SQUARED = "m/s²"

    # Time
    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"

    # Pressure
    PASCAL = "pascal"
    BAR = "bar"

    # Mass
    KILOGRAM = "kilogram"
    GRAM = "gram"

    # Voltage
    VOLT = "volt"
    MILLIVOLT = "millivolt"