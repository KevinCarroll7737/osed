# osed

## WinDBG

Commands: https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/commands

* dd esp (display dword esp)
* dc esp (display char esp)
* dw esp L4 (display word esp + length 4)
* dt ntdll!_TEB (display type of TEB aka dumping struct)

## MSF
* msf-pattern_create -l 800
* msf-pattern_offset -l 800 -q 41424344
