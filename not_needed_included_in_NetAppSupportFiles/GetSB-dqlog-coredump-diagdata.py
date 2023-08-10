# $language = "Python"
# $interface = "1.0"


# Rev 10.00.00.04 corrected 7z extentiom
# Rev 10.00.00.03 corrected if no data enter on message box to exit
# Rev 10.00.00.02 corrected time stamp, is pulled now from customer system 02/19/2020 Luis Lopez
# Luis Lopez - 01/30/2020 ver. 10.00.00.01 @Teradata
# NetApp and DotHill Storage log files
# For NetApp Will download supportData,	 trace data, diagnosticData, and coredump if exists
# 
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GetSB-dqlog-coredump-diagdata.py
import sys
import os
import SecureCRT
import time
import subprocess
import signal

other = "Start Over"
def main():
		commanda = crt.Dialog.Prompt("NetApp Array Name :", "Enter Array Name: ", "DAMC00X-X-X", False)
		if commanda == "": return
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		promptString = "#"
#		promptString = "#", ":"
		crt.Screen.Send( " cd /var/opt/teradata" + '\r')
		crt.Screen.WaitForString(promptString)
		crt.Screen.Send(" date +%m%d%y-%I%M%S%P \r")
		crt.Screen.WaitForString(promptString)
		screenrow = crt.Screen.CurrentRow - 1
		result = crt.Screen.Get(screenrow, 1, screenrow, 11)
		resulta = crt.Screen.Get(screenrow, 1, screenrow, 15)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		   
		q1 = '"'
		myrm = "rm "
		last = ";'"
		gtfile = " sz "
		dotz = ".7z"
		args = " -c 'save storageArray supportData file="
		file = (commanda + "-SupportBundle-" + resulta)
		crt.Screen.Send( " SMcli -n " + commanda + args + q1 +(file) + q1  + last + '\r')
		crt.Screen.WaitForString("#")
		crt.Screen.Send( gtfile + file + '*' + '\r')
		crt.Screen.WaitForString("#")
#		crt.Screen.Send( myrm + file + dotz + '\r' )
#		crt.Screen.WaitForString("#")
#
		argsa = " -c 'start controller [both] trace dataType=all forceFlush=true file="
		filea = commanda + "-dqlog-" + resulta
		crt.Screen.Send( " SMcli -n " + commanda + argsa + q1 +(filea) + q1	 + last + '\r')
		crt.Screen.WaitForString("#")
		crt.Screen.Send( gtfile + filea + '*' + '\r')
		crt.Screen.WaitForString("#")
#		crt.Screen.Send( myrm + filea + dotz + '\r' )
#		crt.Screen.WaitForString("#")
#
		argsb = " -c 'save storageArray controllerHealthImage file="
		fileb = "Coredump-" + result
		crt.Screen.Send( " SMcli -n " + commanda + argsb + q1 +(fileb + '.zip') + q1	 + last + '\r')
		crt.Screen.WaitForString("#")
		crt.Screen.Send( gtfile + fileb + '*' + '\r')
		crt.Screen.WaitForString("#")
#		crt.Screen.Send( myrm + fileb + dotz + '\r' )
#		crt.Screen.WaitForString("#")		
#
		argsc = " -c 'save storageArray diagnosticData file="
		filec = commanda + "-DDC-" + resulta
		crt.Screen.Send( " SMcli -n " + commanda + argsc + q1 +(filec + '.zip') + q1	 + last + '\r')
		crt.Screen.WaitForString("#")
		crt.Screen.Send( gtfile + filec + '*' + '\r') 
		crt.Screen.WaitForString("#")
#		crt.Screen.Send( myrm + filec + dotz + '\r' )
#		crt.Screen.WaitForString("#")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
main()
		