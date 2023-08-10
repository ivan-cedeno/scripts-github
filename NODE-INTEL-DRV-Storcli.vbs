# $language = "VBScript"
# $interface = "1.0"

' Luis Lopez 2023
'/opt/MegaRAID/CmdTool2/CmdTool2 -PDList -a0 | egrep  'Enclosure Device ID|Slot|Media Error|Other Error|Predictive Failure Count|Firmware state\(0\)' | paste - - - - -
'/opt/MegaRAID/CmdTool2/CmdTool2 -LDPDinfo -a0 | grep '^\(Virtual Drive\|State\|Number Of Drives\)' | paste - - -
'/opt/MegaRAID/CmdTool2/CmdTool2 -LdPdInfo -aAll | egrep '^Adapter|^Number of Virtual|^Virtual Drive:|^Name|^Enclosure Device ID:|^Slot Number:|^Inquiry Data:' | grep -v 'Adapter'


Sub Main

Dim datevalue, timevalue, dtsnow, dtsvalue 
	dtsnow = Now() 
	dd = Right("00" & Day(dtsnow), 2)
	mm = Right("00" & Month(dtsnow), 2)
	yy = Year(dtsnow)
	hh = Right("00" & Hour(dtsnow), 2)
	nn = Right("00" & Minute(dtsnow), 2)
	ss = Right("00" & Second(dtsnow), 2) 
	minutevalue = mm & ss
	datevalue = mm & "" & dd & "" & yy
	timevalue = hh & nn & ss
	dtsvalue = datevalue & "-" & TimeValue
	dtsvalue1 = datevalue &".zip"
	zipvalue = ".zip"
	dtsvalue3 = minutevalue
	
Const ForReading = 1
Const ForWriting = 2
Const ForAppending = 8
  crt.Screen.Synchronous = True
  Dim fso, file
  Set fso = CreateObject("Scripting.FileSystemObject")
  Set oShell = CreateObject("WScript.Shell")
  strHomeFolder = oShell.ExpandEnvironmentStrings("%USERPROFILE%\Downloads")
  Set file = fso.OpenTextFile(strHomeFolder &"\output-" & dtsvalue & ".log", ForWriting, True)
  Dim waitStrs
  waitStrs = Array( Chr(10), "#" )
  Dim row, screenrow, readline, items
  row = 1
  crt.Screen.Send "" & vbcr & vblf , True
  crt.Screen.Send "-------------------------------------------------------" & vbcr & vblf , True
  crt.Screen.Send "|============ Physical  Disk Status/State ============|" & vbcr & vblf , True
  crt.Screen.Send "-------------------------------------------------------" & vbcr & vblf , True
  crt.Screen.Send "  /opt/MegaRAID/storcli/storcli64 -PDList -a0 | egrep 'Enclosure Device ID|Slot|Media Error|Other Error|Predictive Failure Count|Firmware state\(0\)' | paste - - - - -" & vbcr
  crt.Screen.Send ""
  crt.Screen.WaitForString chr(10) 
  Do
    result = crt.Screen.WaitForStrings( waitStrs )
    If result = 2 Then
        Exit Do
    End If
    szLineAbove = crt.Screen.Get(_
        crt.screen.CurrentRow - 1, _
        1, _
        crt.screen.CurrentRow - 1, _
        crt.Screen.Columns)
        
    file.Write szLineAbove & vbCrLf
  Loop
'#################################
  waitStrs = Array( Chr(10), "#" )
  row = 1
  crt.Screen.Send "" & vbcr & vblf , True
  crt.Screen.Send "-------------------------------------------------------" & vbcr & vblf , True
  crt.Screen.Send "|================= Vdisk Status/State =================|" & vbcr & vblf , True
  crt.Screen.Send "-------------------------------------------------------" & vbcr & vblf , True
  crt.Screen.Send " /opt/MegaRAID/storcli/storcli64 -LDPDinfo -a0 | grep '^\(Virtual Drive\|State\|Number Of Drives\)' | paste - - - " & vbcr
  crt.Screen.WaitForString chr(10) 
  Do
    result = crt.Screen.WaitForStrings( waitStrs )
    If result = 2 Then
        Exit Do
    End If
    szLineAbove = crt.Screen.Get(_
        crt.screen.CurrentRow - 1, _
        1, _
        crt.screen.CurrentRow - 1, _
        crt.Screen.Columns)
    file.Write szLineAbove & vbCrLf
  Loop
'###################################
  waitStrs = Array( Chr(10), "#" )
  row = 1
  crt.Screen.Send "" & vbcr & vblf , True
  crt.Screen.Send "-------------------------------------------------------" & vbcr & vblf , True
  crt.Screen.Send "|=========== Disks belonging to Virtual Disk ==========|" & vbcr & vblf , True
  crt.Screen.Send "-------------------------------------------------------" & vbcr & vblf , True
  crt.Screen.Send " /opt/MegaRAID/storcli/storcli64 -LdPdInfo -aAll | egrep '^Adapter|^Number of Virtual|^Virtual Drive:|^Name|^Enclosure Device ID:|^Slot Number:|^Inquiry Data:|^Media Error Count:' | grep -v 'Adapter'" & vbcr
  crt.Screen.WaitForString chr(10)
  Do	
    result = crt.Screen.WaitForStrings( waitStrs )
    If result = 2 Then
        Exit Do
    End If
    szLineAbove = crt.Screen.Get(_
        crt.screen.CurrentRow - 1, _
        1, _
        crt.screen.CurrentRow - 1, _
        crt.Screen.Columns)
    file.Write szLineAbove & vbCrLf
  Loop	
  	MsgBox "File Location: " & strHomeFolder
crt.screen.synchronous = false
End Sub