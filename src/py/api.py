#!/usr/bin/env python

import requests
import json
from time import time

class Thermo2Client(object):
    def __init__(self, host='127.0.0.1', port=8822):
        self.host = host
        self.port = port
        self.url = 'http://'+host+':'+str(port)

    def set_value(self,label,value,t=time()):
        post_data = {
            't' : t,
            'value' : value
        }
        response=requests.post(self.url+'/set/'+label, post_data)

        if response.status_code==200:
            data = json.loads(response.text)
            if not 'label' in data.keys():
                raise Exception("label not in return data")
            if not 'value' in data.keys() or not 't' in data.keys():
                return (data['label'], None, None)
            else:
                return (data['label'], data['value'], data['t'])

    def get_value(self,label):
        response=requests.get(self.url+'/get/'+label)

        if response.status_code==200:
            data = json.loads(response.text)
            if not 'label' in data.keys():
                raise Exception("label not in return data")
            if not 'value' in data.keys() or not 't' in data.keys():
                return (data['label'], None, None)
            else:
                return (data['label'], data['value'], data['t'])

