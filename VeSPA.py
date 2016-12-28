'''
@author: wardog
'''

import logging
import traceback
import time
import argparse
from VErySimplePortAttackToolkit.torManager import TorManager
from VErySimplePortAttackToolkit.serviceScanner import ServiceScanner

if __name__ == '__main__':
    
    
    parser = argparse.ArgumentParser(description="VeSPA : the VEry Simple Port Attack tool.")
    parser.add_argument("-d", "--dictionary-file")
    parser.add_argument("-p","--port", type=int, help='tcp port number to scan')
    parser.add_argument("-en","--exit-node")
    parser.add_argument("-ts","--threads-scanner", type=int, help='number of threads for port scanner. Default is 1.')

  
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
    
    try :
               
        logger.debug('Start tor')
        torManager = TorManager('7000',args.exit_node) #choose exit node in russia
        torManager.connect() 
        
        logger.debug('Init scanner')
        serviceScan = ServiceScanner(args.port,3,args.threads_scanner,'targets.csv')
        
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
        
        logger.info('Quit app.')
        
        