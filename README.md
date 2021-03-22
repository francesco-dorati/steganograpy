# Steganograpy
### Video demo: https://youtu.be/_u5dhcBEOY8
## Description:
__Steganography__ is the practice of concealing a message within another message or a physical object.
In computing/electronic contexts, a computer file, message, image, or video is concealed within another file, message, image, or video.

This program conceals a text message within an image using the __LSB algorithm__.

**Programming language**: Python 3.9
**Library for images**: Pillow (PIL)
**Library for terminal colors**: termcolors

### LSB Algorithm
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

### Process
Pseudocode for the process:
#### Encrypt
- transform user input into binary and add 16x`'0'` at the end
- loop through the image
  - get pixel colors
  - modify pixel colors
  - save updated pixel colors to outfile
- write changes to outfile
#### Decrypt
- loop through the image until 16x`'0'` found
  - read least two significat bytes and save them into a variable
- transform binary into text

### Usage

#### Encrypt
With a txt file:
```
steganograpy.py encrypt -i infile.png -f data.txt [-o outfile.png]
```
With a string:
```
steganograpy.py encrypt -i infile.png -m "Message Here." [-o outfile.png]
```
If no outfile specified, the outfile will be `out.png`

#### Decrypt
With a txt outfile:
```
steganograpy.py decrypt -i infile.png [-o outfile.txt]
```
Without outfile:
```
steganograpy.py decrypt -i infile.png
```

### Files
- `steganograpy`: main file
- `reqirements.txt`: reqirements
