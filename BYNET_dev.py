# $language = "Python"
# $interface = "1.0"

# Rev 10.00.00.03 corrected if no data enter on message box to exit
# Rev 10.00.00.02 corrected time stamp, is pulled now from customer system 02/19/2020 Luis Lopez
# Luis Lopez - 01/30/2020 ver. 10.00.00.01 @Teradata
# NetApp and DotHill Storage log files
# For NetApp Will download supportData,	 trace data, diagnosticData, and coredump if exists
# For DotHill will download debug logs
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import time
import os
import subprocess
import time
import io
import itertools
import random

other = "Start Over"
global_var =""

def main():
	def prompt_wait():
		return crt.Screen.WaitForStrings ([ "#", ">", ":", "OK."])

	def hideCMDS():
		crt.Screen.Send (" stty -echo \r" + "\n")
		prompt_wait()
		return

	def showCMDS():
		crt.Screen.Send (" stty echo \n\r")
		prompt_wait()
		return crt.Screen.Send (" stty echo \n\r")

	def clear_screen():
		return crt.Screen.Send(" clear"+"\r\n")

	def titleBuild(title):
		return crt.Screen.Send(' echo -e "#### ' +title+' ####"'+"\r\n\n")

	def return_ibinfo_cmd_builder(adapter,port,cmd,parameter):
		return crt.Screen.Send(' ibinfo -C '+ adapter +' -P '+port+' -d '+ cmd + parameter + '\r\n')

	def return_bam_check():
		return crt.Screen.Send(' echo; echo -e "### bam -s ###"; echo; bam -s; echo -e "### bam -w ###"; echo; bam -w; echo -e "### bam -e 15 ###"; echo; bam -e 15' + '\r\n')

	def return_sysinfo():
		return crt.Screen.Send(' echo; echo -e "### System Name: ###"; tdinfo | grep systemname; echo; echo -e "### System Family ###"; systemtype' + '\r\n')

	#~~~~~~~~~~Menu SCREENS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def return_main_menu_screen():
		main_menu_screen = crt.Dialog.Prompt("📝 Select an option from the menu:\n \n 1. Collect bam-a log. \n 2. Clear IB statistics.\n 3. PCI Mallanox Card check. \n     - PCI Card speed. \n     - Part info. \n     - Firmware Rev. \n 4. Bynet [single] node check.\n 5. Bynet [system-wide] check*^ ⚡\n 6. Infiniband switches utility\n 7. Collect logs for Bynet Engineering \n 8. Development/Testing", "🔴BYNET - Teradata GSO-HW Tools.", "1", False)
		return main_menu_screen

	def return_switch_screen():
		main_menu_screen = crt.Dialog.Prompt("📝 Select an option from the menu:\n \n 1. Connect to switch. \n 2. Infiniband switch health assessment.\n 3. Bynet [single] node check.\n 4. Bynet [system-wide] check*^\n 5. Infiniband switches utility\n 6. Collect logs for Bynet Engineering \n 7. Development/Testing", "🔴BYNET - Teradata GSO-HW Tools.", "1", False)
		return main_menu_screen

	def return_captureIP_screen():
		captureIP=crt.Dialog.Prompt("💡🎯Switch IP Address :", "Enter IP Address: ", "39.80.X.X", False)
		return captureIP

	def return_switch_select_screen():
		switch_selector=crt.Dialog.Prompt("🔴🔴🔴 1. Mellanox7800 \n 2. Mellanox5030 \n 3. Mellanox6036 \n 4. Mellanox6536 \n 5. Mellanox6518 \n 6. Voltaire GD4200 \n 7. Voltaire GD4700 ", "•Select IB switch model: ", "5030|7200 etc", False)
		return  switch_selector

#~~~~~~~~~~Infiniband Switches~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def return_ib_switch_connect(host, ib_password):
		crt.Screen.Send("ssh admin@"+host+'\r')
		prompt_wait()
		crt.Screen.Send(ib_password+'\r')
		prompt_wait()
		crt.Screen.Send("enable"+'\r')
		prompt_wait()
		return
	def return_switch_voltaire_connect(host, voltaire_password):
		crt.Screen.Send("ssh root@"+host+'\r')
		prompt_wait()
		crt.Screen.Send(voltaire_password+'\r')
		prompt_wait()
		return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Program starts here:
	main_menu_screen=return_main_menu_screen()

	if main_menu_screen=="1":
		#hideCMDS()
		#prompt_wait()

		crt.Screen.Send(' now=\"DATE#_$(date +%m-%d-%y__%I-%M-%P_%Z).log\"; bam -a > /tmp/bam-a__#systemname_$(tdinfo | grep systemname | awk \'{print $3}\')__#Node_$(whosmp)__\"$now\"; sleep 3; sz /tmp/bam-a__#systemname_$(tdinfo | grep systemname | awk \'{print $3}\')__#Node_$(whosmp)__\"$now\"' + '\r\n'  )
		prompt_wait()

		#showCMDS()
		#prompt_wait()
		pass

	elif main_menu_screen=="2":

		crt.Screen.Send(" ibinfo -d local_status | grep -i  mlx | awk '{print $1}' | awk 'NR==1 {print}'" + '\r')
		prompt_wait()
		screenrow=crt.Screen.CurrentRow -1
		ib0adapter = crt.Screen.Get(screenrow, 1, screenrow, 6)
		prompt_wait()

		crt.Screen.Send(" ibinfo -d local_status | grep -i  mlx | awk '{print $2}' | awk 'NR==1 {print}'" + '\r')
		prompt_wait()
		screenrow2=crt.Screen.CurrentRow -1
		ib0port= crt.Screen.Get(screenrow2, 1, screenrow2, 1)
		prompt_wait()

		crt.Screen.Send(" ibinfo -d local_status | grep -i  mlx | awk '{print $1}' | awk 'NR==2 {print}'" + '\r')
		prompt_wait()
		screenrow=crt.Screen.CurrentRow -1
		ib1adapter = crt.Screen.Get(screenrow, 1, screenrow, 6)
		prompt_wait()

		crt.Screen.Send(" ibinfo -d local_status | grep -i  mlx | awk '{print $2}' | awk 'NR==2 {print}'" + '\r')
		prompt_wait()
		screenrow2=crt.Screen.CurrentRow -1
		ib1port= crt.Screen.Get(screenrow2, 1, screenrow2, 1)
		prompt_wait()

		clear_screen()

		#~~~~~~~~~~~~~~Clear Infiniband statistics~~~~~~~~~~~~~~#
		prompt_wait()
		titleBuild("Clear Infiniband Statistics")
		prompt_wait()
		crt.Screen.Send(" ibinfo -C "+ib0adapter+" -P "+ib0port+" -a clear_ib_counters; ibinfo -C "+ib1adapter+" -P "+ib1port+" -a clear_ib_counters"+"\r")
		prompt_wait()

		pass
	#-->3. PCI Mellanox Card check (speed, PN, FW).
	elif main_menu_screen=="3":

		hideCMDS()
		prompt_wait()
		crt.Screen.Send(" p=\"-->\"; clear; echo -e \"### PCI Mellanox card speed check, all nodes ###\"; echo; echo -e \"$p PCI Mellanox speed all nodes\"; IBPCI=$(lspci | grep Mellanox | awk \'{print $1}\'); for IB in ${IBPCI[@]};do psh -netecho \"lspci -s $IB -vvv | grep LnkSta:\"; done; sleep 2; echo; echo -e \"### PCI Mellanox card info on $(whosmp) ###\"; echo -e \"$p ibinfo -d hca_vpd\"; ibinfo -d hca_vpd; echo; echo; echo -e \"### Verify PN on adapter is $(ibinfo -d hca_vpd | grep -w \'PN:\' | awk \'{print $2}\') on all the nodes ###\"; echo -e \"$p psh ibinfo -d hca_vpd\"; psh \"ibinfo -d hca_vpd | grep -E \'PCI bus|[=]|ID:|PN:\' | grep -vE \'VA:\'\"; echo; echo -e \"### Verify the FW version ###\"; echo -e \"$p psh ibinfo -d hca_fw|grep -i version\"; psh \"ibinfo -d hca_fw|grep -i version\"; echo; echo -e \"### Verify the psid ###\"; echo -e \"$p ibinfo -d hca_fw|grep -i psid\"; psh \"ibinfo -d hca_fw|grep -i psid\""+"\r")

		prompt_wait()

		showCMDS()
		prompt_wait()

		pass

		pass
	elif main_menu_screen=="6":

		switch_screen=return_switch_screen()
		if switch_screen=="1":
			host=return_captureIP_screen()
			switch_selector=return_switch_select_screen()

			pass

		#~~~~~~~~~~Mellanox Switches~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		if switch_selector=="1":
			return_ib_switch_connect(host, "TD-Mellanox7800")
			crt.Screen.Send("config terminal"+'\r')
			pass
		elif switch_selector=="2":
			return_ib_switch_connect(host, "TD-Mellanox5030")
			crt.Screen.Send("config terminal"+'\r')
			pass
		elif switch_selector=="3":
			return_ib_switch_connect(host, "TD-Mellanox6036")
			crt.Screen.Send("config terminal"+'\r')
			pass
		elif switch_selector=="4":
			return_ib_switch_connect(host, "TD-Mellanox6536")
			crt.Screen.Send("config terminal"+'\r')
			pass
		elif switch_selector=="4":
			return_ib_switch_connect(host, "TD-Mellanox6536")
			crt.Screen.Send("config terminal"+'\r')
			pass
		elif switch_selector=="5":
			return_ib_switch_connect(host, "TD-Mellanox6518")
			crt.Screen.Send("config terminal"+'\r')
			pass
		#~~~~~~~~~~Voltaire Switches~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		elif switch_selector=="6":
			return_switch_voltaire_connect(host, "TD-v4200")
			crt.Screen.Send("config terminal"+'\r')
			pass
		elif switch_selector=="7":
			return_switch_voltaire_connect(host, "TD-v4700")
			pass

	elif main_menu_screen=="d":

		crt.Screen.Send(' card=""; card=$(lspci | grep Mellanox | grep -oE "ConnectX-3|Connect-IB"); if [ $card == "ConnectX-3" ]; then echo "1"; elif [ $card == "Connect-IB" ]; then echo "3"; else echo "No IB-Card detected"; fi'+ '\r')
		prompt_wait()
		screenrow=crt.Screen.CurrentRow -1
		ib_adapter = crt.Screen.Get(screenrow, 1, screenrow, 1)
		if ib_adapter == "1":
			crt.Screen.Send(' echo -e "ConnectX-3 detected"'+"\r")
			prompt_wait()
			pass
		elif ib_adapter=="2":
			crt.Screen.Send(" echo -e 'Connect-IB detected'"+"\r")
			pass
		else:
			crt.Screen.Send(" echo -e 'No IB detected'"+"\r")
			pass


		#~~~new code starts here
		#byn0
		crt.Screen.Send (" stty -echo \r" + "\n")
		prompt_wait()
		crt.Screen.Send ("\r")
		prompt_wait()


		crt.Screen.Send(" var_ib0_adapter=$(ibinfo -d local_status | grep -i  mlx | awk '{print $1}' | awk 'NR==1 {print}')"+ '\r')
		prompt_wait()
		crt.Screen.Send(" var_ib0_port=$(ibinfo -d local_status | grep -i  mlx | awk '{print $2}' | awk 'NR==1 {print $1}')"+ '\r')
		prompt_wait()
		#byn1
		crt.Screen.Send(" var_ib1_adapter=$(ibinfo -d local_status | grep -i  mlx | awk '{print $1}' | awk 'NR==2 {print}')"+ '\r')
		prompt_wait()
		crt.Screen.Send(" var_ib1_port=$(ibinfo -d local_status | grep -i  mlx | awk '{print $2}' | awk 'NR==2 {print $1}')"+ '\r')
		prompt_wait()


		crt.Screen.Send(" clear"+"\r")
		prompt_wait()
		#sminfo byn0
		crt.Screen.Send(' ibinfo -C "$var_ib0_adapter" -P "$var_ib0_port" -d sminfo'+ '\r')
		prompt_wait()
		#sminfo byn1
		crt.Screen.Send(' ibinfo -C "$var_ib1_adapter" -P "$var_ib1_port" -d sminfo'+ '\r')

		crt.Screen.Send (" stty echo \n\r")
		prompt_wait()

	elif main_menu_screen=="n":
		#crt.Screen.Send (" echo -e hello s3cr3t"+'\r')
	#	crt.Screen.Send ( "\ r \ nhello, world! \ r \ n", True)

				# Here is where we will set the value of the string that will indicate that
		# we have reached the end of the data that we wanted to capture with the
		# ReadString method.
		szPrompt = "#"
		#prompt_wait()

		# Using GetScriptTab() will make this script 'tab safe' in that all of the
		# script's functionality will be carried out on the correct tab. From here
		# on out we'll use the objTab object instead of the crt object.
		objTab = crt.GetScriptTab()
		objTab.Screen.Synchronous = True

		# Instruct WaitForString and ReadString to ignore escape sequences when
		# detecting and capturing data received from the remote (this doesn't
		# affect the way the data is displayed to the screen, only how it is handled
		# by the WaitForString, WaitForStrings, and ReadString methods associated
		# with the Screen object).
		objTab.Screen.IgnoreEscape = True

		# We begin the process by sending a command. In this example script,
		# we're simply getting a file listing from a remote UNIX system using the
		# "ls -l" command.
		szCommand = "ibinfo -d local_status"
		objTab.Screen.Send(szCommand + "\r\n")

		# Wait for the command and the trailing CR to be echoed back from the remote
		# before we start capturing data... Otherwise, we'll capture the command we
		# issued, as well as the results, and in this example, we only want to
		# capture the results.
		objTab.Screen.WaitForString(szCommand + "\r\n")

		# This will cause ReadString() to capture data until we see the szPrompt
		# value.
		szResult = objTab.Screen.ReadString(szPrompt)

		# Display the results in a message box
		crt.Dialog.MessageBox(szResult)


	#	outPut = crt.Screen.ReadString ([ "error", "warning", "#"], 10)
	#	index = crt.Screen.MatchIndex
	#	if (index == 0):
	#	    crt.Dialog.MessageBox ( "Timed out!")
	#	elif (index == 1):
	#	    crt.Dialog.MessageBox ( "Found 'error'")
	#	elif (index == 2):
	#	    crt.Dialog.MessageBox ( "Found 'warning'")
	#	elif (index == 3):
	#	    crt.Dialog.MessageBox ( "Found '#'")

		crt.Screen.Send(" ibinfo -d local_status | grep -i  mlx | awk '{print $1}' | awk 'NR==1 {print}'" + '\r')
		prompt_wait()
		screenrow=crt.Screen.CurrentRow -1
		ib0adapter = crt.Screen.Get(screenrow, 1, screenrow, 6)
		crt.Screen.Send(" echo The output is: "+ib0adapter+'\r')
		prompt_wait()

		crt.Screen.Send(" clear"+'\r')

		crt.Screen.Send(" ibinfo -d local_status | grep -i  mlx | awk '{print $2}' | awk 'NR==1 {print}'" + '\r')
		prompt_wait()
		#curCol = crt.Screen.CurrentColumn
		#crt.Dialog.MessageBox (str (curCol))

		#curRow = crt.Screen.CurrentRow
		#crt.Dialog.MessageBox (str (curRow))
		screenrow=crt.Screen.CurrentRow -2
		ib0port = crt.Screen.Get(screenrow, 0, screenrow, 1)
		crt.Screen.Send(" echo The output is: "+ib0port+'\r')
		prompt_wait()

#		if ib0adapter == "1":
#			crt.Screen.Send(' echo -e "ConnectX-3 detected"'+"\r")
#			prompt_wait()
#			pass
#		elif ib0adapter=="2":
#			crt.Screen.Send(" echo -e 'Connect-IB detected'"+"\r")
#			pass
#		else:
#			crt.Screen.Send(" echo -e 'No IB detected'"+"\r")
#			pass
		pass
	#-->BYNET [system-wide] check^*.
	elif main_menu_screen=="5":

		crt.Screen.Synchronous = True

		errorGrep=" | grep -v '0           0           0           0'"


		crt.Screen.Send(" ibinfo -d local_status | grep -i  mlx | awk '{print $1}' | awk 'NR==1 {print}'" + '\r')
		prompt_wait()
		screenrow=crt.Screen.CurrentRow -1
		ib0adapter = crt.Screen.Get(screenrow, 1, screenrow, 6)
		prompt_wait()

		crt.Screen.Send(" ibinfo -d local_status | grep -i  mlx | awk '{print $2}' | awk 'NR==1 {print}'" + '\r')
		prompt_wait()
		screenrow2=crt.Screen.CurrentRow -1
		ib0port= crt.Screen.Get(screenrow2, 1, screenrow2, 1)
		prompt_wait()

		crt.Screen.Send(" ibinfo -d local_status | grep -i  mlx | awk '{print $1}' | awk 'NR==2 {print}'" + '\r')
		prompt_wait()
		screenrow=crt.Screen.CurrentRow -1
		ib1adapter = crt.Screen.Get(screenrow, 1, screenrow, 6)
		prompt_wait()

		crt.Screen.Send(" ibinfo -d local_status | grep -i  mlx | awk '{print $2}' | awk 'NR==2 {print}'" + '\r')
		prompt_wait()
		screenrow2=crt.Screen.CurrentRow -1
		ib1port= crt.Screen.Get(screenrow2, 1, screenrow2, 1)
		prompt_wait()

		clear_screen()
		prompt_wait()

		crt.Screen.Send(" sleep 5"+'\r')
		prompt_wait()
		#~~~~~~~~~~~~~~System info~~~~~~~~~~~~~~#
		return_sysinfo()
		prompt_wait()
		#~~~~~~~~~~~~~~Bam checks~~~~~~~~~~~~~~#
		titleBuild("Bynet general checks")
		prompt_wait()
		return_bam_check()
		crt.Screen.Send(" ibinfo -d local_status"+"\r\n")
		prompt_wait()
		crt.Screen.Send(" ibinfo -d local_netinfo"+"\r\n")
		prompt_wait()
		#~~~~~~~~~~~~~~PCI Mellanox Adapters~~~~~~~~~~~~~~#
		titleBuild("PCI Mellanox card speed check")
		prompt_wait()
		crt.Screen.Send(" IBPCI=$(lspci | grep Mellanox | awk \'{print $1}\'); for IB in ${IBPCI[@]};do psh -netecho \"lspci -s $IB -vvv | grep LnkSta:\"; done "+"\r\n")
		prompt_wait()
		#~~~~~~~~~~~~~~Commands for Domain 0~~~~~~~~~~~~~~#
		titleBuild("BYNET 0")
		prompt_wait()

		return_ibinfo_cmd_builder(ib0adapter,ib0port,"badlinks allhosts","")
		return_ibinfo_cmd_builder(ib0adapter,ib0port,"link_err_stat allhosts",errorGrep)
		return_ibinfo_cmd_builder(ib0adapter,ib0port,"llr_err_stat allhosts",errorGrep)
		return_ibinfo_cmd_builder(ib0adapter,ib0port,"fec_err_stat allhosts",errorGrep)

		return_ibinfo_cmd_builder(ib0adapter,ib0port,"badlinks allswitches","")
		return_ibinfo_cmd_builder(ib0adapter,ib0port,"link_err_stat allswitches",errorGrep)
		return_ibinfo_cmd_builder(ib0adapter,ib0port,"llr_err_stat allswitches",errorGrep)
		return_ibinfo_cmd_builder(ib0adapter,ib0port,"fec_err_stat allswitches",errorGrep)

		#~~~~~~~~~~~~~~Commands for Domain 1~~~~~~~~~~~~~~#
		titleBuild("BYNET 1")
		prompt_wait()

		return_ibinfo_cmd_builder(ib1adapter,ib1port,"badlinks allhosts","")
		return_ibinfo_cmd_builder(ib1adapter,ib1port,"link_err_stat allhosts",errorGrep)
		return_ibinfo_cmd_builder(ib1adapter,ib1port,"llr_err_stat allhosts",errorGrep)
		return_ibinfo_cmd_builder(ib1adapter,ib1port,"fec_err_stat allhosts",errorGrep)

		return_ibinfo_cmd_builder(ib1adapter,ib1port,"badlinks allswitches","")
		return_ibinfo_cmd_builder(ib1adapter,ib1port,"link_err_stat allswitches",errorGrep)
		return_ibinfo_cmd_builder(ib1adapter,ib1port,"llr_err_stat allswitches",errorGrep)
		return_ibinfo_cmd_builder(ib1adapter,ib1port,"fec_err_stat allswitches",errorGrep)
	pass

main()
