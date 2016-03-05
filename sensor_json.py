from sensor import Sensor
import requests
import json
from sensor_event import SensorEvent
from time import time

class JsonSensor(Sensor):

    def getValue(self):
        try:
            response = requests.get(self.url)
        except requests.exceptions.ConnectionError as e:
            self.logger.error(str(e))
            return

        if response.status_code == 200:
            self.logger.debug(response.text)
            data = json.loads(response.text)
            if 'value' in data:
                self.value = data['value']

