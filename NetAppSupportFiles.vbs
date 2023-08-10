#$language = "VBScript"
#$interface = "1.0"

crt.Screen.Synchronous = True

'integration Luis Lopez @teradata 04/19/2022
' NetAppSupportFiles.vbs
'

Dim g_objIE, g_objTab
set g_objTab = crt.GetScriptTab

Dim g_fso
Set g_fso = CreateObject("Scripting.FileSystemObject")
Dim datevalue, timevalue, dtsnow, dtsvalue

'Store DateTimeStamp once.
dtsnow = Now()

'Individual date components
dd = Right("00" & Day(dtsnow), 2)
mm = Right("00" & Month(dtsnow), 2)
yy = Year(dtsnow)
hh = Right("00" & Hour(dtsnow), 2)
nn = Right("00" & Minute(dtsnow), 2)
ss = Right("00" & Second(dtsnow), 2)

'Build the date string in the format yyyy-mm-dd
minutevalue = mm & ss
'Build the date string in the format yyyy-mm-dd
datevalue = mm & "" & dd & "" & yy
'Build the time string in the format hh:mm:ss
timevalue = hh & nn & ss
'Concatenate both together to build the timestamp yyyy-mm-dd hh:mm:ss
dtsvalue = datevalue & "-" & TimeValue
dtsvalue1 = datevalue &".zip"
zipvalue = ".zip"
dtsvalue3 = minutevalue

g_objTab.Screen.Synchronous = True

'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sub Main()
	arrayName = crt.Dialog.Prompt("Please enter array name", "GSO Hardware", "DAMC0XX-XX", False)
	' Supply array name
	If arrayName = "" Then Exit Sub
	if Not g_objTab.Session.Connected then
		MsgBox "This script was designed to be launched from a tab " & _
			   "that is already connected to a remote machine."
		exit sub
	end if
	
	Dim szExpect1, szExpect2, szExpect3, szExpect4, szExpect5, szExpect6, szExpect7, szExpect8
	Dim szSend1, szSend2, szSend3, szSend4, szSend5, szSend6, szSend7, szSend8
	Dim bLogOutput, szLogFile, szAppendOrOverwrite
	crt.screen.Send " cd /var/opt/teradata" & chr(13) 
	szSend1 = " SMcli -n " & arrayName& " -c " & "'save storageArray supportData file=" & chr(34) & arrayName&"-SupportBundle-"& dtsvalue & chr(34)&";'" & chr(13) 
	szExpect1 = "#"
	szSend2 = " sz " & arrayName&"-SupportBundle-"&dtsvalue&"*"
	szExpect2 = "#"
	szSend3 = " SMcli -n " & arrayName & " -c " & "'start controller [both] trace dataType=all forceFlush=false file="& chr(34) & arrayName&"-dqlog-"& dtsvalue & chr(34) & ";'" & " -trace all" 
	szExpect3 = "#"
	szSend4 = " sz " & arrayName&"-dqlog-"&dtsvalue&"*"
	szExpect4 = "#"
	szSend5 = " SMcli -n " & arrayName& " -c " & "'save storageArray controllerHealthImage file=" & chr(34) & arrayName&"-Crdmp"&minutevalue & zipvalue & chr(34)&";'" & chr(13)
	szExpect5 = "#"
	szSend6 = " sz " & arrayName&"-Crdmp"&minutevalue&zipvalue&"*" 
	szExpect6 = "#"
	szSend7 = " SMcli -n " & arrayName& " -c " & "'save storageArray diagnosticData file=" & chr(34) & arrayName&"-DDC-"& dtsvalue1 & chr(34)&";'" & chr(13)
	szExpect7 = "#"
	szSend8 = " sz " & arrayName&"-DDC-"&dtsvalue&"*"
	szExpect8 = "#"
	bLogOutput = True
	szLogFile1 = "C:\temp\cmd-output"
	szLogFile = szLogFile1 & "-" & arrayName & "-" & dtsvalue & ".log"
	szAppendOrOverwrite = "Append"
	
	szSavedLogFileName = g_objTab.Session.LogFileName
	Dim szTempLogFileName 
	
	Do
		if Not PromptForInput(szSend1, szExpect1, _
								szSend2, szExpect2, _
								szSend3, szExpect3, _
								szSend4, szExpect4, _
								szSend5, szExpect5, _
								szSend6, szExpect6, _
								szSend7, szExpect7, _
								szSend8, szExpect8, _
								bLogOutput, szLogFile, _
								szAppendOrOverwrite) then
			MsgBox "GSO User Canceled the Activity"
			exit sub
		end if
		
		if bLogOutput then
			if szLogFile = "" then
				MsgBox "Log filename required if Log option is enabled."
			else		  
				if Not g_fso.FolderExists(g_fso.GetParentFolderName(szLogFile)) then
					MsgBox "Log folder path does not exist: " & vbcrlf & vbcrlf & _
						vbtab & g_fso.GetParentFolderName(szLogFile) & vbcrlf & _
						vbcrlf & "Please specify a log file name in an existing folder."
				else
					szTempLogFileName = szLogFile
					exit do
				end if
			end if
		else
			exit do
		end if
	Loop
	
	if bLogOutput then
		' 1.1) Determine which log mode to use...
		Dim bAppend
		Select Case szAppendOrOverwrite
			Case "Append"
				bAppend = True
			Case "Overwrite"
				bAppend = False
			Case Else
				MsgBox "Unknown LogMode value: " & szAppendOrOverwrite
				exit sub
		End Select
		
		' 1.2) Turn off logging on the old file if it's enabled
		if g_objTab.Session.Logging then g_objTab.Session.Log False
		
		' 1.3) Set up the current session to log to the temporary log file
		'	   specified in the user dialog
		g_objTab.Session.LogFileName = szTempLogFileName
			 
		' 1.3) Start logging with the appropriate log mode
		g_objTab.Session.Log True, bAppend
	end if
	
	g_objTab.Screen.Send  szSend1 & vbcr
	if szExpect1 <> "" then g_objTab.Screen.WaitForString szExpect1
	g_objTab.Screen.Send  szSend2 & vbcr
	if szExpect2 <> "" then g_objTab.Screen.WaitForString szExpect2
	g_objTab.Screen.Send  szSend3 & vbcr
	if szExpect3 <> "" then g_objTab.Screen.WaitForString szExpect3
	g_objTab.Screen.Send  szSend4 & vbcr
	if szExpect4 <> "" then g_objTab.Screen.WaitForString szExpect4
	g_objTab.Screen.Send  szSend5 & vbcr
	if szExpect5 <> "" then g_objTab.Screen.WaitForString szExpect5
	g_objTab.Screen.Send  szSend6 & vbcr
	if szExpect6 <> "" then g_objTab.Screen.WaitForString szExpect6
	g_objTab.Screen.Send  szSend7 & vbcr
	if szExpect7 <> "" then g_objTab.Screen.WaitForString szExpect7
	g_objTab.Screen.Send  szSend8 & vbcr
	if szExpect8 <> "" then g_objTab.Screen.WaitForString szExpect8
	if bLogOutput then
		g_objTab.Session.Log False
		g_objTab.Session.LogFileName = szSavedLogFileName
	end if
	
End Sub

'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Function PromptForInput(byRef szSend1,	byRef szExpect1, _
						byRef szSend2,	byRef szExpect2, _
						byRef szSend3,	byRef szExpect3, _
						byRef szSend4,	byRef szExpect4, _
						byRef szSend5,	byRef szExpect5, _
						byRef szSend6,	byRef szExpect6, _
						byRef szSend7,	byRef szExpect7, _
						byRef szSend8,	byRef szExpect8, _
						byRef bLogOutput, byRef szLogFile, _
						byRef szAppendOrOverwrite)
	Set g_objIE = CreateObject("InternetExplorer.Application")
	g_objIE.Offline = True
	g_objIE.navigate "about:blank"
	
	' Wait for the navigation to the "blank" web page to complete
	Do
		crt.Sleep 100
	Loop While g_objIE.Busy
	
	g_objIE.Document.body.Style.FontFamily = "Sans-Serif"
	g_objIE.Document.body.Style.Color = "white"
	g_objIE.Document.body.style.backgroundColor = "#3a4851"
	g_objIE.Document.body.style.border = "thick solid Orange"
	g_objIE.Document.getElementsByClassName("check")
	g_objIE.Document.Body.innerHTML = _
		"&nbsp;&nbsp;&nbsp;<b>CMD<u>1</u>:</b><input name='Send1' size='140' maxlength='512' AccessKey='1' tabindex=1><br>" & _
		"<b>Prompt:</b><input name='Expect1' size='80' maxlength='512'>" & _
		"<p></p>" & _
		"&nbsp;&nbsp;&nbsp;<b>CMD<u>2</u>:</b><input name='Send2' size='140' maxlength='512' AccessKey='2'><br>" & _
		"<b>Prompt:</b><input name='Expect2' size='80' maxlength='512'>" & _
		"<p></p>" & _
		"&nbsp;&nbsp;&nbsp;<b>CMD<u>3</u>:</b><input name='Send3' size='140' maxlength='512' AccessKey='3'><br>" & _
		"<b>Prompt:</b><input name='Expect3' size='80' maxlength='512'>" & _
		"<p></p>" & _
		"&nbsp;&nbsp;&nbsp;<b>CMD<u>4</u>:</b><input name='Send4' size='140' maxlength='512' AccessKey='4'><br>" & _
		"<b>Prompt:</b><input name='Expect4' size='80' maxlength='512'>" & _
		"<p></p>" & _
		"&nbsp;&nbsp;&nbsp;<b>CMD<u>5</u>:</b><input name='Send5' size='140' maxlength='512' AccessKey='5'><br>" & _
		"<b>Prompt:</b><input name='Expect5' size='80' maxlength='512'>" & _
		"<p></p>" & _
		"&nbsp;&nbsp;&nbsp;<b>CMD<u>6</u>:</b><input name='Send6' size='140' maxlength='512' AccessKey='6' tabindex=1><br>" & _
		"<b>Prompt:</b><input name='Expect6' size='80' maxlength='512'>" & _
		"<p></p>" & _	
		"&nbsp;&nbsp;&nbsp;<b>CMD<u>7</u>:</b><input name='Send7' size='140' maxlength='512' AccessKey='7'><br>" & _
		"<b>Prompt:</b><input name='Expect7' size='80' maxlength='512'>" & _
		"<p></p>" & _
		"&nbsp;&nbsp;&nbsp;<b>CMD<u>8</u>:</b><input name='Send8' size='140' maxlength='512' AccessKey='8'><br>" & _
		"<b>Prompt:</b><input name='Expect8' size='80' maxlength='512'>" & _
		"<p></p>" & _		
		"<input name='LogOutput' type='checkbox' onclick=""document.all('ButtonHandler').value='LogOutput';"" AccessKey='L'><u>L</u>og Output to File<br>" & _
		"&nbsp;&nbsp;&nbsp;&nbsp;" & _
			"<b>Log <u>f</u>ilename:</b><input name='LogFilename' size='71' maxlength='512' AccessKey='f'><br>" & _
		"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;" & _
			"<input type=radio name='LogMode' value='Append' AccessKey='A' checked><u>A</u>ppend<br>" & _
		"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;" & _
			"<input type=radio name='LogMode' value='Overwrite' Accesskey='w' >Over<u>w</u>rite<br>" & _
		"<hr>" & _
		"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<button name='OK' AccessKey='O' onclick=document.all('ButtonHandler').value='OK';><u>O</u>K</button>" & _
		"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" & _
		"<button name='Cancel' AccessKey='C' onclick=document.all('ButtonHandler').value='Cancel';><u>C</u>ancel</button>" & _
		"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<button name='openKB' AccessKey='K' onclick=document.all('ButtonHandler').value='openKb ';><u>K</u>B0013920</button>" & _
		"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i> Refer to KB0013920 for commands and syntax&nbsp;</i>" & _
		"<input name='ButtonHandler' type='hidden' value='Nothing Clicked Yet'>"
	
	g_objIE.MenuBar = False
	g_objIE.StatusBar = True
	g_objIE.AddressBar = False
	g_objIE.Toolbar = False
	g_objIE.height = 690
	g_objIE.width = 990  
	' g_objIE.Navigate "http://www.google.com/"
	g_objIE.document.Title = "GSO Tools Dialog "
	g_objIE.Visible = True
	
	' Wait for the "dialog" to be displayed before we attempt to set any
	' of the dialog's default values.
	Do
		crt.Sleep 100
	Loop While g_objIE.Busy
	' This code brings the IE window to the foreground. REMOVED
	Set objShell = CreateObject("WScript.Shell")
	objShell.AppActivate g_objIE.document.Title
	Set shell = CreateObject("WScript.Shell")
	
	' Set up defaults within the dialog
	g_objIE.Document.All("Send1").Value = szSend1
	g_objIE.Document.All("Expect1").Value = szExpect1
	g_objIE.Document.All("Send2").Value = szSend2
	g_objIE.Document.All("Expect2").Value = szExpect2
	g_objIE.Document.All("Send3").Value = szSend3
	g_objIE.Document.All("Expect3").Value = szExpect3
	g_objIE.Document.All("Send4").Value = szSend4
	g_objIE.Document.All("Expect4").Value = szExpect4
	g_objIE.Document.All("Send5").Value = szSend5
	g_objIE.Document.All("Expect5").Value = szExpect5	
	g_objIE.Document.All("Send6").Value = szSend6
	g_objIE.Document.All("Expect6").Value = szExpect6
	g_objIE.Document.All("Send7").Value = szSend7
	g_objIE.Document.All("Expect7").Value = szExpect7	
	g_objIE.Document.All("Send8").Value = szSend8
	g_objIE.Document.All("Expect8").Value = szExpect8	
	
	g_objIe.Document.All("LogOutput").Checked = bLogOutput
	g_objIE.Document.All("LogFilename").Value = szLogFile
	
	Select Case szAppendOrOverwrite
		Case "Overwrite"
			g_objIE.Document.All("LogMode")(1).Select
			g_objIE.Document.All("LogMode")(1).Checked = true
			g_objIE.Document.All("LogMode")(1).Click

		Case "Append"
		Case Else
			g_objIE.Document.All("LogMode")(0).Select
			g_objIE.Document.All("LogMode")(0).Checked = false
			g_objIE.Document.All("LogMode")(0).Click

	End Select	  

	Do
		On Error Resume Next
			Err.Clear
			szNothing = g_objIE.Document.All("ButtonHandler").Value
			if Err.Number <> 0 then exit function
 
		Select Case g_objIE.Document.All("ButtonHandler").Value
			Case "Cancel"
				g_objIE.Quit
				
				End Select	
' test
		Select Case g_objIE.Document.All("ButtonHandler").Value
			Case "openKb"
				g_objIE.Offline = True
				g_objIE.navigate "about:blank"
				StartURL = "www.google.com" 
				set IE = CreateObject("InternetExplorer.Application") 
				IE.Visible = true 
				IE.Navigate StartURL 
				
				exit function
' End
			
			Case "OK"
				' Capture data from each field in the dialog...
				szSend1	   = g_objIE.Document.All("Send1").Value
				szExpect1  = g_objIE.Document.All("Expect1").Value
				szSend2	   = g_objIE.Document.All("Send2").Value
				szExpect2  = g_objIE.Document.All("Expect2").Value
				szSend3	   = g_objIE.Document.All("Send3").Value
				szExpect3  = g_objIE.Document.All("Expect3").Value
				szSend4	   = g_objIE.Document.All("Send4").Value
				szExpect4  = g_objIE.Document.All("Expect4").Value	
				szSend5	   = g_objIE.Document.All("Send5").Value
				szExpect5  = g_objIE.Document.All("Expect5").Value
				szSend6	   = g_objIE.Document.All("Send6").Value
				szExpect6  = g_objIE.Document.All("Expect6").Value	
				szSend7	   = g_objIE.Document.All("Send7").Value
				szExpect7  = g_objIE.Document.All("Expect7").Value	
				szSend8	   = g_objIE.Document.All("Send8").Value
				szExpect8  = g_objIE.Document.All("Expect8").Value
				bLogOutput = g_objIE.Document.All("LogOutput").Checked
				szLogFile  = g_objIE.Document.All("LogFilename").Value
				
				for nIndex = 0 to g_objIE.Document.All("LogMode").Length - 1
					if g_objIE.Document.All("LogMode")(nIndex).Checked then
						szAppendOrOverwrite = g_objIE.Document.All("LogMode")(nIndex).Value
						exit for
					end if
				Next
				
				PromptForInput = True

				g_objIE.Quit
				
				exit function
				
			Case "LogOutput"

				g_objIE.Document.All("ButtonHandler").value = ""
				
				' Handle the check in real-time...
				if g_objIE.Document.All("LogOutput").Checked then
					' Enable the other elements of the dialog dealing with
					' logging
					g_objIE.Document.All("LogFilename").Disabled = False
					g_objIE.Document.All("LogMode")(0).Disabled = False
					g_objIE.Document.All("LogMode")(1).Disabled = False
				else
					' Disable the other elements of the dialog dealing with
					' logging
					g_objIE.Document.All("LogFilename").Disabled = True
					g_objIE.Document.All("LogMode")(0).Disabled = True
					g_objIE.Document.All("LogMode")(1).Disabled = True
				end if
					
			End Select
			
		On Error Goto 0
		' Wait for user interaction with the dialog... Instead of crt.Sleep,
		' we use g_objTab.Screen.WaitForString and pass in a string that
		' is never expected to be found.  The worst case scenario here is
		' that 1 second will pass between the time that the user clicks on
		' the OK button and the dialog goes away, for example.
		' We do this to avoid 100% CPU usage.
		g_objTab.Screen.WaitForString "1324;l1@#$!@#$!@#$ This will never appear", 1
	Loop

	
End Function