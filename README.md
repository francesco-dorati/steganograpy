
<h1 align="center">
  Steganography
  <br>
</h1>

<h4 align="center">A program to hide text messages inside images.</h4>

<p align="center">Steganography is the art of hiding a secret message within a normal message. This is used to transfer some secret message to another person; with this technique, no one else in between will know the secret message you wanted to convey.</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#algorithm">Algorithm</a> •
  <a href="#download">Download</a> •
  <a href="#files">Files</a> •
  <a href="#packages">Packages</a> •
  <a href="#license">License</a>
</p>

<img width="1130" alt="Schermata 2021-08-20 alle 23 30 13" src="https://user-images.githubusercontent.com/36961170/130329613-309cb960-f23b-4513-a2f0-b100e599bf77.png">


## Key Features

* **Hide text messages inside images**
  - Least Significat Bit (LSB) algorithm.
  - Hide messages inside the least significat bits of each pixel value.
* **Extract text messages from images**
* **Integrated encryption/decryption**
  - Text messages are encrypted/decrypted using SHA256.
* **Allow custom number of bits encoding**  
  - Default for LSB is 2.
* **Interactive mode**
* **Supports JPEG, PNG images**
* **Supports TXT files**
* **Lightweight and fast**


## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com) and [Python](https://www.python.org/downloads/) (which comes with [pip](https://pypi.org/project/pip/)) installed on your computer.  
From your command line:

```bash
# Clone this repository
$ git clone https://github.com/francesco-dorati/steganograpy.git

# Go into the repository
$ cd steganography

# Install dependencies
$ python3 -m pip install --upgrade -r requirements.txt

# Run the app
$ python3 main.py
```

## Algorithm
**Least Significat Bit** (LSB) algorithm is a steganographic algorithm that is able to conceal a message within an image **by modifying its least significant two-bits.**  
In the resulting image the pixel value will be formed by **6 bits for the image and 2 bits for the message.**

**Example:**  
*Message:* 01100101 -> 01 10 01 01  
*Image pixels:* 00100110 01101001 10010010 11100011

*Resulting image:* 001001(01) 011010(10) 100100(01) 111000(01)

Since only the least significat bits are modified, **the difference between the two images is imperceptible**.

## Download

You can [download](https://github.com/francesco-dorati/steganograpy/releases/tag/v2.0) the latest installable version of Steganography for Windows, macOS and Linux.

## Files
* `main.py`: entry file for the program. (front-end)
* `steganography.py`: file containing Steganography API. (back-end)
* `requirements.txt`: file containing the list of dependencies.

## Packages
This software uses the following open source packages:
* [Pillow](https://python-pillow.org/) for image manipulation.
* [Cryptography](https://pypi.org/project/cryptography/) for encryption.

## License

MIT
