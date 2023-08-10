# $language = "python"
# $interface = "1.0"

# Integration Luis Lopez - 01/11/2023 ver. 01 @Teradata
# sreen capture ArrayHealthStatus (SMcli –n DAMC1XX-X –c “show storageArray healthStatus;” )

import os, sys, platform, re
import codecs
import os
import subprocess
import time

def Main():
	LOG_DIRECTORY = os.path.join(
		os.path.expanduser('~\Downloads'), 'NetAppArray-Status-Information')
	LOG_FILE_TEMPLATE = os.path.join(
		LOG_DIRECTORY, "Array Status information-")
	SCRIPT_TAB = crt.GetScriptTab()
	if not os.path.exists(LOG_DIRECTORY):
		os.mkdir(LOG_DIRECTORY)

	if not os.path.isdir(LOG_DIRECTORY):
		crt.Dialog.MessageBox(
			"Log output directory %r is not a directory" % LOG_DIRECTORY)
		return
	SCRIPT_TAB.Screen.IgnoreEscape = True
	SCRIPT_TAB.Screen.Synchronous = True
	while True:
		if not SCRIPT_TAB.Screen.WaitForCursor(1):
			break
	rowIndex = SCRIPT_TAB.Screen.CurrentRow
	colIndex = SCRIPT_TAB.Screen.CurrentColumn - 1
	prompt = SCRIPT_TAB.Screen.Get(rowIndex, 1, rowIndex, colIndex)
	prompt = prompt.replace("\n","")
	timestr = time.strftime("%m%d%Y-%H%M%S")
	promptString = "#"
	crt.Screen.Send("\r")
	crt.Screen.WaitForString(promptString)
	screenrow = crt.Screen.CurrentRow - 1
	tray = crt.Screen.Get(screenrow, 1, screenrow, 1)
	crt.Screen.Send('\r')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	objTab = crt.GetScriptTab()
	objTab.Screen.Synchronous = True
	objTab.Screen.IgnoreEscape = True
	crt.Screen.Synchronous = True
	crt.Session.SetStatusText("This is an example")
	vanish = ( ' stty -echo' + "\r")
	objTab.Screen.Send( vanish )
	crt.Screen.Send("	 echo  " + chr(34) + "Collecting Storage Array status. Please wait..." + chr(34) + chr(13))
	crt.Screen.Send(" SMcli -d -v " + chr(124) + "egrep -i 'Attention" + chr(124) + "needs' " + chr(124) + " awk '" + chr(123) + "print $1" + chr(125) + "' > /tmp/Arrays.txt" + chr(13))
	crt.Screen.WaitForString("# ")
	crt.Screen.Send(" for x in `cat /tmp/Arrays.txt`; do" + chr(13))
	crt.Screen.Send("	 echo  " + chr(34) + " " + chr(34) + " " + chr(13))
	crt.Screen.Send("	 echo  " + chr(34) + "==========================================================================================" + chr(34) + chr(13))
	crt.Screen.Send("echo -e " + '"' + "ARRAY: $" + "{" + "x" + "}" + chr(92) + "n" + '"' + '\r')
	crt.Screen.Send(" SMcli -n $x -c " + chr(34) + "show storageArray healthStatus;" + chr(34) + " " + chr(13))
	crt.Screen.Send("done" + chr(13))
	crt.Screen.WaitForString("# ")
	crt.Screen.Send(" rm /tmp/Arrays.txt" + "\r")
	crt.Screen.WaitForString("# ")
	crt.Session.SetStatusText("")
	crt.Screen.Send (" stty echo \n\r")
	crt.Screen.Send (" stty echo \n\r")
	crt.Screen.WaitForString("# ")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	 
	logFileName = LOG_FILE_TEMPLATE + timestr +".log"
	result = SCRIPT_TAB.Screen.ReadString(prompt)
	result = result.replace("\n","")
	result = result.strip()
	filep = open(logFileName, 'a')
	crt.Screen.WaitForString(promptString)
	filep.write(result + os.linesep)
	time.sleep(1)
	filep.close()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	LaunchViewer(LOG_DIRECTORY)	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def LaunchViewer(filename2):
	try:
		os.startfile(filename2)
	except AttributeError:
		subprocess.call(['open', filename2])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def NN(number, digitCount):
	# Normalizes a single digit number to have digitCount 0s in front of it
	format = "%0" + str(digitCount) + "d"
	return format % number 
Main()
