from flask.views import MethodView
from flask import request
import subprocess
import re
import semantic_version
import os

path = 'software'
endpoint = 'software'

class SoftwareInfo(MethodView):
    def get(self):
        """ Get software information
        ---
        description: Get information about the software
        tags:
          - Software
        responses:
          200:
            content:
              application/json:
                schema: 
                  type: array
                  items: String
        """

        env = os.environ
        env['LD_LIBRARY_PATH'] = "/opt/raspindi/usr/lib"

        atemraw = subprocess.check_output(['/opt/raspindi/bin/atem', '-v']).decode('utf-8').rstrip()
        cameraraw = subprocess.check_output(['/opt/raspindi/bin/camera', '-v']).decode('utf-8').rstrip()
        neopixelraw = subprocess.check_output(['/opt/raspindi/bin/neopixel', '-v']).decode('utf-8').rstrip()
        raspindiraw = subprocess.check_output(['/opt/raspindi/bin/raspindi', '-v'], env=env).decode('utf-8').rstrip()

        atem = semantic_version.Version.coerce(atemraw)
        camera = semantic_version.Version.coerce(cameraraw)
        neopixel = semantic_version.Version.coerce(neopixelraw)
        raspindi = semantic_version.Version.coerce(raspindiraw)

        return {
            "atem": str(atem),
            "camera": str(camera),
            "neopixel": str(neopixel),
            "raspindi": str(raspindi)
        }