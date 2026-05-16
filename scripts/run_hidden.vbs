Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

If WScript.Arguments.Count = 0 Then
    WScript.Quit 2
End If

root = fso.GetParentFolderName(fso.GetParentFolderName(WScript.ScriptFullName))
target = WScript.Arguments(0)

If InStr(target, ":\") = 0 And Left(target, 2) <> "\\" Then
    target = root & "\" & target
End If

extra = ""
For i = 1 To WScript.Arguments.Count - 1
    extra = extra & " " & Chr(34) & WScript.Arguments(i) & Chr(34)
Next

ext = LCase(fso.GetExtensionName(target))
If ext = "ps1" Then
    cmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File " & Chr(34) & target & Chr(34) & extra
Else
    cmd = Chr(34) & target & Chr(34) & extra
End If

shell.CurrentDirectory = root
shell.Run cmd, 0, False
