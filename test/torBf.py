'''
@author: wardog

^ ^
o O
\./

'''

import io
import stem.process
import socket
import socks
import telnetlib
from simpleTelnetScan.torManager import TorManager
import threading

from stem.util import term

port_tor = 7000
port = 1818
host = 'guilhem.radonde.net'




"""configTor = {
'SocksPort': str(port_tor),
'ExitNodes': '{ru}',
}

tor_process = stem.process.launch_tor_with_config(config = configTor,init_msg_handler = print_bootstrap_lines,)
"""



def threadTelnet():
    print("Starting telnet:\n")
    tn = telnetlib.Telnet(host,port=port)
    tn.read_until(b"\n")
    print("Stop telnet:\n")
    torManager.disconnect()


try:
    print("Starting Tor:\n")
    torManager = TorManager('7000','fr')
    torManager.connect()
    
    print("\nChecking our endpoint:\n")
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", port_tor, True)
    socket.socket = socks.socksocket  

    #threadTelnet()
    _loopThread = threading.Thread(target = threadTelnet)
    _loopThread.start()
    

finally:
    #tor_process.kill()  # stops tor
    #torManager.disconnect()
    print("Finish")




