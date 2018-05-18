#Config Utility for Checkpoint Security Checkups
#Install Gaia
#Insert USB, Set expert password, enter expert mode and run CPCheckupConfig.py


#Import Modules
import getpass
import subprocess
import time
import urllib2


#Methods
def test_connectivity():
	try:
		urllib2.urlopen("https://checkpoint.com:, timeout=1)
		return True
	except urllib2.URLError as err:
		return False

#Program Start

print " _____ ______   _____ _               _                  _____              __ _       "
print "/  __ \| ___ \ /  __ \ |             | |                /  __ \            / _(_)      "
print "| /  \/| |_/ / | /  \/ |__   ___  ___| | ___   _ _ __   | /  \/ ___  _ __ | |_ _  __ _ "
print "| |    |  __/  | |   | '_ \ / _ \/ __| |/ / | | | '_ \  | |    / _ \| '_ \|  _| |/ _` |"
print "| \__/\| |     | \__/\ | | |  __/ (__|   <| |_| | |_) | | \__/\ (_) | | | | | | | (_| |"
print " \____/\_|      \____/_| |_|\___|\___|_|\_\\__,_| .__/   \____/\___/|_| |_|_| |_|\__, |"
print "                                                | |                               __/ |"
print "                                                |_|                              |___/ "
print "Written by Mike Braun and Jordan Schraa \n\n"


#Get Variables
management_IP = raw_input("Enter desired Management IP: ")

print "Enter desired GAIA password"
password = getpass.getpass()

license_string = raw_input ("Enter License String (Optional): ")

client_IP = raw_input ("Enter desired Client IP(Optional): ")
if client_IP is "":
	client_interface = raw_input ("Enter desired Client Interface(Default is eth5): ")
	if client_interface is "":
		client_interface = "eth5"

dns_IP = raw_input ("Enter Desired DNS Server(Optional - Default is 8.8.8.8): ")
if dns_IP is "":
	dns_IP = "8.8.8.8"

#Set Default CLI to Bash
subprocess.Popen("chsh -s /bin/bash admin")

#Run First Time Config Wizard Tasks

#Gaia Setup
#Run Modify Script
subprocess.Popen("./modifyScript.sh")
time.sleep(5)

#Configure Interface
subprocess.Popen("clish")
subprocess.Popen("add dhcp client interface " + client_interface)
subprocess.Popen("set interface state on")

#Test Internet Connection
internet = False

if test_connectivity():
	internet = True
	continue
else:
	print "No Internet Connection. Skipping Updates and License Activation"

#Smart Console Setup
