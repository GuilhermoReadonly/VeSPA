'''
@author: wardog

^ ^
o O
\./

'''

import sys
import logging
import traceback
import random
import socket
import struct



#logging.basicConfig(filename='scan.log', format = "%(asctime)s %(levelname)s:%(name)s: %(message)s", level=logging.INFO) 


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(levelname)s:%(name)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

handler = logging.FileHandler("scan.log","a", encoding=None, delay="true")
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)

try:
	logger.info("Start app.")
	port = 23

	nbFind = 0
	while True:
		ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

		logger.debug("Try			" + ip + ":" + str(port))
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(0.5)
		result = sock.connect_ex((ip,port))

		if result == 0:
			logger.info("Find " + ip + ":" + str(port) + " open !!!")
			nbFind +=1
		else:
			logger.debug("Nothing here	" + ip + ":" + str(port))

		if nbFind > 1000:
			break


except BaseException as e:
	logger.error("Error occurs : " + traceback.format_exc())
finally:
	logger.info("Exit app.")
	sys.exit()

