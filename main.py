#!/usr/bin/python3

import sys
from getopt import getopt

from steganography import Steganography

def main():
    if len(sys.argv) < 2:
        print_help()
        exit(1)

    opts, _ = getopt(sys.argv[2:], "i:f:m:o:")

    action = sys.argv[1]
    if action not in ['encode', 'decode']:
        print_help()
        exit(1)

    # check for opt presence
    img_path = None
    message = None
    for opt in opts:
        if opt[0] == '-i':
            img_path = opt[1]

        elif opt[0] == '-f':
            with open(opt[1]) as file:
                message = file.read()

        elif opt[0] == '-m':
            message = opt[1]
    

    s = Steganography()

    if action == 'encode':    
        # text
        if not message:
            text = input('Text: ')
 
        outfile = s.encode(img_path, message)
        print(f'New file created: {outfile}')
        
    else:
        text = s.decode(img_path)
        print(f'Text: {text}')
    

def print_help():
    print("""
Steganography

    Usage:
        steganograpy encode [-i image] [-f textfile | -m message]
        steganograpy decode -i image
    """)

if __name__ == '__main__':
    main()



exit()
#####


from sys import argv, exit


from termcolor import colored

def main():
    EOF_length = 16

    if len(argv) < 2:
        print('Usage: {argv[0]} [encrypt|decrypt] -i infile [-f datafile | -m message] [-o outfile]')
        exit(1)

    # check correct action
    action = argv[1]
    if action not in ['encrypt', 'decrypt']:
        print(f'Invalid action "{action}".')
        exit(1)

    opts, args = getopt(argv[2:], "i:f:m:o:h")


    # check correct args
    if (action == 'encrypt' and len(opts) < 2) or (action == 'decrypt' and len(opts) < 1):
        print(f'Usage: {argv[0]} [encrypt|decrypt] -i infile [-f datafile|-m message] [-o outfile]')
        exit(1)


    # check for opt presence
    infile = None
    outfile = None
    datafile = None
    textdata = None
    for opt in opts:
        if opt[0] == '-i':
            infile = opt[1]
        elif opt[0] == '-o':
            outfile = opt[1]
        elif opt[0] == '-f':
            datafile = opt[1]
        elif opt[0] == '-m':
            textdata = opt[1]
        elif opt[0] == '-h':
            print(f'Usage: {argv[0]} [encrypt|decrypt] -i infile [-f datafile|-m message] [-o outfile]')
            exit(1)

    if infile == None:
        print("Missing infile.")
        exit(1)
 

    # encrypt
    if action == 'encrypt':
        # check data presence
        if not datafile and not textdata:
            print('Missing datafile/textdata.')
            exit(1)

        elif datafile and textdata:
            print('Too many arguments.')
            exit(1)

        # encrypting message 
        print(colored('Encrypting...', 'grey', attrs=['bold']))

        # open files 
        img = Image.open(infile)
        out = Image.new("RGBA", img.size, 0xffffff)

        # read data from file or input
        if datafile:
            with open(datafile, 'r') as file:
                txt = file.read()
        else:
            txt = textdata

        binary = list(''.join(format(ord(i), '08b') for i in txt) + '0' * EOF_length)


        # loop for every pixel
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

        # save outfile
        out.save(outfile if outfile else f'out.png')

        # close file
        img.close()
        out.close()

        # completed message
        print(colored('Text encrypted successfully!', 'green', attrs=['bold'])) 
        print(colored('Encrypted image is in ', attrs=['bold']) + colored(outfile if outfile else 'out.png', 'blue', attrs=['bold']))
    else:
        # check datafile presence
        if datafile != None:
            print('Datafile not necessary.')
            exit(1)

        # open files
        img = Image.open(infile)
        if outfile:
            out = open(outfile, "w")

        # check image format
        if img.format != 'PNG':
            print('Invalid image format.')
            exit(2)

        binary = ""

        # encrypting message 
        print(colored('Decrypting...', 'grey', attrs=['bold']))
        
        # loop for every pixel
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

        # binary to text
        num = int(binary, 2)
        byte = num.bit_length() + 7 // 8
        arr = num.to_bytes(byte, "big")
        text = arr.decode()

        # write to file
        if outfile:
            out.write(text.strip('\0'))
        
        # completed message
        print(colored('Text decrypted successfully!', 'green', attrs=['bold'])) 
        if outfile:
            print(colored('Decrypted message is in ', attrs=['bold']) + colored(outfile, 'blue', attrs=['bold']))
        else:
            print(colored('\nMessage:', attrs=['bold']))
            print(text)



if __name__ == '__main__':
    #main()
    s = Steganograpy()
    print(s.binary_to_text(s.text_to_binary('suca')))

