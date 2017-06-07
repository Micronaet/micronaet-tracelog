rem Library:
Set wshShell = CreateObject("WScript.Shell")
Set objFSO=CreateObject("Scripting.FileSystemObject")
Set args = Wscript.Arguments

rem Variables:
Dim strOra, strSeparator, strUserName, strComputerName, strMode, strFilePath

rem Constant:
Const ForReading = 1, ForAppending = 8

rem Parameters:
strFilePath = "c:\micronaet\"
strSeparator = ";"
constAppending = 8 
constReading = 1
constWriting = 2

rem Passed parameters:
strMode = "err"
On Error Resume next
strMode = args(0)


rem Dynamic parameter:
strNow = Now()
strUserName = wshShell.ExpandEnvironmentStrings( "%USERNAME%" )
strComputerName = wshShell.ExpandEnvironmentStrings( "%COMPUTERNAME%" )
strLog = strUserName & strSeparator & strComputerName & strSeparator & strNow & strSeparator & strMode & vbCrLf

'If objFSO.FolderExists(strDirectory) Then
'   Set objFolder = objFSO.GetFolder(strDirectory)
'Else
'   Set objFolder = objFSO.CreateFolder(strDirectory)
'   WScript.Echo "Just created " & strDirectory
'End If

rem Write on file:
strFileName=strFilePath & strComputerName & ".log"
Set objFile = objFSO.OpenTextFile(strFileName,ForAppending,True)
objFile.Write strLog
objFile.Close
