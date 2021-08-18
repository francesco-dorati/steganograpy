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
