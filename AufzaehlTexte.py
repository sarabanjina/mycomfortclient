import xml.etree.ElementTree as ET
import pickle
from pickle import UnpicklingError
import os
from collections import defaultdict
import logging

#from mycomfortclient.myComfortObject import myComfortObject
from .myComfortObject import myComfortObject

logger = logging.getLogger("mycomfortclient")

class AufzaehlTexte(myComfortObject):
    def __init__(self, gateway, language='en'):
        super().__init__()
        self.language = language
        self.AufzaehlTexte = defaultdict(dict)
        self.cache_file = "AufzaehlTexte_" + self.language + ".cache"
        self._gateway = gateway

        self._getAufzaehlTexte()

    def _getAufzaehlTexte(self):
        if os.path.isfile(self.cache_file):
            try:
                binary_file = open(self.cache_file,mode='rb')
                self.AufzaehlTexte = pickle.load(binary_file)
                logger.debug("AufzaehlTexte restored from cache file " + self.cache_file)
                return
            except UnpicklingError:
                logger.warning("Could not restore AufzaehlTexte")

        try:
            root = ET.fromstring(self._get('http://' + self._gateway._hostname + ':' + self._gateway._port + '/res/xml/AufzaehlTexte_' + self.language + '.xml'))
        except:
            logger.error("Exception getting AufzaehlTexte from server")
            return

        logger.debug("Parsing XML from AufzaehlTexte...")
        for gn in root.findall('gn'):
            for mn in gn.findall('mn'):
                for enum in mn.findall('enum'):
                    if mn.get('id') not in self.AufzaehlTexte[gn.get('id')]:
                        self.AufzaehlTexte[gn.get('id')][mn.get('id')] = {}
                    self.AufzaehlTexte[gn.get('id')][mn.get('id')][str(enum.get('id'))] = str(enum.text)

        binary_file = open(self.cache_file,mode='wb')
        pickle.dump(self.AufzaehlTexte,binary_file)
        binary_file.close()

    def getstr(self, id, subid, value):
        try:
            return  self.AufzaehlTexte[str(id)][str(subid)][str(value)]
        except KeyError:
            return "Unknown description"
