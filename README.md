# OSED

![image](https://github.com/user-attachments/assets/1964c089-4a89-457b-b370-cbed76354f11)

## Exploit Strategy

* If EIP controllable and DEP off: direct shellcode jump.
* If DEP on: plan ROP to call VirtualProtect/VirtualAlloc or find JIT/ret2libc equivalent.
* If ASLR present: find module without ASLR/rebase or use info leaks.
  
## Methodology

1. Crash the application
2. Controlling EIP
3. Locating space for BOF (350–400 bytes) (`dds esp+2c0 L4`)
    1. Increase buffer length (ex.: 800 -> 1500)
4. Checking bad chars
    1. `!py \\tsclient\local-share\srbx7_bads.py --generate -b 00`
    2. `!py \\tsclient\local-share\srbx7_bads.py --address esp --bad 00 --start 01 --end 7f`
       1. Debug: `Debug: `db esp-8 L100``
6. Redirecting execution flow
    1. `JMP ESP` (TIP: if application compiled with `DEP`, `JMP ESP` address must be in the `.text`)
        1. `msf-nasm_shell` > `jmp esp` > `FFE4`
        2. Confirm the opcode at the address: `u 10090c83` > `ffe4`
        3. Python: `eip = b"\x83\x0c\x09\x10"     #0x10090c83 - JMP ESP`
7. Generating shellcode
8. Getting the shellcode
9. Improving the exploit (not to crash the application)
    1. If multi-threaded application, add to msf-venom `EXITFUNC=thread`

## Links

* https://github.com/sebastian93921/OSED-Code-Snippets scripts for exploit phase
* https://github.com/bugzzzhunter/OSEDscripts/ windbg python automation
* https://github.com/epi052/osed-scripts?tab=readme-ov-file#install-monash install mona

> Automatically attach to process (ex.: `PROCESS_NAME` = `syncbrs`)

* `Set-ExecutionPolicy Bypass -Scope Process -Force`
* `while ($true) {\\tsclient\local-share\attach-process.ps1 -process-name syncbrs -commands '.load pykd.pyd; g;'}`
* `while ($true) {\\tsclient\local-share\attach-process.ps1 -path .\VulnApp1.exe -process-name VulnApp1 -commands '.load pykd.pyd; g;'}`

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

Mona: 
* `.load pykd.pyd`: load pykd
* `!py mona modules`: list modules
* `!py mona config -set workingfolder "c:\%p"`: set workingfolder
* `!py mona bytearray -b "\x00\x0a"`: generate a list of bad chars
  * `C:\Program Files\Windows Kits\10\Debuggers\bytearray.bin`: list location
  * `!py mona compare -f C:\Program Files\Windows Kits\10\Debuggers\bytearray.bin -a esp`: compare list with the stack starting at ESP
* `!py mona jmp -r esp -cpb '\x00'`: if lot of space (ex.: `inputBuffer += pack("<I",0x00418674) #00418674`)

  
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
