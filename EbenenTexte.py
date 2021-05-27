import requests
import xml.etree.ElementTree as ET
import pickle
from pickle import UnpicklingError
import os
from collections import defaultdict
import logging

logger = logging.getLogger('mycomfortclient')

class EbenenTexte:
    def __init__(self, gateway, language='en'):
        super().__init__()
        self.language = language
        self.EbenenTexte = defaultdict(dict)
        self.cache_file = "EbenenTexte_" + self.language + ".pickle"
        self._gateway = gateway

        self._getEbenenTexte()

    def _getEbenenTexte(self):
        if os.path.isfile(self.cache_file):
            try:
                binary_file = open(self.cache_file,mode='rb')
                self.EbenenTexte = pickle.load(binary_file)
                logger.debug("EbenenTexte restored from cache file " + self.cache_file)
                return
            except UnpicklingError:
                logger.warning("Could not restore EbenenTexte")

        try:
            root = ET.fromstring(self._get('http://' + self._gateway._hostname + ':' + self._gateway._port + '/res/xml/EbenenTexte_' + self.language + '.xml'))
        except:
            logger.error("Exception getting AufzaehlTexte from server")
            return

        for fcttyp in root.findall('fcttyp'):
            for ebene in fcttyp.findall('ebene'):
                self.EbenenTexte[fcttyp.get('id')][ebene.get('id')] = str(ebene.text)

        binary_file = open(self.cache_file,mode='wb')
        pickle.dump(self.EbenenTexte,binary_file)
        binary_file.close()

    def get(self, id, subid):
        try:
            return  self.EbenenTexte[str(id)][str(subid)]
        except KeyError:
            return 'Unknown level'
