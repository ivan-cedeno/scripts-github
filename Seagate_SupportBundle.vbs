# $language = "VBScript"
# $interface = "1.0"


'Luis Lopez 2022
'To collect logs from seagate array
'Seagate_SupportBundle.vbs


  crt.Screen.Synchronous = True

sub Main

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

  Set fso = CreateObject("Scripting.FileSystemObject")
  tdArray = crt.Dialog.Prompt("Enter controler A or B Name:", "GSO Hardware", "DAMC0-X-XX", False)
	If tdArray = "" Then Exit Sub
  crt.Screen.Send " ssh manage@" & tdArray & VbCr
  crt.Screen.WaitForString "Password: "
  crt.Screen.Send "!manage" & VbCr
  crt.Screen.WaitForString "# "
  crt.Screen.Send "set cli-parameters pager disable" & VbCr
  crt.Screen.WaitForString "Success: "
  
  Dim filesys, newfolder
  set filesys=CreateObject("Scripting.FileSystemObject")
  If  Not filesys.FolderExists("C:\Temp\SeagateSB") Then
     newfolder = filesys.CreateFolder ("C:\Temp\SeagateSB")
  End If
  '###########################################
  crt.Session.Log False
  
  'saving our global setting
  strOrigLogFilename = crt.Session.Config.GetOption("Log Filename")
  
  strLogfile = "C:\Temp\SeagateSB\store-" & tdArray & strName & "-" & dtsvalue & ".log"
  crt.Session.LogFileName = strLogfile
  crt.Session.Log True
  crt.Screen.Send "show configuration" & vbCr
  crt.Screen.WaitForString "Success: "
  crt.Sleep 3000
  crt.Screen.Send  VbCr
  crt.Screen.Send "show events" & vbCr
  crt.Screen.WaitForString "Success: "
  crt.Sleep 3000
  crt.Screen.Send VbCr
  crt.Screen.Send "show provisioning" & vbCr
  crt.Screen.WaitForString "Success: "
  crt.Sleep 3000
  crt.Screen.Send VbCr
  crt.Screen.Send "show disk-statistics" & vbCr
  crt.Screen.WaitForString "Success: "
  crt.Sleep 3000
  crt.Screen.Send VbCr
  crt.Screen.Send "show mui" & vbCr
  crt.Screen.WaitForString "Success: ", 5
  crt.Sleep 3000
  crt.Screen.Send "show red" & vbCr
  crt.Screen.WaitForString "Success: "
  crt.Screen.Send "exit" & vbCr
  crt.Session.Log False
  crt.Screen.Synchronous = False
  'restoring our global setting
  crt.Session.Config.SetOption "Log Filename", strOrigLogFilename
  MsgBox "File Name and Location: " & strLogfile
  '#########################################
  nTimeout = 5
  Do While crt.Screen.WaitForString ("Press any key to continue ", nTimeout) & vbCr
  Loop
  crt.Session.Log False
	Exit Sub
End sub

