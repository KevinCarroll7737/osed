# OSED

![image](https://github.com/user-attachments/assets/1964c089-4a89-457b-b370-cbed76354f11)

## WinDBG

Commands: https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/commands

Basics:

* `g` : go (resumes execution after attaching)
* `bp <0xaddress>` : set breakpoint
* `t` : single step after bp
* `? <0xstart> - <0xend>` : check bytes between addresses
* `dd esp` : display dword esp
* `dc esp` : display char esp
* `dw esp L4` : display word esp + length 4
* `dt ntdll!_TEB` : display type of TEB aka dumping struct
*  `u <0xstart>` : unasm an address

Reverse:

* `0x10090c83` -> `\x83\x0c\x09\x10` : (un)converting hex to python for LE (AMD64 and x86)
* `dds esp+2c0 L4` : check if 0x2c0 bytes fit on the stack
* `db esp - 10 L20` : check bad chars
* `lm m libssp` : list loaded modules that match "libssp" (`u <0xstart>` : unasm an address)
* `s -b <0xstart> <0xend> 0xff 0xe4` : search bytes FFE4 aka JMP ESP in memory (__Make sure no bad chars in addresses return__)

## MSF

* `msf-pattern_create -l 800`
* `msf-pattern_offset -l 800 -q 41424344`
* `msf-nasm_shell`
```
nasm > jmp esp
00000000  FFE4              jmp esp
```
