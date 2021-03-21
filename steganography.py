from getopt import getopt
from sys import argv, exit

from PIL import Image

"""
    TODO:
    -   ascii art, colors and status
    -   usage strganograpy [encrypt|decrypt] -i file [-d datafile] [-o file]
    -   add shebang
"""

EOF_length = 16

# check correct action
action = argv[1]
if action not in ['encrypt', 'decrypt']:
    print(f'Invalid action "{action}".')
    exit(1)

opts, args = getopt(argv[2:], "i:d:o:")


# check correct args
if (action == 'encrypt' and len(opts) < 2) or (action == 'decrypt' and len(opts) < 1):
    print(f'Usage: {argv[0]} [encrypt|decrypt] -i infile [-d datafile] [-o outfile]')
    exit(1)


# check for opt presence
infile = None
outfile = None
datafile = None
for opt in opts:
    if opt[0] == '-i':
        infile = opt[1]
    elif opt[0] == '-o':
        outfile = opt[1]
    elif opt[0] == '-d':
        datafile = opt[1]
    
if infile == None:
    print("Missing infile.")
    exit(1)
 

# encrypt
if action == 'encrypt':
    # check datafile presence
    if datafile == None:
        print("Missing datafile.")
        exit(1)

    # open files 
    img = Image.open(infile)
    out = Image.new("RGBA", img.size, 0xffffff)
    txt = open(datafile, "r").read()

    ######

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

    txt.close()
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
