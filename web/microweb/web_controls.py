#!/usr/bin/python

#
# Licensed under the BSD license.  See full license in LICENSE file.
# http://www.lightshowpi.org/
#
# Author: Ken B

import BaseHTTPServer
import CGIHTTPServer_root
import cgitb; cgitb.enable()  ## This line enables CGI error reporting
import os, sys
import logging
import threading

logger = logging.getLogger("root")
broadlink = os.getenv("BROADLINK")
sys.path.append(broadlink)

server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer_root.CGIHTTPRequestHandler
server_address = ("", 80)
lspitools = os.getenv("SYNCHRONIZED_LIGHTS_HOME") + "/web/microweb"
os.chdir(lspitools)
handler.cgi_directories = ["/cgi-bin"]

##
import relay, socket
logger.info("Starting relay...")

try:
    destination_address = "192.168.187.103"
    destination_port = 32001
    with socket.socket() as s:
        is_remote = s.connect_ex((destination_address, destination_port))
except Exception as e:
    logger.error(str(e))
    is_remote=True
finally:
    if is_remote:
        destination_address = "fife.entrydns.org"
        destination_port = 57325

relay = threading.Thread(target=relay.TheServer,
                          kwargs={"local_host":"",
                                  "local_port":39554,
                                  "destination_address":destination_address,
                                  "destination_port":destination_port,
                                  "autostart":True},
                          ).start()


try: 
    httpd = server(server_address, handler)
    httpd.serve_forever()

except KeyboardInterrupt:
    os.system('pkill -f "bash $SYNCHRONIZED_LIGHTS_HOME/bin"')
    os.system('pkill -f "python $SYNCHRONIZED_LIGHTS_HOME/py"')


