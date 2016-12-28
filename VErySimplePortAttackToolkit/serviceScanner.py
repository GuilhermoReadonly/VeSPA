'''
@author: wardog
'''
import logging
import random
import traceback
import struct
import threading
import socks
import socket
import time

class ServiceScanner(object):

    port = 23
    portTor = 7000
    timeout = 1
    nbThread = 1
    targetsFile = 'targets.csv'
    

    _loopThread = []
    _stopLoop = False
    _lock = threading.Lock()
    
    _statNbTry = 0
    _statNbFind = 0
    _statStartTime = time.perf_counter()

    def __init__(self, port, timeout, nbThread, targetsFile):
        self.logger = logging.getLogger()
        self.port = port
        self.timeout = timeout
        self.nbThread = nbThread
        self.targetsFile = targetsFile

        
    def stopScan(self):
        self._stopLoop = True

    def startScan(self):
        self._stopLoop = False
        self.logger.info("Service scanner start with " + str(self.nbThread) + " threads and timeout = " + str(self.timeout))
        for i in range(0, self.nbThread):
            self._loopThread.append(threading.Thread(target = self._scanLoop)) 
            self._loopThread[i].start()
            self.logger.debug("Service scanner thread [" + self._loopThread[i].getName() + "] started")
        
            
    def _scanLoop(self):
        try:
            
            self.logger.debug("Start scan loop")
            
            
            
            self._stopLoop = False
            while not self._stopLoop:

                host = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

                self.logger.debug("Try " + host + ":" + str(self.port))
                
                
                socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", self.portTor, True)
                s = socks.socksocket()
                with s:
                    s.settimeout(self.timeout)
                    try:
                        self._statNbTry += 1
                        s.connect((host, self.port))
    
                        
                        f = open(self.targetsFile, 'a')
                        with self._lock,f:  
                            self._statNbFind += 1  
                            
                            deltaTime = time.perf_counter() - self._statStartTime               
                            self.logger.info("Find " + host + ":" + str(self.port) + " open !" )
                            self.logger.info("Stats : find " + str(self._statNbFind) + ' on ' + str(self._statNbTry) + ' tries in ' + str(deltaTime) + ' seconds. ')
                            self.logger.info("Stats : " + str(self._statNbFind/deltaTime) + ' finds/seconds. ' + str(self._statNbTry/deltaTime) + ' tries/seconds.')
                          
                            f.write(host+':'+ str(self.port) +'\n')
                            f.close()

                        
                    except BaseException as e:
                        self.logger.debug("Nothing here " + host + ":" + str(self.port) + ' ' + str(e))
        
        
        except BaseException as e:
            self.logger.error("Error occurs while scanning : " + str(e))
        finally:
            self.logger.debug("Exiting scan loop")      
            