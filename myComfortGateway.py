from datetime import datetime
from datetime import timezone
import threading
from requests.auth import HTTPDigestAuth
import threading
import logging

#from mycomfortclient.myComfortObject import myComfortObject
#from mycomfortclient.myComfortBoiler import Boiler
#from mycomfortclient.myComfortModule import Module
#from mycomfortclient.VarIdentTexte import VarIdentTexte
#from mycomfortclient.AufzaehlTexte import AufzaehlTexte
from .myComfortObject import myComfortObject
from .myComfortBoiler import Boiler
from .myComfortModule import Module
from .VarIdentTexte import VarIdentTexte
from .AufzaehlTexte import AufzaehlTexte

logger = logging.getLogger("mycomfortclient")

from pprint import pprint

apiURLPath = "/api/1.0/lookup" # return a realtime value (slow)
apiURLCachePath = "/api/1.0/datapoint" # return  a 30 sec cached value
apiURLFullCachePath = "/api/1.0/datapoints" # return every cached values

class Gateway(myComfortObject):
    """Representation of a Windhager myComfort (RC7030) Gateway."""

    def __init__(self, hostname, port, username, password, cacheDuration=60, logginglevel=logging.WARNING):
        super().__init__()

        self._gateway = self
        self._hostname = hostname
        self._port = port
        self._cacheDuration = int(cacheDuration)
        logger.setLevel(logginglevel)

        self._installation = []
        self._boilers = []
        self._modules = []
        self._cache = {}
        self._VarIdentTexte = None
        self._AufzaehlTexte = None
        self._lock = threading.Lock()
        self._name = ""
        self._serial_no = ""
        self._id = ""

        self._username = username
        self._password = password
        self._auth = HTTPDigestAuth(username, password)

        self._getInstallation()
        self._refreshCache()
        self._VarIdentTexte = VarIdentTexte(self._gateway, 'en')
        self._AufzaehlTexte = AufzaehlTexte(self._gateway, 'en')

#        logger.debug(pprint(self._VarIdentTexte.VarIdentTexte))
        logger.debug("Gateway(hostname=%s) (name=%s) (serial_no=%s) (cache_duration=%d) instantiated.", self._hostname, self._name, self._serial_no, self._cacheDuration)

    def _getInstallation(self):
        subnets = self._getjson("http://" + self._hostname + ":" + self._port + apiURLPath )
        for subnet in subnets:
            nodes = self._getjson("http://" + self._hostname + ":" + self._port + apiURLPath + "/" + str(subnet))

            for node in nodes:
                try:
                    id = str(node['nodeId'])
                    if not 'functions' in node: # this is the gateway
                        self._name = node['name']
                        self._serial_no = node['programId']
                        self._id = id
                        logger.info("Gateway found : " + node['name'] + " (" + id + ")")
                    else:
                        fcttype = node['functions'][0]['fctType']

                        if fcttype == 9 or fcttype == 10:
                            logger.info("Boiler found : " + node['name'] + " (" + id + ")")
                            self._boilers.append(Boiler(node['name'], node['neuronId'], id, self._gateway))
                        elif fcttype == 14:
                            logger.info("Module found : " + node['name'] + " (" + id + ")")
                            self._modules.append(Module(node['name'], node['neuronId'], id, self._gateway))
                        else:
                            logger.info("Unknown device found : " + node['name'] + " (" + id + ")")

                    self._installation.append(node)
                except KeyError:
                    pass

    def _refreshCache(self):
        logger.debug("Refreshing cache...")

        self._lock.acquire()
        try:
            datapoints = self._getjson("http://" + self._hostname + ":" + self._port + apiURLFullCachePath)
            for datapoint in datapoints:
                if all (k in datapoint for k in ("OID", "value", "timestamp")):
                    self._cache[datapoint['OID']] = datapoint
        finally:
            self._lock.release()

    def _refreshAuth(self):
        logger.debug("Refreshing Digest Auth...")
        self._auth = HTTPDigestAuth(self._username, self._password)

    def _expiredDatapoint(self, oid, cacheDuration = 0):
        if oid in self._cache:
            _cacheDuration = cacheDuration if cacheDuration else self._cacheDuration
            # Home Assistant hasn't any timezone configured, datetime.now() is UTC...
            try:
                from homeassistant.util import dt
                now = dt.now().replace(tzinfo=None)
            except ImportError:
                now = datetime.now()
            oidDatetime = datetime.strptime(self._cache[oid]['timestamp'], '%Y-%m-%d %H:%M:%S')
            if (now - oidDatetime).seconds < _cacheDuration:
                return False

        return True

    def _getDatapoint(self, oid):
        datapoint = self._getjson("http://" + self._hostname + ":" + self._port + apiURLCachePath + oid)

        if datapoint:
            self._lock.acquire()
            try:
                if datapoint and all (k in datapoint for k in ("OID", "value", "timestamp")):
                    self._cache[datapoint['OID']] = datapoint
            finally:
                self._lock.release()

    def boilers(self):
        """Retrieve the boilers from the Gateway."""
        return self._boilers

    def modules(self):
        """Retrieve the modules from the Gateway."""
        return self._modules

    def datapoint(self, oid, cacheDuration = 0):
        if self._expiredDatapoint(oid, cacheDuration):
            self._getDatapoint(oid)

        try:
            return self._cache[oid]
        except:
            return None

    def value(self, oid, cacheDuration = 0):
        datapoint = self.datapoint(oid, cacheDuration)
        if (datapoint is None or oid == 'error'):
            return 'error'

        splittedOid = oid.split('/')
        # Oid "/1/xx/0/2/9/0 is not enum (Operation Mode)
        if 'enum' in datapoint or (splittedOid[4] == "2" and splittedOid[5] == "9"):
            return(self._AufzaehlTexte.getstr(splittedOid[4],splittedOid[5],datapoint['value']))

        return datapoint['value'] if 'value' in datapoint else 'error'

    def oid(self, description):
        id,subid = self._VarIdentTexte.getid(description)

        return id + "/" + subid if id and subid else 'error'

    def setValue(self, oid, value):
        data = {'OID': oid, 'value': value}
        return self._put("http://" + self._hostname + ":" + self._port + apiURLCachePath, data)

    @property
    def serial_no(self):
        """Return the serial_no of the gateway."""
        return self._serial_no
