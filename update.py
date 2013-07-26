#!/usr/bin/python
# This script is designed to run on a host and populate the mac address and hostname.
# It needs to be run as root. 
import sys
import db
import os
import myExceptions
import inventory
from socket import gethostname



inv = inventory.Inventory() 

myMac = os.popen("ifconfig | grep -B 1 inet | grep eth | grep -o ..:..:..:..:..:..").read().strip()
#Need to be root to do this, but it works. (Service tag) 
myST = os.popen("dmidecode -s system-serial-number").read().strip()
myHostName = gethostname() 

print myHostName

with inv: 
    idtag = inv.getID(myST)
    
    dbValues = inv.get(idtag)
    dbValues['hostname'] = myHostName
    dbValues['mac_address'] = myMac
    
    inv.edit(idtag, dbValues)
    
    

