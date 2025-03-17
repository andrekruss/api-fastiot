class DeviceNotFoundException(Exception):
    "Exception used for failed device search."

    def __init__(self, message: str = "Couldn't find device."):
        self.message = message

    def __str__(self):
        return self.message