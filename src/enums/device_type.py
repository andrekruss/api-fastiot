from enum import Enum

class DeviceType(str, Enum):
    SENSOR = "sensor"
    ACTUATOR = "actuator"