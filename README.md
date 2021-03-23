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
1. transform user input into binary and add 16x`'0'` at the end
```python
 binary = list(''.join(format(ord(i), '08b') for i in txt) + '0' * EOF_length)
```
2. loop through the image
    1. get pixel colors
    2. modify pixel colors
    3. save updated pixel colors to outfile
```python
width, height = img.size
for x in range(width):
    for y in range(height):
        # get pixel colors
        if img.format == 'PNG':
            r, g, b, a = img.getpixel((x, y))
        else:
            r, g, b = img.getpixel((x, y))

        if binary:
            r = int(format(r, '010b')[:-2] + binary.pop(0) + binary.pop(0), 2)

        if binary:
            g = int(format(g, '010b')[-2:] + binary.pop(0) + binary.pop(0), 2)

        if binary:
            b = int(format(b, '010b')[-2:] + binary.pop(0) + binary.pop(0), 2)

        # put pixel on out image
        if img.format == 'PNG':
            out.putpixel((x, y), (r, g, b, a))
        else:
            out.putpixel((x, y), (r, g, b, 255))
```
3. write changes to outfile
```python
out.save(outfile if outfile else f'out.png')
```
#### Decrypt
1. loop through the image until 16x`'0'` found
    1. read least two significat bytes and save them into a variable
```python
width, height = img.size
for x in range(width):
    for y in range(height):
        # get pixel colors
        r, g, b, a = img.getpixel((x, y))

        binary += format(r, '010b')[-2:]
        if binary[-EOF_length:] == '0' * EOF_length:
            break

        binary += format(g, '010b')[-2:]
        if binary[-EOF_length:] == '0' * EOF_length:
            break

        binary += format(b, '010b')[-2:]
        if binary[-EOF_length:] == '0' * EOF_length:
            break

    if binary[-EOF_length:] == '0' * EOF_length:
        break
 
binary = binary[:-EOF_length]
```
2. transform binary into text
```python
num = int(binary, 2)
byte = num.bit_length() + 7 // 8
arr = num.to_bytes(byte, "big")
text = arr.decode()
```

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
