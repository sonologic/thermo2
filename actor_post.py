from actor import Actor
import requests
import logging

class PostActor(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.logger = logging.getLogger('thermo2.'+__name__)

    def actOnValue(self, label, t, value):
        postData = {
            'label' : label,
            't'     : t,
            'value' : value,
        }
        try:
            requests.post(self.url, data=postData)
        except requests.exceptions.ConnectionError as e:
            self.logger.error(e)

