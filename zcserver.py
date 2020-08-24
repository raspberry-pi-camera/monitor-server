from zeroconf import ServiceInfo, Zeroconf
import socket
import time

desc = {'version': '0.1'}
print(socket.gethostbyname(socket.getfqdn()))

info = ServiceInfo(
    "_pimonitor._tcp.local.",
    "{}._pimonitor._tcp.local.".format(socket.gethostname().split('.')[0]),
    addresses=[socket.inet_aton(socket.gethostbyname(socket.getfqdn()))],
    port=80,
    properties=desc,
    server="{}.local.".format(socket.gethostname().split('.')[0]),
)

zeroconf = Zeroconf()
zeroconf.register_service(info)

try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    zeroconf.unregister_service(info)
    zeroconf.close()