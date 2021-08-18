class Steganography:
    try:
        from PIL import Image
    except ImportError:
        print('Missing packages, run `python3 -m pip install -r requirementes.txt`')
        exit(1)

    def __init__(self, eof=16, bits=2):

        self.EOF_LENGTH = eof
        self.BITS = bits

    def encode(self, img_path: str, text: str) -> str:
        out_name = 'out.png'

        img = self.Image.open(img_path)
        out = self.Image.new("RGBA", img.size, 0xffffff)

        binary = list(self.__to_binary(text) + ('0' * self.EOF_LENGTH))

        # loop for image pixels
        width, height = img.size
        for x in range(width):
            for y in range(height):
                # read pixel from image
                if img.format == 'PNG':
                    r, g, b, a = img.getpixel((x, y))
                else:
                    r, g, b = img.getpixel((x, y))

                # modify pixel value
                new_colors = []
                for color in (r, g, b):
                    if not binary:
                        new_colors.append(color)
                        continue

                    binary_color = bin(color)[:-self.BITS]
                    for _ in range(self.BITS):
                        if binary:
                            binary_color += binary.pop(0)
                        else:
                            binary_color += '0'

                    new_colors.append(int(binary_color, 2))

                # write pixel on out image
                if img.format == 'PNG':
                    out.putpixel((x, y), (*new_colors, a))
                else:
                    out.putpixel((x, y), (*new_colors, 255))


        # save new image
        out.save(out_name)

        # close images 
        img.close()
        out.close()

        return out_name


    def decode(self, img_path: str) -> str:
        binary = ''

        img = self.Image.open(img_path)

        # check image format
        if img.format != 'PNG':
            print('Invalid image format.')
            exit(1)
        
        # loop for image pixels
        width, height = img.size
        for x in range(width):
            for y in range(height):
                # get pixel colors
                r, g, b, _ = img.getpixel((x, y))

                # extract message from pixel colors
                for color in (r, g, b):
                    binary += format(color, '#010b')[-self.BITS:]
                    if binary[-self.EOF_LENGTH:] == ('0' * self.EOF_LENGTH):
                        break

                if binary[-self.EOF_LENGTH:] == ('0' * self.EOF_LENGTH):
                    break

            if binary[-self.EOF_LENGTH:] == ('0' * self.EOF_LENGTH):
                break

        return self.__to_text(binary[:-self.EOF_LENGTH])
        

    def __to_binary(self, text: str) -> str:
        binary = ''

        encoded_text = text.encode('utf-8')
        for word in encoded_text:
            byte = format(word, '#010b')[2:]

            if len(byte) != 8:
                byte = '0' * (8 - len(byte)) + byte

            binary += byte
        
        return binary

    def __to_text(self, binary: str) -> str:
        text = ''

        while binary:
            byte = binary[:8]
            char = chr(int(byte, 2))
            text += char

            binary = binary[8:]
        
        return text