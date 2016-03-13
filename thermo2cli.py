#!/usr/bin/env python

import argparse
import requests
import json
from time import time
from parser_constants import ParserConstants
from api import Thermo2Client

def get_args():
    parser = argparse.ArgumentParser(description='Thermo2 Client')
    parser.add_argument('-s','--set', nargs=1, help='name of event to inject')
    parser.add_argument('-g','--get', nargs=1, help='name of event to read')
    parser.add_argument('--host', nargs=1, help='hostname to connect to (defaults to 127.0.0.1)', default=['127.0.0.1'])
    parser.add_argument('-p','--port', nargs=1, help='port to connect to (defaults to 8822)', default=[8822])
    parser.add_argument('-t','--time', nargs=1, help='time to send with event (for -s only, defaults to time of invocation)', default=[time()])
    parser.add_argument('-v','--value', nargs=1, help='time to send with event (for -s only)')

    args = parser.parse_args()

    if args.set==None and args.get==None:
        raise Exception("Need either -s or -g")

    if args.set!=None and args.value==None:
        raise Exception("-s specified, but no -v")

    return args

if __name__ == '__main__':
    args = get_args()

    t2c = Thermo2Client(args.host[0], args.port[0])

    try:
        if args.set!=None:
            (label, value, t) = t2c.set_value(args.set[0], args.value[0], args.time[0])
        if args.get!=None:
            (label, value, t) = t2c.get_value(args.get[0])
    except requests.exceptions.ConnectionError as e:
        print "Unable to connect: "+str(e)

    print ("%s:%s:%s") % (label, value, t)
        
