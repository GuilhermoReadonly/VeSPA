'''
@author: wardog
'''
import logging
import stem.process

import traceback

class TorManager(object):

    port = '7000'
    exitNode = 'ru'
    torProcess = None

    def __init__(self, port,exitNode):
        self.port = port
        self.exitNode = exitNode
        logging.getLogger().debug("Init Tor with port=" + self.port + " exitNode=" + str(self.exitNode))
        
    def connect(self):
        logging.getLogger().debug("Starting Tor")

        configTor = {
        'SocksPort': self.port
        }
        
        if(self.exitNode != None):
            configTor['ExitNodes'] = '{' + self.exitNode + '}'
        
        try:
            self.torProcess = stem.process.launch_tor_with_config(config = configTor,init_msg_handler = self.print_bootstrap_lines)

            
        except BaseException as e:
            logging.getLogger().error("Error occurs : " + traceback.format_exc())
            self.disconnect()
        


    def disconnect(self):
        if self.torProcess != None:
            logging.getLogger().debug("Stoping Tor")
            self.torProcess.terminate()    
        
    def print_bootstrap_lines(self,line):
        logging.getLogger().debug(line)
        

