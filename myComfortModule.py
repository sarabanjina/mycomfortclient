#from mycomfortclient.myComfortObject import myComfortObject
from .myComfortObject import myComfortObject
import logging

logger = logging.getLogger("mycomfortclient")

class Module(myComfortObject):
    """Representation of a Windhager myComfort module."""

    def __init__(self, name, serial_no, id, gateway):
        super().__init__()

        self._name = name
        self._serial_no = serial_no
        self._id = id
        self._gateway = gateway

    @property
    def serial_no(self):
        """Return the serial number of the boiler."""
        return self._serial_no

    @property
    def name(self):
        """Return the name of the boiler."""
        return self._name

    def getOutsideTemperature(self):
        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Outside temperature") + "/0")

    def getFlowTemperature(self):
        return self._gateway.value("/1/" + self._id + "/0/" + "0/2" + "/0")
#        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Actual") + "/0")

    def getFlowSetpointTemperature(self):
        return self._gateway.value("/1/" + self._id + "/0/" + "1/2" + "/0", self._gateway._cacheDuration * 5)
#        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Set point") + "/0")

    def isDHWCircuit(self):
        return int(self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("DHW circuit") + "/0", self._gateway._cacheDuration * 60))

    def getDHWTemperature(self):
        return self._gateway.value("/1/" + self._id + "/0/" + "0/4" + "/0")
#        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Actual") + "/0")

    def getDHWSetpointTemperature(self):
        return self._gateway.value("/1/" + self._id + "/0/" + "1/4" + "/0", self._gateway._cacheDuration * 5)
#        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Set point") + "/0")

    def getActiveProgram(self):
        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Select mode\t") + "/0", self._gateway._cacheDuration * 5)

    def getOperationMode(self):
        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Operation mode") + "/0", self._gateway._cacheDuration * 5)

    def getBurnerActive(self):
        return self._gateway.boilers()[0].getBurnerActive()

    def getCurrentDesiredTemperature(self):
        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Set point") + "/0", self._gateway._cacheDuration * 5)

    def getRoomTemperatureSetpoint(self):
        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Set point") + "/0", self._gateway._cacheDuration * 5)

    def setRoomTemperatureSetpoint(self, temperature):
        return self._gateway.setValue("/1/" + self._id + "/0/" + self._gateway.oid("Temperature") + "/0", str(temperature))

    def setDuration(self, duration):
        return self._gateway.setValue("/1/" + self._id + "/0/" + self._gateway.oid("Duration") + "/0", str(duration))
