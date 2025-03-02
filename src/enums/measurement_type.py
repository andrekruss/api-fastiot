from enum import Enum

class MeasurementType(str, Enum):
    TEMPERATURE = "temperature"
    VELOCITY = "velocity"
    ACCELERATION = "acceleration"
    TIME = "time"
    PRESSURE = "pressure"
    MASS = "mass"
    LUMINOSITY = "luminosity"
    HUMIDITY = "humidity"
    VOLTAGE = "voltage"