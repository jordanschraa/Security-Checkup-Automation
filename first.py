#Config Utility for Checkpoint Security Checkups
#Install Gaia
#Insert USB, Set expert password, enter expert mode and run CPCheckupConfig.py. Include COntract File

#Import Modules
import getpass
import subprocess
import time
import urllib2

#Methods
'''
def test_connectivity():
	try:
		urllib2.urlopen("https://checkpoint.com":, timeout=1)
		return True
	except urllib2.URLError as err:
		return False
'''
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
management_IP = raw_input("Enter desired Management IP: ")

print "Enter desired GAIA password"
password = getpass.getpass()

license_string = raw_input ("Enter License String (Do not include cplic put): ")

client_IP = raw_input ("Enter desired Client IP(Optional): ")
if client_IP is "":
	client_interface = raw_input ("Enter desired Client Interface(Default is eth5): ")
	if client_interface is "":
		client_interface = "eth5"

dns_IP = raw_input ("Enter Desired DNS Server(Optional - Default is 8.8.8.8): ")
if dns_IP is "":
	dns_IP = "8.8.8.8"

#Set Default CLI to Bash
#subprocess.Popen("chsh -s /bin/bash admin")
						
f = open('first_time_wizard.txt', "w+")
f.write('hostname=security_checkup \n')
f.write('mgmt_admin_name=admin \n')
f.write('mgmt_admin_passwd='+password+' \n')
f.write('mgmt_gui_clients_radio=any \n')
f.write('install_security_managment="true" \n')
f.write('install_security_gw="true" \n')
f.write('install_mgmt_primary="true" \n')
f.write('install_mgmt_secondary="false" \n')
f.write('download_info="true" \n')
f.write('upload_info="true" \n')
f.close()

#cronjob to have next python file run on system-startup

def subprocess_cmd(command):
	process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	proc_stdout = process.communicate()[0].strip()
	p_status = process.wait()
	print proc_stdout
cmd1 =""" "add cron job pythonrestart command '$FWDIR/Python/bin/python /mnt/usb-storage/second.py' recurrence system-startup" """
cmd2 =""" "config_system -f ./first_time_wizard.txt" """ 
subprocess_cmd("clish -c " + cmd1 + "; clish -c" + cmd2)
