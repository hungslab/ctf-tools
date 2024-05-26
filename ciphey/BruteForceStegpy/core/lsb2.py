#!/usr/bin/env python4
# Module for processing images, audios and the least significant bits.

import os
import numpy
from PIL import Image
from . import crypt2

MAGIC_NUMBER = b'stegv3'

class HostElement:
    """ This class holds information about a host element. """
    def __init__(self, filename):
        self.fileDir = os.path.dirname(filename)
        self.filename = filename
        self.format = filename[-3:]
        self.header, self.data = self.get_file(filename)

    def read_message(self, encrypted_data, password):
        try:
            salt = bytes(encrypted_data[:16])
            msg = crypt2.decrypt_info(password, bytes(encrypted_data[16:]), salt)
        except Exception:
            return("Wrong password.")

        if not self.check_magic_number(msg):
            return("Wrong password.")

        msg_len = int.from_bytes(bytes(msg[6:10]), 'big')
        filename_len = int.from_bytes(bytes(msg[10:11]), 'big')

        start = filename_len + 11
        end = start + msg_len
        end_filename = filename_len + 11
        if (filename_len > 0):
            filename = '_' + bytes(msg[11:end_filename]).decode('utf-8')
        else:
            return bytes(msg[start:end]).decode('utf-8')

        with open(os.path.join(self.fileDir, filename), 'wb') as f:
            f.write(bytes(msg[start:end]))

        return f'File {filename} succesfully extracted from {self.filename}'
    

    def get_file(self, filename):
        ''' Returns data from file in a list with the header and raw data. '''
        if filename.lower().endswith('wav'):
            content = numpy.fromfile(filename, dtype=numpy.uint8)
            content = content[:10000], content[10000:]
        elif filename.lower().endswith('gif'):
            image = Image.open(filename)
            frames = []
            palettes = []
            try:
                while True:
                    frames.append(numpy.array(image))
                    palettes.append(image.getpalette())
                    image.seek(image.tell()+1)
            except EOFError:
                pass
            content = [palettes, image.info['duration']], numpy.asarray(frames)
        else:
            image = Image.open(filename)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            content = None, numpy.array(image)
        return content

    def decode_message(self):
        ''' Decodes the image numpy array into a byte array. '''
        self.data.shape = -1, # convert to 1D
        bits = 2 ** ((self.data[0] & 48) >> 4) # bits = 2 ^ (5th and 6th bits)    
        divisor = 8 // bits

        if(self.data.size % divisor != 0):
            self.data = numpy.resize(self.data, self.data.size + (divisor - self.data.size % divisor))
        
        msg = numpy.zeros(len(self.data) // divisor, dtype=numpy.uint8)
        
        for i in range(divisor):
            msg |= (self.data[i::divisor] & (2 ** bits - 1)) << bits*i
        
        return msg

    def check_magic_number(self, msg):
        # if bytes(msg[0:6]) != MAGIC_NUMBER:
        #     print(bytes(msg[:6]))
        #     print('ERROR! No encoded info found!')
        #     exit(-1)
        return bytes(msg[:6]) == MAGIC_NUMBER
        
if __name__ == '__main__':
    message = 'hello'.encode('utf-8')
    host = HostElement('gif.gif')
    host.insert_message(message, bits=4)
    host.save()

