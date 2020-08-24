from flask.views import MethodView
from flask import request
import subprocess
import re

path = 'hardware'
endpoint = 'hardware'

class HardwareInfo(MethodView):
    def get(self):
        """ Get hardware information
        ---
        description: Get information about the hardware
        tags:
          - Hardware
        responses:
          200:
            content:
              application/json:
                schema: 
                  type: array
                  items: String
        """
        with open("/proc/cpuinfo", "r") as stream:
            contents = stream.read()
        
        serial = re.search("^Serial.+?([0-9a-f]+)$", contents, re.M)
        processors = len(re.findall("^processor", contents, re.M))
        board = re.search("^Model.+?: (.+)$", contents, re.M)

        output = subprocess.check_output(['/opt/vc/bin/vcgencmd', 'measure_temp']).decode('utf-8')
        gputemp = re.match(r"temp=([0-9\.]+)'C", output)
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as stream:
            cputemp = int(stream.read()) / 1000
        hostname = subprocess.check_output(['/bin/hostname']).decode('utf-8').rstrip()

        return {
            "hostname": hostname,
            "serial": serial.group(1).lstrip("0"),
            "processors": processors,
            "board": board.group(1),
            "gpu_temp": float(gputemp.group(1)),
            "cpu_temp": cputemp,
            "warn_temp": 65,
            "max_temp": 80
        }