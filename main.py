'''
Created on 13 déc. 2016

@author: wardog
'''

import logging
import traceback
import time
from simpleTelnetScan.torManager import TorManager
from simpleTelnetScan.serviceScanner import ServiceScanner

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
        torManager = TorManager('7000','ru')
        torManager.connect() 
        
        logger.debug('Init scanner')
        serviceScan = ServiceScanner(23,3,1000)
        
        logger.debug('Start scanner')
        serviceScan.startScan()
        logger.debug('Scanner started')
        
    except:
        logging.getLogger().error("Error occurs : " + traceback.format_exc())
    
    finally:
        time.sleep(100)
        
        serviceScan.stopScan()
        
        time.sleep(1)
        torManager.disconnect()
        
        logger.info('Quit app.')
        
        
        
def getLoginPasswords():
    return [
        ("root","xc3511"),
        ("root","vizxv"),
        ("root","admin"),
        ("admin","admin"),
        ("root","888888"),
        ("root","xmhdipc"),
        ("root","default"),
        ("root","juantech"),
        ("root","123456"),
        ("root","54321"),
        ("support","support"),
        ("root",""),
        ("admin","password"),
        ("root","root"),
        ("root","12345"),
        ("user","user"),
        ("admin",""),
        ("root","pass"),
        ("admin","admin1234"),
        ("root","1111"),
        ("admin","smcadmin"),
        ("admin","1111"),
        ("root","666666"),
        ("root","password"),
        ("root","1234"),
        ("root","klv123"),
        ("Administrator","admin"),
        ("service","service"),
        ("supervisor","supervisor"),
        ("guest","guest"),
        ("guest","12345"),
        ("guest","12345"),
        ("admin1","password"),
        ("administrator","1234"),
        ("666666","666666"),
        ("888888","888888"),
        ("ubnt","ubnt"),
        ("root","klv1234"),
        ("root","Zte521"),
        ("root","hi3518"),
        ("root","jvbzd"),
        ("root","anko"),
        ("root","zlxx."),
        ("root","7ujMko0vizxv"),
        ("root","7ujMko0admin"),
        ("root","system"),
        ("root","ikwb"),
        ("root","dreambox"),
        ("root","user"),
        ("root","realtek"),
        ("root","00000000"),
        ("admin","1111111"),
        ("admin","1234"),
        ("admin","12345"),
        ("admin","54321"),
        ("admin","123456"),
        ("admin","7ujMko0admin"),
        ("admin","1234"),
        ("admin","pass"),
        ("admin","meinsm"),
        ("tech","tech"),
        ("mother","fucker")]