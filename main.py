'''
@author: wardog
'''

import logging
import traceback
import time
from VErySimplePortAttackToolkit.torManager import TorManager
from VErySimplePortAttackToolkit.serviceScanner import ServiceScanner

if __name__ == '__main__':
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
    
    logger.info('Start app.')
    
    try :
               
        logger.debug('Start tor')
        torManager = TorManager('7000','ru') #choose exit node in russia
        torManager.connect() 
        
        logger.debug('Init scanner')
        serviceScan = ServiceScanner(23,3,300,'targets.csv')
        
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
        
        