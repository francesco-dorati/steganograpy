from getopt import getopt
from sys import argv, exit

from PIL import Image

opt, args = getopt(argv[1:], "e:d")

end_length = 16

if len(opt) != 1 or len(args) != 1:
    print(f"Usage: {argv[0]} [-e txtfile | -d] <filename>")
    exit(1)

if opt[0][0] == "-e":
    img = Image.open(args[0])
    out = Image.new("RGBA", img.size, 0xffffff)

    txt = open(opt[0][1], "r").read()

    binary = list(''.join(format(ord(i), '08b') for i in txt) + '0' * end_length)

    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b, a = img.getpixel((x, y))

            if binary:
                r = int(bin(r)[:-2] + binary.pop(0) + binary.pop(0), 2)

            if binary:
                g = int(bin(g)[:-2] + binary.pop(0) + binary.pop(0), 2)

            if binary:
                b = int(bin(b)[:-2] + binary.pop(0) + binary.pop(0), 2)

            out.putpixel((x, y), (r, g, b, a))

    out.save('out.png')
    
    print("Done!")
else:
    img = Image.open(args[0])
    out = open("out.txt", "w")

    binary = ""

    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b, a = img.getpixel((x, y))

            binary += bin(r)[-2:]
            if binary[-end_length:] == '0' * end_length:
                break

            binary += bin(g)[-2:]
            if binary[-end_length:] == '0' * end_length:
                break

            binary += bin(b)[-2:]
            if binary[-end_length:] == '0' * end_length:
                break

        if binary[-end_length:] == '0' * end_length:
            break

    binary = binary[:-end_length]

    num = int(binary, 2)
    byte = num.bit_length() + 7 // 8
    arr = num.to_bytes(byte, "big")
    text = arr.decode()

    out.write(text)

    print("Done!")
