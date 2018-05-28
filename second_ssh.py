import getpass
import pysftp
import subprocess
import sys
import paramiko
import time
import urllib2


#Methods
def test_connectivity():
	try:
		urllib2.urlopen("https://checkpoint.com:, timeout=1)
		return True
	except urllib2.URLError as err:
		return False
                        
#Method for running commands
def subprocess_cmd(command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        proc_stdout = process.communicate()[0].strip()
        p_status = process.wait()
        print proc_stdout


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
ip_address = raw_input("Enter desired Management IP: ")

username = raw_input("Enter GAIA username")

print "Enter GAIA password"
password = getpass.getpass()

license_string = raw_input ("Enter License String (Do not include cplic put): ")
                            
script_location = raw_input("Enter full path to modifyScript.sh")

contract_location = raw_input("Enter full path to contract (including filename)")

#SFTP Connection
srv = pysftp.Connection(host=ip_address, username=username,
password=your_password)
#Upload
srv.put(script_location)

#Establish SSH Connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect (ip_address, username=username, password=password)
rc = ssh.invoke_shell()
print "SSH session established with: " + ip_address                                                       

#Set Expert Password
rc.send("\n")
rc.send("set expert-password)
rc.send("\n")
time.sleep(2)
rc.send(password)
rc.send("\n")
time.sleep(2)
rc.send(password)
rc.send("\n")
time.sleep(2)

'''
#Run Modify Script
subprocess.Popen("./modifyScript.sh")
time.sleep(5)

#Configure Interface
subprocess_cmd('clish -c "add dhcp client interface '+ client_interface'"')
subprocess_cmd('clish -c "set interface state on"')

#Test Internet Connection
internet = False

if test_connectivity():
	internet = True
	continue
else:
	print "No Internet Connection. Updates and License Activation will fail an will have to be done manually"
	continue

#Active License
subprocess_cmd('clish -c "cplic put '+ license_string '"')

#May have to have contract file downloaded and on usb. Then subprocess can be used to call file

#Update Gaia. Download and update every hotfix available
for x in range (10)
	subprocess_cmd('clish -c "installer download-and-install ' + x'"')
	time.sleep(5)
	subprocess.Popen("s")
#

#Smart Console Setup

#Login
subprocess_cmd("mgmt login")
time.sleep(2)
'''