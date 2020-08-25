#!/usr/bin/env python3

from flask import Flask, render_template
from os import getenv
from importlib import import_module
from flask_restful import abort, Api, Resource
from zeroconf import ServiceInfo, Zeroconf
import socket
import time


app = Flask(__name__)

api_prefix = '/v1'

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def gen_url(url):
    return "{}/{}".format(api_prefix, url)

api = Api(app)

from monitorserver.resources import submodules as resources


for resource in resources:
    res = import_module("monitorserver.resources.{}".format(resource))
    api.add_resource(getattr(res, resource), gen_url(res.path), endpoint=res.endpoint)

if __name__ == '__main__':
    
    desc = {'version': '0.1'}


    info = ServiceInfo(
        "_pimonitor._tcp.local.",
        "{}._pimonitor._tcp.local.".format(socket.gethostname().split('.')[0]),
        addresses=[socket.inet_pton(socket.AF_INET, get_ip())],
        port=5000,
        properties=desc,
        server="{}.local.".format(socket.gethostname().split('.')[0]),
    )

    zeroconf = Zeroconf()
    zeroconf.register_service(info)

    try:
        app.run(debug=True, host="0.0.0.0")
    finally:
        zeroconf.unregister_service(info)
        zeroconf.close()
