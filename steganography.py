class Steganography:
    try:
        from PIL import Image
    except ImportError:
        print('Missing packages, run `python3 -m pip install --upgrade -r requirements.txt`')
        exit(1)

    def __init__(self, eof=16, bits=2):
        """Initalizes the Steganograpy object. 

        Args:
            eof (int, optional): the length of the leading zeroes of the hidden message. Defaults to 16.
            bits (int, optional): the number of bits used for the message. Defaults to 2.
        """
        self.EOF_LENGTH = eof
        self.BITS = bits

    def encode(self, img_path: str, text: str, password: str = None) -> str:
        """Hides text inside an image using LSB algorithm.

        Args:
            img_path (str): the path of the image.
            text (str): the text to be concealed.
            password (str, optional): the text encryption password. Defaults to None.

        Returns:
            out_name (str): the filename of the message containing image.
        """
        out_name = 'out.png'

        # load images
        img = self.Image.open(img_path)
        out = self.Image.new("RGBA", img.size, 0xffffff)

        # encrypt
        if password:
            text = self.__encrypt(text, password)

        # convert to binary
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


    def decode(self, img_path: str, password: str = None) -> str:
        """Extracts the hidden message from an image.

        Args:
            img_path (str): the path of the image containing the message.
            password (str, optional): the encryption password of the hidden message. Defaults to None.

        Returns:
            message (str): the hidden message.
        """
        binary = ''

        # load image
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

                    has_message_ended = binary[-self.EOF_LENGTH:] == ('0' * self.EOF_LENGTH) 
                    if has_message_ended:
                        break

                if has_message_ended:
                    break

            if has_message_ended:
                break
        
        # remove padding
        text = self.__to_text(binary[:-self.EOF_LENGTH])

        # decrypt
        if password:
            text = self.__decrypt(text, password)

        return text
        

    def __to_binary(self, text: str) -> str:
        """Converts text to binary.

        Args:
            text (str): the string to be converted.

        Returns:
            binary (str): the binary representation of the given string.
        """
        binary = ''

        encoded_text = text.encode()
        for word in encoded_text:
            binary += format(word, '#010b')[2:]
        
        return binary

    def __to_text(self, binary: str) -> str:
        """Converts a binary string to text.

        Args:
            binary (str): the binary string.

        Returns:
            text (str): the text represented by the binary string.
        """
        text = ''

        while binary:
            byte = binary[:8]
            char = chr(int(byte, 2))
            text += char

            binary = binary[8:]
        
        return text
    
    def __encrypt(self, text: str, password: str) -> str:
        """Encrypts the given string with a password using SHA256.

        Args:
            text (str): the string to be encrypted.
            password (str): the encryption password.

        Returns:
            encrypted_text (str): the string encrypted with the given password.
        """
        try:
            import base64
            from cryptography.fernet import Fernet
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        except ImportError:
            print('Missing packages, run `python3 -m pip install --upgrade -r requirements.txt`')
            exit(1)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'',
            iterations=100000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

        return Fernet(key).encrypt(text.encode()).decode()

    def __decrypt(self, encrypted_text: str, password: str) -> str:
        """Decrypts the given password encrypted string using SHA256.

        Args:
            encrypted_text (str): the encrypted string.
            password (str): the encryption password.

        Returns:
            text (str): the unencrypted string.

        """ 
        try:
            import base64
            from cryptography.fernet import Fernet
            from cryptography.fernet import InvalidToken
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        except ImportError:
            print('Missing packages, run `python3 -m pip install --upgrade -r requirements.txt`')
            exit(1)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'',
            iterations=100000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

        try:
            return Fernet(key).decrypt(encrypted_text.encode()).decode()
        except InvalidToken:
            print('Wrong password.')
            exit(1)


