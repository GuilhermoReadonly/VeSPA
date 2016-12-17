'''
@author: wardog
'''
import logging
import math
import traceback
import struct
import threading
import socks
import socket
import time

class TelnetDictionaryAttack(object):

    dictionary = []
    listTargets = []
    nbThread = 1
    
    _loopThread = []
    _stopLoop = False
    
    _statNbTry = 0
    _statNbFind = 0
    _statStartTime = time.perf_counter()
    
    
    def __init__(self, dictionary, listTargets, nbThread):
        self.logger = logging.getLogger()
        self.dictionary = dictionary
        self.listTargets = listTargets
        self.nbThread = nbThread

    def stopAttack(self):
        self._stopLoop = True

    def startAttack(self):
        self._stopLoop = False
        self.logger.info("Service scanner start with " + str(self.nbThread) + " threads and " + str(len(self.listTargets)) + " targets")
        
        ceilNbTargetsPerThread = math.ceil(len(self.listTargets)/self.nbThread)         
        for i in range(0, self.nbThread):
            subTargetsList = self.listTargets[i * ceilNbTargetsPerThread :(i+1) * ceilNbTargetsPerThread]
            self._loopThread.append(threading.Thread(target = self._attackLoop, args=([subTargetsList]))) 
            self._loopThread[i].start()
            self.logger.debug("Telnet attack thread [" + self._loopThread[i].getName() + "] started")
            
    def _attackLoop(self,subTargetsList):

            
        self.logger.debug("Start attack loop")
        
        self._stopLoop = False
        
        for i in range(0, len(subTargetsList)):

            self.logger.debug("target : " + str(subTargetsList[i]))
            
            time.sleep(1)
            
            if(self._stopLoop):
                break
                
                
                    
                    