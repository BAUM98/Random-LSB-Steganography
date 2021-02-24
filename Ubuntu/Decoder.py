import sys
import numpy as np
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512, SHA256
import binascii
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

class Decoder:
    def __init__(self, inputImage, outputDir, password = "password"):
        self.__stegoImage = Image.open(inputImage)
        self.__pixels = self.__stegoImage.load()
        self.__outputDir = outputDir
        self.__password = password
    
    def run(self):
        #Step 1: generate hashes
        self.__generateHash()
        #Step 2: Get first 10 bits to determine size
        self.__setup()
        self.__getSize()
        self.__getFileType()
        self.__getEntirePixelList()
        self.__getBytes()
        print("Decode Finished")

    def __generateHash(self):
        iterations = 200000
        #https://cryptobook.nakov.com/mac-and-key-derivation/pbkdf2
        salt = 'Steganography'
        key = PBKDF2(self.__password, salt, 64, count=iterations, hmac_hash_module=SHA256)
        self.__seed1 = binascii.hexlify(key)
        key = PBKDF2(key, salt, 64, count=iterations, hmac_hash_module=SHA512)
        self.__verification = binascii.hexlify(key)
        key = PBKDF2(self.__verification, salt, 64, count=iterations, hmac_hash_module=SHA256)
        self.__seed2 = binascii.hexlify(key)
    
    def __setup(self):
        self.__generateSizePixels()
        self.__generatePixelTracker()
        
    def __generateSizePixels(self):
        np.random.seed(int.from_bytes(self.__seed1, "big") % (2**32 - 1))
        width, height = self.__stegoImage.size
        self.__sizePixelList = []
        #List of pixel orders for every bit, 6 for size, 4 for file extension
        x = np.random.randint(0, width - 1, 80, np.uint64)
        np.random.seed(int.from_bytes(self.__seed2, "big") % (2**32 - 1))
        y = np.random.randint(0, height - 1, 80, np.uint64)
        self.__sizePixelList = np.vstack((x, y)).T

    def __generatePixelTracker(self):
        self.__pixelTracker = []
        width, height = self.__stegoImage.size
        for w in range(width):
            self.__pixelTracker.append([])
            for h in range(height):
                #Start off at 1, 1 = red, 2 = green, 3 = blue
                self.__pixelTracker[w].append(1) 

    def __getSize(self):
        self.__totalSize = 0
        #6 bytes for size of output file
        for bitIndex in range(48):
           pixel = self.__sizePixelList[bitIndex]
           self.__totalSize <<= 1
           self.__totalSize = self.__totalSize + self.__getNextBit(pixel) 
        

    def __getFileType(self):
        #4 bytes for output file extension
        fileBytes = bytearray([0] * 4)
        for bitIndex in range(48, 80):
            pixel = self.__sizePixelList[bitIndex]
            fileBytes[int((bitIndex - 48) / 8)] <<= 1
            fileBytes[int((bitIndex - 48) / 8)] += self.__getNextBit(pixel)
        self.__outputFileFormat = ""
        for fb in fileBytes:
            if fb == 0:
                break
            self.__outputFileFormat += chr(fb)



    def __getNextBit(self, pixel):
        trackerBit = self.__pixelTracker[pixel.item(0)][pixel.item(1)]
        colorOfInterest = (trackerBit - 1) % 3
        bitOfInterest = int((trackerBit) / 3)
        if self.__pixels[pixel.item(0), pixel.item(1)][colorOfInterest] & (2 ** bitOfInterest) == (2 ** bitOfInterest):
            self.__pixelTracker[pixel.item(0)][pixel.item(1)] += 1
            return 1
        self.__pixelTracker[pixel.item(0)][pixel.item(1)] += 1
        return 0

    def __getEntirePixelList(self):
        np.random.seed(int.from_bytes(self.__seed1, "big") % (2**32 - 1))
        width, height = self.__stegoImage.size
        self.__sizePixelList = []
        #List of pixel orders for every bit
        #for i in range(totalSize):
        #    self.pixelList.append([math.floor(random.random() * (width - 1)), math.floor(random.random() * (height - 1))])
        x = np.random.randint(0, width - 1, self.__totalSize + 80, np.uint64)
        np.random.seed(int.from_bytes(self.__seed2, "big") % (2**32 - 1))
        y = np.random.randint(0, height - 1, self.__totalSize + 80, np.uint64)
        self.__pixelList = np.vstack((x, y)).T

    def __getBytes(self):
        byteStream = bytearray([0] * (int((self.__totalSize - 80) / 8)))
        for bitIndex in range(80, self.__totalSize):
            pixel = self.__pixelList[bitIndex]
            byteStream[int((bitIndex - 80) / 8)] <<= 1
            byteStream[int((bitIndex - 80) / 8)] += self.__getNextBit(pixel)
        f = open(self.__outputDir + "/decoded." + self.__outputFileFormat, "wb")
        f.write(byteStream)
        f.close()

if __name__ == '__main__':
    e = Decoder(sys.argv[1], sys.argv[2])
    e.run()