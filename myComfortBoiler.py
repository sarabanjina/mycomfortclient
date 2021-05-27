#from mycomfortclient.myComfortObject import myComfortObject
from .myComfortObject import myComfortObject
import logging

logger = logging.getLogger("mycomfortclient")

class Boiler(myComfortObject):
    """Representation of a Windhager myComfort boiler."""

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


    def getBoilerTemperature(self):
        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Boiler temp. actual value") + "/0")

    def getBoilerSetpointTemperature(self):
        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Set temperature") + "/0")

    def getExhaustTemperature(self):
        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Temp. Exhaust   ") + "/0")

    def getBufferTemperature(self):
        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Switch/buffer temperature") + "/0")

    def getBurnerStarts(self):
        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Number of burner starts") + "/0", self._gateway._cacheDuration * 10)

    def getBurnerHours(self):
        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Operating hours") + "/0", self._gateway._cacheDuration * 60)

    def getBurnerModulation(self):
        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Current boiler output") + "/0")

    def getOperatingMode(self):
        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Operating mode") + "/0")

    def getOperatingTimeCleaning(self):
        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Operating time until Stage 1 cleaning") + "/0", self._gateway._cacheDuration * 60)

    def getOperatingTimeMainCleaning(self):
        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Operating time until Stage 2 cleaning") + "/0", self._gateway._cacheDuration * 60)

    def getOperatingTimeMaintenance(self):
        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Operating time until Full service") + "/0", self._gateway._cacheDuration * 60)

    def getBoilerConsumptionBulkfill(self):
        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Pellet consumption since bulk fill") + "/0", self._gateway._cacheDuration * 30)

    def getBoilerConsumptionTotal(self):
        return self._gateway.value("/1/" + self._id + "/0/" + self._gateway.oid("Pellet consumption total") + "/0", self._gateway._cacheDuration * 30)

    def getBurnerActive(self):
        burnerActive = {
            "Burner locked": False,
            "Self-test": False,
            "Switch-off heat gener.": False,
            "Stand-by": False,
            "Burner OFF": False,
            "Purging": False,
            "Ignition phase": True,
            "Flame stabilisation": True,
            "Modulation mode": True,
            "Boiler locked": False,
            "Stand-by off period": False,
            "Fan OFF": False,
            "Cladding door open": False,
            "Ignition ready": False,
            "Cancel ignition phase": True,
            "Start procedure": True,
            "Step-loading": True,
            "Burnout": True
        }

        return burnerActive.get(self.getOperatingMode(), False)
