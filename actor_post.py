from actor import Actor
import requests

class PostActor(Actor):
    def actOnValue(self, label, t, value):
        postData = {
            'label' : label,
            't'     : t,
            'value' : value,
        }
        requests.post(self.url, data=postData)

