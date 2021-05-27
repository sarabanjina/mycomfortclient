import requests
import xml.etree.ElementTree as ET
import pickle
from pickle import UnpicklingError
import os
import logging

logger = logging.getLogger('mycomfortclient')

class ErrorTexte:
    def __init__(self, gateway, language='en'):
        super().__init__()
        self.host = host
        self.language = language
        self.ErrorTexte = {}
        self.cache_file = "ErrorTexte_" + self.language + ".pickle"
        self._gateway = gateway

        self._getErrorTexte()

    def _getErrorTexte(self):
        if os.path.isfile(self.cache_file):
            try:
                binary_file = open(self.cache_file,mode='rb')
                self.ErrorTexte = pickle.load(binary_file)
                logger.info("ErrorTexte restored from cache file " + self.cache_file)
                return
            except UnpicklingError:
                logger.warning("Could not restore ErrorTexte")

        try:
            root = ET.fromstring(self._get('http://' + self._gateway._hostname + ':' + self._gateway._port + '/res/xml/ErrorTexte_' + self.language + '.xml'))
        except:
            logger.error("Exception getting ErrorTexte from server")
            return

        root = ET.fromstring(r.text)

        for error in root.findall('error'):
            self.ErrorTexte[error.get('code')] = error.get('text')

        binary_file = open(self.cache_file,mode='wb')
        pickle.dump(self.ErrorTexte,binary_file)
        binary_file.close()

    def get(self, id):
        return  self.ErrorTexte.get(str(id), 'Unknown error')
