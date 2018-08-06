#!/usr/bin/env python3

import sys
import os
import time
from datetime import datetime
import random	


source_path="/home/delkov/Documents/air/FTP/ftp_store"

os.chdir(source_path)


while True:

	txt_name=str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+'.txt'
	print(txt_name)
	file = open(txt_name,'w') 


	file.write('Date='+str(datetime.now().strftime('%d/%m/%Y'))+'\nTime='+str(datetime.now().strftime('%H:%M:%S'))+'\nRef=VNK001\nStatSLM_197517=-2\nStatSLM_---=0\nStatSLM_---=0\nLeq(A)='+str(random.randint(0,100))+'\nSlow(A)='+str(random.randint(0,100))+'\nSP(A)=0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;\nStatMet=-1\nTemp=---\nHum=---\nPres=---\nWind=---\nDir=---\nCoord=ÍÑ;ÍÑ\nStatCom=99\nTCore=49\nTMB=46\nTHDD=34\nFreeHDD=139.4\nStatUPS=99\nPowUPS=POW\nTimeUPS=393 min') 
	file.close()
	time.sleep(1)