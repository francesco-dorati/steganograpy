# Steganograpy
#### Video demo: https://youtu.be/_u5dhcBEOY8

__Steganography__ is the practice of concealing a message within another message or a physical object.  
In computing/electronic contexts, a computer file, message, image, or video is concealed within another file, message, image, or video.

This program conceals a text message within an image using the __LSB algorithm__.

## LSB Algorithm
Least Significat Bit (LSB) Algorithm is a steganographic algorithm that is able to conceal a message within an image by modifying its least significant two-bits.
In the resulting image the pixel value will be formed by 6 bits for the image and 2 bits for the message.

Example:
Message:  
01100101  
  
Image pixels:   
00100110 01101001 10010010 11100011  
  
Resulting image:  
001001(01) 011010(10) 100100(01) 111000(01)  

Since only the least significat bits are modified, the diffference between the two images is imperceptible.

## Usage

### Encrypt
With a txt file:
```
steganograpy.py encrypt -i infile.png -f data.txt [-o outfile.png]
```
With a string:
```
steganograpy.py encrypt -i infile.png -m "Message Here." [-o outfile.png]
```
### Decrypt
With a txt outfile:
```
steganograpy.py decrypt -i infile.png [-o outfile.txt]
```
Without outfile:
```
steganograpy.py decrypt -i infile.png
```
