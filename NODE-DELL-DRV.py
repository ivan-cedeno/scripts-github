# $language = "python"
# $interface = "1.0"


# Luis Lopez,  NODE-DELL-DRV.py, @teradata 2022
# 
#omreport storage vdisk controller=0 | grep "^\(ID\|Status\|State\|Layout\|Device Name\)" | awk '{print $1 " " $2 "	 " $3 "	 " $4}' | paste - - - - -
#omreport storage pdisk controller=0 | grep "^\(ID\|Status\|State\|Failure\|SAS Address\|Progress\)" | awk '{print $1 " " $2 "	" $3 "	" $4 }' | paste - - - - - -
#omconfig storage controller controller=0 action=exportlog
#omreport storage vdisk | egrep '^(ID|Status|State)'
#omreport storage vdisk controller=0 | awk '/^ID/ {print $NF}' | while read v; \
#do omreport storage vdisk controller=0 vdisk=$v | grep -E '^(ID|State|Layout|Size)'; \
#omreport storage pdisk controller=0 vdisk=$v | grep -E '^(Status|Name|State|Capacity|$)'; done
# This script assumes the user has logged in and is sitting at a command
# prompt as the script is launched from SecureCRT's 'Script -> Run' menu.

import time

def Main():
	szPrompt = "#", ":"
	
	objTab = crt.GetScriptTab()
	objTab.Screen.Synchronous = True
	objTab.Screen.IgnoreEscape = True	
	crt.Screen.Send("\r|*****************************************************|\r\n",True)
	crt.Screen.Send("\r|============ Checking slots on enclosure ============|\r\n",True)
	crt.Screen.Send("\r|_____________________________________________________|\r\n",True)
	time.sleep(1) # Sleep for 1 seconds
	tdcmd0 = " omreport	 storage enclosure controller=0 enclosure=0:1 info=pdslotreport | egrep	 '^(Hot Spare|Slot Count|Occupied Slot Count|Occupied Slots|Empty Slots)'"
	objTab.Screen.Send(tdcmd0 + "\r\n")	
	szResult = objTab.Screen.ReadString(szPrompt)
	time.sleep(1) # Sleep for 1 seconds
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	  
	crt.Screen.Send("\r|*****************************************************|\r\n",True)
	crt.Screen.Send("\r|============ Physical  Disk Status/State ============|\r\n",True)
	crt.Screen.Send("\r|_____________________________________________________|\r\n",True)
	tdcmd1 = " omreport storage pdisk controller=0 | grep '^\(ID\|Status\|Serial\|State\|Failure\|SAS Address\|Progress\)' | awk '{print $1 " " $2 "	 " $3 "	 " $4 }' | paste - - - - - - -"
	objTab.Screen.Send(tdcmd1 + "\r\n")	
	szResult = objTab.Screen.ReadString(szPrompt)
	time.sleep(1) # Sleep for 1 seconds
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	crt.Screen.Send("\r|*****************************************************|\r\n",True)
	crt.Screen.Send("\r|============== Vdisk  Disk Status/State =============|\r\n",True)
	crt.Screen.Send("\r|_____________________________________________________|\r\n",True)
	tdcmd2 = " omreport storage vdisk controller=0 | grep '^\(ID\|Status\|State\|Layout\|Device Name\)' | awk '{print $1 " " $2 "	 " $3 "	 " $4}' | paste - - - - -"
	objTab.Screen.Send( tdcmd2 + "\r\n")
	szResult = objTab.Screen.ReadString(szPrompt)
	time.sleep(1) # Sleep for 1 seconds
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	vanish = ( ' stty -echo' + "\r")
	objTab.Screen.Send( vanish )
	crt.Screen.Send("\r|*****************************************************|\r\n",True)
	crt.Screen.Send("\r|========== Disks belonging to Virtual Disk ==========|\r\n",True)
	crt.Screen.Send("\r|_____________________________________________________|\r\n",True)
	crt.Screen.Synchronous = True
	echoline = (' echo " "')
	crt.Screen.Send( echoline + ";" + " omreport storage vdisk controller=0 " + chr(124) + " awk '/^ID/ " + chr(123) + "print $NF" + chr(125) + "' " + chr(124) + " while read v" + chr(13))
	crt.Screen.Send(" do" + chr(13))
	crt.Screen.Send(" echo " + chr(34) + "==================================|" + chr(34) + chr(13))
	crt.Screen.Send(" omreport storage vdisk controller=0 vdisk=$v " + chr(124) + " grep -E '^(ID" + chr(124) + "State" + chr(124) + "Layout" + chr(124) + "Size)'" + chr(13))
	crt.Screen.Send(" omreport storage pdisk controller=0 vdisk=$v " + chr(124) + " grep -E '^(Status" + chr(124) + "Name" + chr(124) + "State" + chr(124) + "Capacity" + chr(124) + "$)'" + chr(13))
	crt.Screen.Send(" done" + chr(13))
	crt.Screen.Send (" stty echo \n\r")
	crt.Screen.Send (" stty echo \n\r")
	szResult = objTab.Screen.ReadString(szPrompt)	
Main()