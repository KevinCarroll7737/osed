# osed

## WinDBG

Commands: https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/commands

Basics:

* ? address_1 - address_2 (check bytes between addresses)
* dd esp (display dword esp)
* dc esp (display char esp)
* dw esp L4 (display word esp + length 4)
* dt ntdll!_TEB (display type of TEB aka dumping struct)

Reverse:

* dds esp+2c0 L4 (check if 0x2c0 bytes fit on the stack)
* db esp - 10 L20 (check bad chars)

## MSF

* msf-pattern_create -l 800
* msf-pattern_offset -l 800 -q 41424344
