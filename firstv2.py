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


#create string for config_system

config_string = """ "hostname=security_checkup&ipaddr_v4="+management_IP+"&masklen_v4=24&primary="+dns_IP+"&mgmt_admin_passwd="+password+"&timezone='America/Edmonton'&install_security_gw=true&gateway_daip=false&install_ppak=true&install_security_management=true&gateway_cluster_member=false&install_security_managment=true&mgmt_admin_name=adminIP&mgmt_gui_clients_radio=any" """


#cronjob to have next python file run on system-startup
cmd1 =""" "add cron job pythonrestart command '$FWDIR/Python/bin/python /mnt/usb-storage/second.py' recurrence system-startup" """

#config wizard
cmd2 =""" "config_system -s """ + config_string + """ " """

#run commands
subprocess_cmd("clish -c " + cmd1) 
subprocess_cmd(cmd2)
