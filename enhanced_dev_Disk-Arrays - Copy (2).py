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
# GetArraySuppBundleOnly.py
# development

import time

other = "Start Over"
#menu_vendor_select = crt.Dialog.Prompt("■ Enter (1) for NetApp array or (2) for Seagate Array:", "►Teradata GSO-HW Tools: Disk Arrays", "1", False)
global_var ="True"



def main():

#------------------------------------------------------------------------------------------------------
#Program functions
	def prompt_wait():
		return crt.Screen.WaitForStrings ([ "#", ">", ":", "OK."])

	def get_array_name(array_name):
		array_name=crt.Dialog.Prompt("-->Disk Array Name :", "► Enter Array Name. ", "===HELLO LIC FROM VS-CODE===", False)
		return array_name
	def return_controller_select(id_controller):
		id_controller= crt.Dialog.Prompt("■ Select Controller (A|B): ", "► Select Controller from menu: ", "A|B", False)
		if id_controller=="A":
			return "1"
			pass
		if id_controller=="B":
			return "2"
			pass

	def return_to_main_program():
		crt.Dialog.MessageBox ( "Invalid selection ")
		do_menu_menu_vendor_select=return_menu_vendor_select()
		return
	def alert_invalid_selection():
		crt.Dialog.MessageBox ( "Invalid selection ")
		return

#------------------------------------------------------------------------------------------------------
#NetApp Functions
	def return_netapp_SMcli_builder(array_name,netapp_command):
		return crt.Screen.Send('SMcli -n ' + array_name + netapp_command + '\r')

	def return_netapp_rshfa_builder(diskArray_name, id_controller, cli_cmd):
		return crt.Screen.Send("rshfa "+diskArray_name+id_controller+cli_cmd+"\r")
	def return_netapp_cli_menu():
		return crt.Dialog.Prompt(" 1. getRecoveryFailureList_MT \n 2.vdmShowRAIDVolList \n 3. hwLogShow \n 4. fdiCapture \n 5. vdmShowDriveList  ","►NetApp CLI Menu ", "DAMC00X-X-X", False)
	def return_menu_vendor_select():
		 return crt.Dialog.Prompt("■  Enter (1) for NetApp array or (2) for Seagate Array:", "►Teradata GSO-HW Tools: Disk Arrays", "1", False)
	def return_netapp_main_menu():
		return crt.Dialog.Prompt("■ Menu of Commands \n \n 1. SupportBundle  \n 2. healthStatus \n 3. longRunningOperations \n 4. show allVolumes \n 5. storage ArrayProfile \n 6. show allDrives \n 7.allEvents(MEL) \n 8.show storageArray unreadableSectors \n 9. volumeDisribution \n 10. GHS Coverage  \n \n ■ Other Methods \n \n A. TELNET connect \n B. SHELL Menu \n \n ■ Automation* \n\n (A1*)-->Check health status, all arrays with attention needed \n (A2*)-->Check all arrays vol. registrations",	 "► NetApp SMcli Command Menu ", "1", False)
#------------------------------------------------------------------------------------------------------
#Seagate/DotHill Functions
	def return_seagateMenuFunction(global_var):
		return crt.Dialog.Prompt("■  DotHill menu: \n\n 1. Support Bundle \n 2.TELNET connect. \n\n ■ Automation** \n\n (D-A1*)-->Health status all arrays", "•Select Option from menu: ", "1|2", False)

	def return_seagate_session_connect(protocol, diskArray_name):
		crt.Screen.Send(protocol +diskArray_name+'\r')
		prompt_wait()
		crt.Screen.Send("manage"+'\r')
		prompt_wait()
		crt.Screen.Send("!manage"+'\r')

	def menu_segate_1():
		return crt.Dialog.Prompt("►►(DEV)Seagate Array Name :", "Enter Array Name: ", "DAMC00X-X-X", False)
#------------------------------------------------------------------------------------------------------
#Program starts here:
#NetApp section:

	do_menu_vendor_select=return_menu_vendor_select()
	diskArray_name=get_array_name("")
	if diskArray_name=="":
		alert_invalid_selection()
		return

	if do_menu_vendor_select == "1":

		do_netapp_main_menu=return_netapp_main_menu()
		if do_netapp_main_menu=="testing":
				crt.Screen.Send("echo hello DEV array"+'\r')
				prompt_wait()
				DEV_return_netapp_SMcli_builder(diskArray_name," -c 'show storageArray healthStatus;'")
				pass
		elif do_netapp_main_menu=="1":
				crt.Screen.Send("date +%m%d%y-%I%M%S%P \r")
				prompt_wait()
				screenrow = crt.Screen.CurrentRow - 1
				date_result = crt.Screen.Get(screenrow, 1, screenrow, 15)
				return_netapp_SMcli_builder(diskArray_name," -c 'save storageArray supportData file="'"'"/var/opt/teradata/"+diskArray_name+'_SupportBundle_'+date_result+'"'";'")
				prompt_wait()
				crt.Screen.Send("sz /var/opt/teradata/"+diskArray_name+'_SupportBundle_'+date_result+'*'+'\r')
				pass
		elif do_netapp_main_menu == "2":
			return_netapp_SMcli_builder(diskArray_name," -c 'show storageArray healthStatus;'")
			pass
		elif do_netapp_main_menu=="3":
			return_netapp_SMcli_builder(diskArray_name," -c 'show storageArray longRunningOperations;'")
			pass
		elif do_netapp_main_menu=="4":
			return_netapp_SMcli_builder(diskArray_name," -c 'show allVolumes;' | egrep 'Volume name|status|owner'")
			pass
		elif do_netapp_main_menu=="5":
			return_netapp_SMcli_builder(diskArray_name," -c 'show storageArray profile;'")
			pass
		elif do_netapp_main_menu=="6":
			return_netapp_SMcli_builder(diskArray_name," -c 'show allDrives summary;' ")
			pass
		elif do_netapp_main_menu=="7":
			return_netapp_SMcli_builder(diskArray_name," -c 'save storageArray allEvents file="'"'"/tmp/"+diskArray_name+'_MEL.txt"'";'")
			crt.Screen.WaitForString("#")
			crt.Screen.Send('egrep "Date|Description|Priority" '+"/tmp/"+diskArray_name+"_MEL.txt"+' | paste - - - | egrep -v "Informational" | less'+ '\r')
			pass
		elif do_netapp_main_menu=="8":
			return_netapp_SMcli_builder(diskArray_name," -c 'show storageArray unreadableSectors;'")
			pass
		elif do_netapp_main_menu=="9":
			return_netapp_SMcli_builder(diskArray_name," -c 'reset storageArray volumeDistribution;'")
			pass
		elif do_netapp_main_menu=="10":
			return_netapp_SMcli_builder(diskArray_name," -c 'show storageArray hotSpareCoverage;'")
			pass
		elif do_netapp_main_menu=="A":
			id_controller=return_controller_select("")
			crt.Screen.Send("telnet "+diskArray_name+id_controller+ '\r')
			crt.Screen.WaitForString(":")
			crt.Screen.Send("shellUsr"+ '\r')
			crt.Screen.WaitForString(":")
			crt.Screen.Send("wy3oo&w4"+ '\r')
			pass
		elif do_netapp_main_menu=="A1*":
			q1="'"

			crt.Screen.Send('clear; d="";z="";t="";clear; echo; echo -e "SMcli -d -v : Checking all NetApp Disk Arrys";  SMcli -d -v; sleep 2; t=$(SMcli -d -v |grep -i attention| awk '+q1+"{print$1}"+q1+' | wc -w);echo; echo -e "There is a total of "$t" Arrays with attention needed.. Checking Disk Arrays...";sleep 3; d=$(SMcli -d -v | grep -i attention | awk '+q1+"{print $1}"+q1+'); for i in ${d[@]}; do z="SMcli -n $i -c '+q1+"show storageArray healthStatus;"+q1+'"; echo; echo -e "▬▬▬▬Checking health status for NetApp Disk Array: $i▬▬▬▬";echo;  echo "--->$z"; eval $z; done'+"\r")

			pass
		elif do_netapp_main_menu=="A2*":
			q1="'"
			crt.Screen.Send('clear; d="";z=""; z="SMcli -n $i -c '+q1+"show allVolumes reservations;"+q1+' |grep -i Regist"; SMcli -d -v; sleep 4; echo; echo -e "--->Checking status of Disk Arrays Reservations: "; echo; d=$(SMcli -d -v | awk '+q1+"{print $1}"+q1+'); for i in ${d[@]}; do echo; echo -e "■ Checking reservations for NetApp Disk Array: $i \n"; echo "-->$z"; eval $z; done '+"\r")

#------------------------------------------------------------------------------------------------------
#Netapp CLI section
		if do_netapp_main_menu=="B":
			do_netapp_cli_menu=return_netapp_cli_menu()
			if do_netapp_cli_menu=="1":
				id_controller=return_controller_select("")
				return_netapp_rshfa_builder(diskArray_name, id_controller," getRecoveryFailureList_MT")
				pass
			elif do_netapp_cli_menu=="2":
				id_controller=return_controller_select("")
				return_netapp_rshfa_builder(diskArray_name, id_controller," vdmShowRAIDVolList")
				pass
			elif do_netapp_cli_menu=="3":
				id_controller=return_controller_select("")
				return_netapp_rshfa_builder(diskArray_name, id_controller," hwLogShow")
				pass
			elif do_netapp_cli_menu=="4":
				id_controller=return_controller_select("")
				return_netapp_rshfa_builder(diskArray_name, id_controller," fdiCapture")
				pass
			elif do_netapp_cli_menu=="5":
				id_controller=return_controller_select("")
				return_netapp_rshfa_builder(diskArray_name, id_controller," vdmShowDriveList")
				pass
#------------------------------------------------------------------------------------------------------
#Seagate/DotHill section:
	if do_menu_vendor_select == "2":

		do_seagateMenuFunction=return_seagateMenuFunction("")

		if do_seagateMenuFunction=="testing":
			return_seagate_session_connect("ftp ",diskArray_name)
			prompt_wait()
			crt.Screen.Send("get logs "+diskArray_name+"_SupportBundle_.zip"+"\r")
			prompt_wait()
			crt.Screen.Send("bye"+'\r')
			prompt_wait()

			pass

		if do_seagateMenuFunction=="other":
			crt.Screen.Send("date +%m%d%y-%I%M%S%P"+'\r')
			prompt_wait()
			screenrow = crt.Screen.CurrentRow - 1
			date_result = crt.Screen.Get(screenrow, 1, screenrow, 15)
			crt.Screen.Send("cd /tmp" +'\r')
			prompt_wait()
			return_seagate_session_connect("ftp ", diskArray_name)
			prompt_wait()
			crt.Screen.Send("get logs "+diskArray_name+"_SupportBundle_"+date_result+".zip"+"\r")
			prompt_wait()
			crt.Screen.Send("bye"+'\r')
			prompt_wait()
			crt.Screen.Send("sz /tmp/"+diskArray_name+"_SupportBundle_"+date_result+"*"+"\r")
			pass

		elif do_seagateMenuFunction=="2":
			return_seagate_session_connect("telnet ", diskArray_name)
			prompt_wait()
			pass
		elif do_seagateMenuFunction=="D-A1*":
			q1="'"
			crt.Screen.Send('d="";z=""; cat /etc/hosts | grep -i damc; echo -e "\n This command will perform a quick health check against all DotHill Arrays in this system...\n\n"; d=$(cat /etc/hosts| grep -i damc | awk '+q1+"{print $2}"+q1+'); for i in ${d[@]}; do z="rshfa -V dh $i show system | egrep -v '+q1+"System Contact|System Location|Vendor Name|Product Brand|SCSI|Supported Locales|Command completed"+q1+'"; echo -e "\nRunning Health check on: $i \n\n"; eval $z; done'+"\r")
			pass


	#	commandb = crt.Dialog.Prompt("►Seagate Array Name :", "Enter Array Name: ", "DAMC00X-X-X", False)
		#my_segate_menu=return_seagateMenuSelect("1")


		if do_seagateMenuFunction=="1":
			#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
					promptString = "#"
					crt.Screen.Send( "cd /tmp" + '\r')
					crt.Screen.WaitForString(promptString)
					crt.Screen.Send("date +%m%d%y-%I%M%S%P \r")
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
					filed = "Store-" + diskArray_name + "_" + result + xtype
					crt.Screen.Send( cmdb + diskArray_name + '\r')
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
					pass
			#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		else:
				return
main()
