# Intro to Stegano 1

## Information
**Category**: Stegano    
**Difficulty**: Baby  
**Author:** explo1t  
**Points:** Not known yet  
**Description:**
>This is an introductory challenge for the almighty steganography challenges. The three stages contain very different variants of hidden information. Find them!

## Overview

As challenge file there's one picture:
>chall.jpg
The picture is this:   

<img src="./chall.jpg" width="200" height="auto" alt="chall.jpg aka. CalmOverflow"/>

## Solution

I did exiftool to the File, it gives the following output:   
`exiftool chall.jpg`
```
ExifTool Version Number         : 11.16
File Name                       : chall.jpg
Directory                       : .
File Size                       : 172 kB
File Modification Date/Time     : 2020:03:31 21:01:42+02:00
File Access Date/Time           : 2020:05:28 22:01:57+02:00
File Inode Change Date/Time     : 2020:04:01 11:27:07+02:00
File Permissions                : rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : inches
X Resolution                    : 72
Y Resolution                    : 72
Comment                         : alm1ghty_st3g4n0_pls_g1v_fl4g
Image Width                     : 1024
Image Height                    : 1128
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:4:4 (1 1)
Image Size                      : 1024x1128
Megapixels                      : 1.2

```

There we see as comment `alm1ghty_st3g4n0_pls_g1v_fl4g`    
I tried to extract hidden files with stehide,    
as password i used the comment.   
`steghide extract -q -sf chall.jpg -xf flag -p alm1ghty_st3g4n0_pls_g1v_fl4g`  
This gives the file flag.  
In this file is this:   
`CSCG{Sup3r_s3cr3t_d4t4}`   
And that is the flag!

## Mitigation

Hiding data is only pseudo security. Also, you should not include the password in the same message