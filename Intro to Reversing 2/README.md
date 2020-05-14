# Intro to Reversing 2

## Information
**Category**: Reverse Engineering    
**Difficulty**: Baby  
**Author:** 0x4d5a  
**Points:** Not known yet  
**Description:**
>This is a introductory challenge for beginners which are eager to learn reverse engineering on linux. The three stages of this challenge will increase in difficulty. But for a gentle introduction, we have you covered: Check out the video of LiveOverflow or follow the authors step by step guide to solve the first part of the challenge.
>
>Once you solved the challenge locally, grab your real flag at: nc hax1.allesctf.net 9601
>
>Note: Create a dummy flag file in the working directory of the rev1 challenge. The real flag will be provided on the server

## Overview

As attachment there is an ZIP file.
In this ZIP file there are two files:
>flag   
>rev2

The rev2 file is an ELF linux excecutable binary:   
```
rev2: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=6f10fffe1293cf3b8e79f2d2b7b27fa4cfd9b1b9, not stripped
```

## Solution
I opened the `rev2` executable in Ghidra.  
In the main function there is this pseudo code:
```c
[...]
  initialize_flag();
  puts("Give me your password: ");
  read_input = read(0,buffer_string,0x1f);
  buffer_string[(int)read_input + -1] = '\0';
  i = 0;
  while (i < (int)read_input + -1) {
    buffer_string[i] = buffer_string[i] + -0x77;
    i = i + 1;
  }
  iVar1 = strcmp(buffer_string,&DAT_00100ab0);
  if (iVar1 == 0) {
    puts("Thats the right password!");
    printf("Flag: %s",flagBuffer);
  }
  else {
    puts("Thats not the password!");
  }
[...]
```
There we can see that the programm reads the input and then remove 0x77 from every byte and compares it with "DAT_001000ab0" which is following::
```hex
fcfdeac0baece8fdfbbdf7beefb9fbf6bdc0bab9f7e8f2fde8f2fc00
```
So I built an simple (bad) Python code that does this in reverse, so add 0x77:  
(Note: I removed the null byte at the end)
```python
password = "fcfdeac0baece8fdfbbdf7beefb9fbf6bdc0bab9f7e8f2fde8f2fc"
out = password
for i in range(0, len(password), 2):
        a = int(password[i:i+2], 16) + 0x77
        b = hex(a % 256)[2:]
        out = out[:i] + b + out[i+2:]
print(bytes.fromhex(out).decode("ASCII"))
```
As result:   
`sta71c_tr4n5f0rm4710n_it_is`   
Submitting the Password:   
`nc hax1.allesctf.net 9601`
```
Give me your password:
sta71c_tr4n5f0rm4710n_it_is
Thats the right password!
Flag: CSCG{1s_th4t_wh4t_they_c4ll_on3way_transf0rmati0n?}
```
And there is the Flag:   
`CSCG{1s_th4t_wh4t_they_c4ll_on3way_transf0rmati0n?}`



