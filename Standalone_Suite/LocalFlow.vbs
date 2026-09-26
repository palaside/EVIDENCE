' LocalFlow.vbs - Digital Evidence Desktop Executable Launcher (0 Window / Silent Native Experience)
Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")
strPath = FSO.GetParentFolderName(WScript.ScriptFullName)

' 1. Start Server & Autonomous Watcher Daemon completely hidden (WindowStyle 0 = No CMD Window)
WshShell.Run "cmd /c python """ & strPath & "\tools\data_server.py""", 0, False
WScript.Sleep 1200

' 2. Start Autonomous Watch & Slice Agent completely hidden
WshShell.Run "cmd /c python """ & strPath & "\tools\watch_and_slice.py""", 0, False
WScript.Sleep 800

' 3. Launch UI in Microsoft Edge App Mode (like a native desktop app with no address bar/distractions)
appUrl = "http://127.0.0.1:8088/PROJECT_EVIDENCE_3COL_PROTOTYPE.html"
edgePath = WshShell.ExpandEnvironmentStrings("%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe")

If FSO.FileExists(edgePath) Then
    WshShell.Run """" & edgePath & """ --app=" & appUrl & " --window-size=1600,960", 1, False
Else
    ' Fallback to default browser
    WshShell.Run appUrl, 1, False
End If

Set WshShell = Nothing
Set FSO = Nothing
