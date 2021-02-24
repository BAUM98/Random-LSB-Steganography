import os
import sys
from PIL import Image
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512, SHA256
import binascii
import random
import math
import numpy as np
Image.MAX_IMAGE_PIXELS = None

class Encoder:
    def __init__(self, inputImage, message, outputDir, password = "password"):
        self.__inputImage = Image.open(inputImage)
        self.__imageType = inputImage[inputImage.rfind("."):]
        self.__inputImage.save(".\Temp\cover" + self.__imageType)
        self.__inputImage.close()
        self.__inputImage = Image.open(".\Temp\cover" + self.__imageType)
        self.__pixels = self.__inputImage.load()
        
        self.__message = message
        self.__outputDir = outputDir
        self.__password = password
        print(self.__password)
    
    def run(self):
        #Step 1: Generate password and verification key hashes
        self.__generateHash()
        self.__setup()
        self.__encodeBytes()
        self.__inputImage.save(self.__outputDir + "/encoded" + self.__imageType)
        os.system("del .\Temp\cover"  + self.__imageType)       
        print("Encode Finished")
        

    
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
        self.__generatePixelQueue()
        self.__generatePixelTracker()
        self.__encodeFileType()
        self.__readMessage()


    def __generatePixelQueue(self):
        np.random.seed(int.from_bytes(self.__seed1, "big") % (2**32 - 1))
        # total size in bits of encrypted and compressed file, 
        # + 80 for file size (calculating how many pixels to edit) and fileType (for easier decoding)
        # max of like 1TB, BIG file
        self.__totalSize = (os.path.getsize(self.__message) * 8) + 80
        self.__startBytes = bytearray((self.__totalSize & 2**48 - 1).to_bytes(6, byteorder="big"))
        width, height = self.__inputImage.size
        self.__pixelList = []
        #List of pixel orders for every bit
        x = np.random.randint(0, width - 1, self.__totalSize + 80, np.uint64)
        np.random.seed(int.from_bytes(self.__seed2, "big") % (2**32 - 1))
        y = np.random.randint(0, height - 1, self.__totalSize + 80, np.uint64)
        self.__pixelList = np.vstack((x, y)).T
    
    def __encodeFileType(self):
        self.__fileType = bytearray(list(self.__message[self.__message.rfind(".") + 1:].encode('utf-8')))
        for i in range(4 - len(self.__fileType)):
            self.__fileType.append(0)
    
    def __readMessage(self):
        with open(self.__message, "rb") as f:
            self.__messageBytes = f.read()
        
        self.__messageBytes = self.__startBytes + self.__fileType + self.__messageBytes
 
    def __generatePixelTracker(self):
        self.__pixelTracker = []
        width, height = self.__inputImage.size
        for w in range(width):
            self.__pixelTracker.append([])
            for h in range(height):
                #Start off at 1, 1 = red, 2 = green, 3 = blue
                self.__pixelTracker[w].append(1)     

    def __encodeBytes(self):
        for bitIndex in range(self.__totalSize):
            self.Print = False
            self.test = bitIndex
            byte = self.__messageBytes[int(bitIndex / 8)]
            pixel = self.__pixelList[bitIndex]
            bit = byte & (2**(7 - (bitIndex % 8)))
            if bit != 0:
                bit = 1
            self.__encodeBit(pixel, bit)
        


    def __encodeBit(self, pixel, bit):
        trackerBit = self.__pixelTracker[pixel.item(0)][pixel.item(1)]
        self.printMask = False
        RGBChange = (trackerBit - 1) % 3
        t = (0, 0, 0)
        if RGBChange == 0:
            t = (self.__set_bit(self.__pixels[pixel.item(0), pixel.item(1)][0], int(trackerBit / 3), bit), self.__pixels[pixel.item(0), pixel.item(1)][1], self.__pixels[pixel.item(0), pixel.item(1)][2])
        elif RGBChange == 1:
            t = (self.__pixels[pixel.item(0), pixel.item(1)][0], self.__set_bit(self.__pixels[pixel.item(0), pixel.item(1)][1], int(trackerBit / 3), bit), self.__pixels[pixel.item(0), pixel.item(1)][2])
        else:
            t = (self.__pixels[pixel.item(0), pixel.item(1)][0], self.__pixels[pixel.item(0), pixel.item(1)][1], self.__set_bit(self.__pixels[pixel.item(0), pixel.item(1)][2], int(trackerBit / 3), bit))
        
        self.__pixels[pixel.item(0), pixel.item(1)] = t
        self.__pixelTracker[pixel.item(0)][pixel.item(1)] += 1
            

    # Copied from https://stackoverflow.com/questions/12173774/how-to-modify-bits-in-an-integer
    def __set_bit(self, v, index, x):
        """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
        mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
        v &= ~mask          # Clear the bit indicated by the mask (if x is False)
        if x:
            v |= mask         # If x was True, set the bit indicated by the mask.
        return v