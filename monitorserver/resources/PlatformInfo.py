from flask.views import MethodView
from flask import request
import os

path = 'platform'
endpoint = 'platform'

class PlatformInfo(MethodView):
    def get(self):
        """ Get platform information
        ---
        description: Get information about the platform
        tags:
          - Platform
        responses:
          200:
            content:
              application/json:
                schema: 
                  type: array
                  items: String
        """
        if os.path.isfile("/boot/piplatform.txt"):
            with open("/boot/piplatform.txt", "r") as stream:
                platform = stream.read().rstrip()
        else:
            platform = "UNKNOWN"
        return {
            "platform": platform
        }