# Labs

## exploiting-stack-overflows

The first Cs from our buffer landed between EIP and ESP.

> `dds esp -10 L8`

<img style="margin-left: 20px;" width="1280" height="747" alt="VirtualBoxVM_vloUex5UQl" src="https://github.com/user-attachments/assets/5587fc62-d42a-47ec-a886-1c38825da6c2" />

Just adding an offset of Cs to calculate the shellcode length (Ds)

* <img width="1123" height="296" alt="VirtualBoxVM_RSKUQ1txBE" src="https://github.com/user-attachments/assets/ae802a47-36ce-4598-84ac-59ead82e204b" />

* <img width="2544" height="652" alt="image" src="https://github.com/user-attachments/assets/4b511429-b302-44da-8cdd-471580528989" />

Check if there's enough space for a shellcode

> `dds esp+2c0 L4`

> `? 01cb7720 - esp`

* <img width="1277" height="439" alt="VirtualBoxVM_0BxZsYkiBF" src="https://github.com/user-attachments/assets/b025d398-28b1-438a-a89c-22e1a5190014" />
