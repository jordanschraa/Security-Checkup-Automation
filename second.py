#Run Modify Script
subprocess.Popen("./modifyScript.sh")
time.sleep(5)

#Configure Interface
subprocess.Popen('clish -c "add dhcp client interface '+ client_interface'"')
subprocess.Popen('clish -c "set interface state on"rebo)

#Test Internet Connection
internet = False

if test_connectivity():
	internet = True
	continue
else:
	print "No Internet Connection. Updates and License Activation will fail an will have to be done manually"
	continue

#Active License
subprocess.Popen("cplic put " + license_string)
#May have to have contract file downloaded and on usb. Then subprocess can be used to call file

#Update Gaia. Download and update every hotfix available
for x in range (10)
	subprocess.Popen("installer download-and-install " + x)
	time.sleep(5)
	subprocess.Popen("s")
#

#Smart Console Setup

#Login
subprocess.Popen("mgmt login")
time.sleep(2)