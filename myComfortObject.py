import requests
from requests.auth import HTTPDigestAuth
import json
import logging

logger = logging.getLogger("mycomfortclient")

class myComfortObject:
    """Base for myComfortObjects."""

    def __init__(self):
        self._gateway: Gateway = None
        self._serial_no = None

    def _get(self,url):
        try:
            logger.debug("Retrieving url " + url)
            r = requests.get(url, auth=self._gateway._auth,timeout=5)
            if r.status_code == 401:
                logger.warning("Authentication error (401) while retrieving " + url)
                self._gateway._refreshAuth()
                r = requests.get(url, auth=self._gateway._auth)

        except requests.exceptions.HTTPError as e:
            logger.warning("Error while retrieving " + url + " : " + str(e))
            return
        except requests.exceptions.Timeout:
            logger.warning("Timeout waiting for answer from " + url)
            return
        except requests.exceptions.RequestException as e:
            logger.error("Error while retrieving " + url + " : " + str(e))
            self._gateway._refreshAuth()
            return

        return r.text


    def _getjson(self,url):
        response = self._get(url)
        return json.loads(response) if response else None

    def _put(self,url, data):
        try:
            logger.debug("Putting url " + url + " with oid " + data['OID'] + " and value " + data['value'])
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.put(url, data=json.dumps(data), auth=self._gateway._auth, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.warning("Error while putting " + url + " : " + str(e))
            return False
        except requests.exceptions.Timeout:
            logger.warning("Timeout waiting for answer from " + url)
            return False
        except requests.exceptions.RequestException as e:
            logger.error("Error while putting " + url + " : " + str(e))
            self._gateway._refreshAuth()
            return False

        return True

