import requests
import xml.etree.ElementTree as ET
import pickle
from pickle import UnpicklingError
import os
from collections import defaultdict
import logging

#from mycomfortclient.myComfortObject import myComfortObject
from .myComfortObject import myComfortObject

logger = logging.getLogger("mycomfortclient")

class VarIdentTexte(myComfortObject):
    def __init__(self, gateway, language='en'):
        super().__init__()
        self.language = language
        self.VarIdentTexte = {}
        self.VarIdentTexte['id'] = defaultdict(dict)
        self.VarIdentTexte['text'] = defaultdict(dict)
        self.cache_file = "VarIdentTexte_" + self.language + ".cache"
        self._gateway = gateway
        self._getVarIdentTexte()

    def _getVarIdentTexte(self):
        if os.path.isfile(self.cache_file):
            try:
                binary_file = open(self.cache_file,mode='rb')
                self.VarIdentTexte = pickle.load(binary_file)
                logger.debug("VarIdentTexte restored from cache file " + self.cache_file)
                return
            except UnpicklingError:
                logger.warning("Could not restore VarIdentTexte")

        try:
            root = ET.fromstring(self._get('http://' + self._gateway._hostname + ':' + self._gateway._port + '/res/xml/VarIdentTexte_' + self.language + '.xml'))
        except:
            logger.error("Exception getting VarIdentTexte from server")
            return

        logger.debug("Parsing XML from VarIdentTexte...")
        for gn in root.findall('gn'):
            for mn in gn.findall('mn'):
                self.VarIdentTexte['id'][gn.get('id')][mn.get('id')] = str(mn.text)
                if not str(mn.text) in self.VarIdentTexte['text']:
                    self.VarIdentTexte['text'][str(mn.text)] = (gn.get('id'), mn.get('id'))

        # Missing Operating mode in English and French (Betriebsphasen in German)
        self.VarIdentTexte['id']['2']['1'] = "Operating mode"
        self.VarIdentTexte['text']['Operating mode'] = ('2','1')
        # Missing Outside temperature in English and French (Aussentemperatur in German)
        self.VarIdentTexte['id']['0']['0'] = "Outside temperature"
        self.VarIdentTexte['text']['Outside temperature'] = ('0','0')

        binary_file = open(self.cache_file,mode='wb')
        pickle.dump(self.VarIdentTexte,binary_file)
        binary_file.close()

    def getstr(self, id, subid):
        try:
            return  self.VarIdentTexte['id'][str(id)][str(subid)]
        except KeyError:
            return 'Unknown description'

    def getid(self, description):
        if description in self.VarIdentTexte['text']:
            return self.VarIdentTexte['text'][description]
        else:
            return None
