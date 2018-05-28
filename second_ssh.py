import getpass
import os
import subprocess
import sys
import paramiko
import time
import urllib2
from scp import SCPClient

                    

#Program Start

print " _____ ______   _____ _               _                 "
print "/  __ \| ___ \ /  __ \ |             | |                "
print "| /  \/| |_/ / | /  \/ |__   ___  ___| | ___   _ _ __   "
print "| |    |  __/  | |   | '_ \ / _ \/ __| |/ / | | | '_ \  "
print "| \__/\| |     | \__/\ | | |  __/ (__|   <| |_| | |_) | "
print " \____/\_|      \____/_| |_|\___|\___|_|\_\\__,_| .__/  "
print "                                                | |     "
print "                                                |_|     "
print "Written by Mike Braun and Jordan Schraa \n\n"

#Get Variables
ip_address = raw_input("Enter Management IP: ")

username = raw_input("Enter GAIA username: ")

print "Enter GAIA password"
password = getpass.getpass()

mfilepath = raw_input("Enter Modify Script Location(including filename): ")

client_interface = raw_input ("Enter desired Client Interface(Default is eth5): ")
if client_interface is "":
    client_interface = "eth5"

license_string = raw_input ("Enter License String (Do not include cplic put): ")

contract_location = raw_input("Enter full path to ServiceContract.xml (including filename): ")

#Establish SSH Connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect (ip_address, username=username, password=password)
rc = ssh.invoke_shell()
print "SSH session established with: " + ip_address 

#Set Expert Password
rc.send("lock database override")
rc.send("\n")
rc.send("set expert-password")
rc.send("\n")
result = rc.recv(1024)
rc.send("\n")
time.sleep(2)
rc.send(password)
rc.send("\n")
time.sleep(2)
rc.send(password)
rc.send("\n")
time.sleep(2)

#Change Default Shell
rc.send("expert")
rc.send("\n")
time.sleep(2)
rc.send(password)
rc.send("\n")
time.sleep(2)
rc.send("chsh -s /bin/bash")
rc.send("\n")
time.sleep(2)

#Upload Modify Script
scpclient = SCPClient(ssh.get_transport(), socket_timeout=15.0)
scpclient.put(mfilepath, "/home/admin")

#Run Modify Script
rc.send("chmod +x /home/admin/modifyScript.sh")
rc.send("/home/admin/modifyScript.sh")
time.sleep(5)

#Change Shell to CLISH
rc.send("clish")
rc.send("\n")
time.sleep(2)

#Configure Interface
rc.send("lock database override")
rc.send("\n")
rc.send('add dhcp client interface '+ client_interface)
rc.send("\n")
time.sleep(2)
rc.send('set interface ' + client_interface + ' state on')
time.sleep(15)
rc.send("\n")

'''
#Test Internet Connection
internet = False

if test_connectivity():
	internet = True
	continue
else:
	print "No Internet Connection. Updates and License Activation will fail an will have to be done manually"
	continue
'''

#Activate License
rc.send("lock database override")
rc.send("\n")
rc.send("cplic put '"+ license_string + "'")
rc.send("\n")


#Set to Expert for contract install
rc.send('expert')
rc.send('\n')
time.sleep(2)
rc.send(password)
rc.send("\n")
time.sleep(2)

#Upload Contract File
scpclient.put(contract_location, "/var/log")

#Activate Contract

rc.send("cplic contract put -o /var/log/servicecontract.xml") 
rc.send("\n")
time.sleep(2)
results = rc.recv(4000)
print results

'''

#Update Gaia. Download and update every hotfix available

for x in range (10):
	rc.send('installer download-and-install ' + str(x))
	time.sleep(5)
	rc.send('s')

#Smart Console Setup

#Login
rc.send("mgmt login")
time.sleep(2)
'''