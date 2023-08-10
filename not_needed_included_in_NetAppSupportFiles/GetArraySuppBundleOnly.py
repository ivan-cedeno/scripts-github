# $language = "Python"
# $interface = "1.0"

# Rev 10.00.00.04 corrected 7z extentiom
# Rev 10.00.00.03 corrected if no data enter on message box to exit
# Rev 10.00.00.02 corrected time stamp, is pulled now from customer system 02/19/2020 Luis Lopez
# Luis Lopez - 01/30/2020 ver. 10.00.00.01 @Teradata
# NetApp and DotHill Storage log files
# For NetApp Will download supportData,	 trace data, diagnosticData, and coredump if exists
# For DotHill will download debug logs
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GetArraySuppBundleOnly.py
import sys
import os
import SecureCRT
import time
import subprocess
import signal

other = "Start Over"
array1 = crt.Dialog.Prompt("Enter '1' for NetApp or '2' for Seagate Array:", "Teradata GSO HW Tools ", "1", False)
def main():

	if array1 == "": return
	if array1 == "1":
		commanda = crt.Dialog.Prompt("NetApp Array Name :", "Enter Array Name: ", "DAMC00X-XX", False)
		if commanda == "": return
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		objTab = crt.GetScriptTab()
		promptString = "#"
#		promptString = "#", ":"
		objTab.Screen.Send( " cd /var/opt/teradata" + '\r')
		crt.Screen.WaitForString(promptString)
		objTab.Screen.Send(" date +%m%d%y-%I%M%S%P \r")		 
		crt.Screen.WaitForString(promptString)
		screenrow = crt.Screen.CurrentRow - 1
		result = crt.Screen.Get(screenrow, 1, screenrow, 15)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~			
		cmda = " SMcli -n "
		q1 = '"'
		myrm = "rm "
		minus = "-"
		last = ";'"
		gtfile = " sz "
		dotz = ".7z"
		args = " -c 'save storageArray supportData file="
		file = (commanda + "-SupportBundle-" + result)
		objTab.Screen.Send( cmda + commanda + args + q1 +(file) + q1  + last + '\r')
		crt.Screen.WaitForString("#")
		objTab.Screen.Send( gtfile + file + '*' + '\r')
		crt.Screen.WaitForString("#")
#		crt.Screen.Send( myrm + file + dotz + '\r' )

	elif array1 == "2": 
		commandb = crt.Dialog.Prompt("Seagate Array Name :", "Enter Array Name: ", "DAMC00X-X-X", False)		
		if commandb == "": return
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		promptString = "#"
#		promptString = "#", ":"
		crt.Screen.Send( " cd /var/opt/teradata" + '\r')
		crt.Screen.WaitForString(promptString)
		crt.Screen.Send(" date +%m%d%y-%I%M%S%P \r")		 
		crt.Screen.WaitForString(promptString)
		screenrow = crt.Screen.CurrentRow - 1
		result = crt.Screen.Get(screenrow, 1, screenrow, 15)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~									
		crt.Screen.Send( "" + '\r')
		usern = "manage"
		pword = "!manage"
		cmdb = "ftp "
		szd = "sz "
		cdir = "cd /tmp"
		gbye = "by"
		xtype = ".zip"
		args = "get logs "
		gtfile = "sz "	
		filed = "Store-" + commandb + "_" + result + xtype
		crt.Screen.Send( cmdb + commandb + '\r')
		crt.Screen.WaitForString(":")
		crt.Screen.Send( usern + '\r')
		crt.Screen.WaitForString("OK.")
		crt.Screen.Send( pword + '\r')
		crt.Screen.WaitForString(">")
		crt.Screen.Send( args + filed + '\r')
		crt.Screen.WaitForString(">")
		crt.Screen.Send( gbye + '\r')
		crt.Screen.WaitForString("#")
		crt.Screen.Send( gtfile + filed + '\r')
		crt.Screen.WaitForString("#")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
main()
		