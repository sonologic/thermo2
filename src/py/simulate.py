#!/usr/bin/env python

import argparse
import requests
import json
from time import time
from time import sleep
from parser_constants import ParserConstants
from api import Thermo2Client

def get_args():
    parser = argparse.ArgumentParser(description='Thermo2 Client')
    parser.add_argument('--host', nargs=1, help='hostname to connect to (defaults to 127.0.0.1)', default=['127.0.0.1'])
    parser.add_argument('-p','--port', nargs=1, help='port to connect to (defaults to 8822)', default=[8822])

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = get_args()

    t2c = Thermo2Client(args.host[0], args.port[0])

    while True:
        burn = None
        temp1 = None
        try:
            (label, burn, t) = t2c.get_value('burn')
            (label, temp1, t) = t2c.get_value('temp1')
        except requests.exceptions.ConnectionError as e:
            print "Unable to connect: "+str(e)

        print "temp1="+str(temp1)+", burn="+str(burn)

        if temp1==None:
            temp1 = 20.25
        else:
            if burn==100:
                temp1 += 0.125/2
            else:
                temp1 -= 0.125/2
        
        try:
            t2c.set_value('temp1', temp1)
        except requests.exceptions.ConnectionError as e:
            print "Unable to connect: "+str(e)

        sleep(3)
            
        
