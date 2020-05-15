# Intro to Reversing 3

## Information
**Category**: Reverse Engineering    
**Difficulty**: Baby  
**Author:** 0x4d5a  
**Points:** Not known yet  
**Description:**
>This is a introductory challenge for beginners which are eager to learn reverse engineering on linux. The three stages of this challenge will increase in difficulty. But for a gentle introduction, we have you covered: Check out the video of LiveOverflow or follow the authors step by step guide to solve the first part of the challenge.
>
>Once you solved the challenge locally, grab your real flag at: nc hax1.allesctf.net 9602
>
>Note: Create a dummy flag file in the working directory of the rev1 challenge. The real flag will be provided on the server

## Overview

As attachment there is an ZIP file.
In this ZIP file there are two files:
>flag   
>rev3

The `rev3` file is an ELF linux non stripped excecutable binary:   
```
rev3: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=7fc813b97129ba8e754158292465a8e3dca5b05e, not stripped
```

## Solution
I opened the `rev3` executable in Ghidra.  
In the main function there is this pseudo code:
```c
[...]
  initialize_flag();
  puts("Give me your password: ");
  input = read(0,passwort,0x1f);
  passwort[(int)input + -1] = 0;
  i = 0;
  while (i < (int)input + -1) {
    passwort[i] = passwort[i] ^ (char)i + 10U;
    passwort[i] = passwort[i] - 2;
    i = i + 1;
  }
  iVar1 = strcmp((char *)passwort,"lp`7a<qLw\x1ekHopt(f-f*,o}V\x0f\x15J"); 
  if (iVar1 == 0) {
    puts("Thats the right password!");
    printf("Flag: %s",flagBuffer);
  }
  else {
    puts("Thats not the password!");
  }
[...]
```
There we can see that the programm reads the input.   
And then it XOR each byte with the count of the letter plus 10 and removes 2.   
This string gets compared with the following hexstring:   

```
6c706037613c714c771e6b486f707428662d662a2c6f7d560f154a00
```
So I need an program which first add 2 to the string and then xor this with i + 10

So I built an Python code that does this:   
(Note: I removed the null byte at the end)
```python
password = "6c706037613c714c771e6b486f707428662d662a2c6f7d560f154a"
out = password
for i in range(0, len(password), 2):
        a = int(password[i:i+2], 16) + 2
        b = int(i / 2) + 10
        c = a ^ b
        out = out[:i] + hex(c)[2:] + out[i+2:]
print(bytes.fromhex(out).decode("ASCII"))
```
As result:   
`dyn4m1c_k3y_gen3r4t10n_y34h`   
Submitting the Password:   
`nc hax1.allesctf.net 9602`
```
Give me your password:
dyn4m1c_k3y_gen3r4t10n_y34h
Thats the right password!
Flag: CSCG{pass_1_g3ts_a_x0r_p4ss_2_g3ts_a_x0r_EVERYBODY_GETS_A_X0R}
```
And there is the Flag:   
`CSCG{pass_1_g3ts_a_x0r_p4ss_2_g3ts_a_x0r_EVERYBODY_GETS_A_X0R}`

# Mitigation

To prevent the password from being read out so easily, you could use a hashing procedure or other procedures which are not reversible.   
In addition, you should distribute your binary without debugging symbols, since this makes reverse engineering easier