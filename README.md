# osed

## WinDBG

Commands: https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/commands

Basics:

* `? <0xstart> - <0xend>` (check bytes between addresses)
* `dd esp` (display dword esp)
* `dc esp` (display char esp)
* `dw esp L4` (display word esp + length 4)
* `dt ntdll!_TEB` (display type of TEB aka dumping struct)
* `lm m libssp`
* `s -b <0xstart> <0xend> 0xff 0xe4` (search bytes FFE4 aka JMP ESP in memory) (__Make sure no bad chars in addresses return__)

Reverse:

* `dds esp+2c0 L4` (check if 0x2c0 bytes fit on the stack)
* `db esp - 10 L20` (check bad chars)

## MSF

* `msf-pattern_create -l 800`
* `msf-pattern_offset -l 800 -q 41424344`
* `msf-nasm_shell`
```
nasm > jmp esp
00000000  FFE4              jmp esp
```
