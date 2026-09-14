Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
strCurrentDir = fso.GetParentFolderName(WScript.ScriptFullName)
strWatcher = strCurrentDir & "\tools\slip_hotfolder_watcher.py"

' Find pythonw.exe path
Dim strPythonw, userProfile
userProfile = WshShell.ExpandEnvironmentStrings("%USERPROFILE%")

If fso.FileExists(userProfile & "\miniconda3\pythonw.exe") Then
    strPythonw = """" & userProfile & "\miniconda3\pythonw.exe"""
ElseIf fso.FileExists(userProfile & "\anaconda3\pythonw.exe") Then
    strPythonw = """" & userProfile & "\anaconda3\pythonw.exe"""
ElseIf fso.FileExists(userProfile & "\AppData\Local\Programs\Python\Python311\pythonw.exe") Then
    strPythonw = """" & userProfile & "\AppData\Local\Programs\Python\Python311\pythonw.exe"""
ElseIf fso.FileExists(userProfile & "\AppData\Local\Programs\Python\Python310\pythonw.exe") Then
    strPythonw = """" & userProfile & "\AppData\Local\Programs\Python\Python310\pythonw.exe"""
ElseIf fso.FileExists("C:\Program Files\Python311\pythonw.exe") Then
    strPythonw = """C:\Program Files\Python311\pythonw.exe"""
Else
    strPythonw = "pythonw.exe"
End If

' Run pythonw silently with window mode 0 (hidden)
WshShell.CurrentDirectory = strCurrentDir
WshShell.Run strPythonw & " """ & strWatcher & """", 0, False
