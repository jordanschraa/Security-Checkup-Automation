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
rc.send("\n")
time.sleep(2)
rc.send(password)
rc.send("\n")
time.sleep(2)
rc.send(password)
rc.send("\n")
time.sleep(7)

#Change Default Shell
rc.send("expert")
rc.send("\n")
time.sleep(2)
rc.send(password)
rc.send("\n")
time.sleep(2)
rc.send("chsh -s /bin/bash")
rc.send("\n")
time.sleep(5)

#Upload Modify Script
rc.send("expert")
rc.send("\n")
time.sleep(2)
rc.send(password)
rc.send("\n")
time.sleep(2)
ssh.close()
time.sleep(1)
ssh.connect (ip_address, username=username, password=password)
scpclient = SCPClient(ssh.get_transport(), socket_timeout=15.0)
scpclient.put(mfilepath, "/home/admin")
rc = ssh.invoke_shell()

#Run Modify Script
rc.send("chmod 777 /home/admin/modifyScript.sh")
rc.send("\n")
rc.send("/home/admin/modifyScript.sh")
rc.send("\n")
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
'''


#Smart Console Setup

#Login
rc.send("mgmt login user " + username)
rc.send("\n")
time.sleep(1)
rc.send(password)
time.sleep(1)

#Create Rules
rc.send("clish")
rc.send("\n")
rc.send("lock database override")
rc.send("\n")
rc.send('mgmt_cli add package name "security_checkup" threat-prevention "false"')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli add access-layer name "FW_Layer"  firewall "true" add-default-rule "false" shared "true"')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli set package name "security_checkup" access-layers.add.1.name "FW_Layer" access-layers.add.1.position 1')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli add access-rule layer "FW_Layer" source "any" destination "any" service "any" action "accept" position "1" name "Accept All"')
rc.send("\n")
time.sleep(2)


#Publish Rules
rc.send('mgmt_cli publish')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli install-policy policy-package "security_checkup"')
rc.send("\n")
time.sleep(200)

#Reboot
rc.send('expert')
rc.send('\n')
time.sleep(2)
rc.send(password)
rc.send("\n")
time.sleep(2)
rc.send('reboot')
rc.send('\n')
rc.send('y')
rc.send('\n')