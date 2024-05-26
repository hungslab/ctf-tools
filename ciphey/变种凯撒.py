import base64
from string import *
str1 = 'yD9oB3Inv3YAB19YynIuJnUaAGB0um0='
string1 = 'ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba0123456789+/'
string2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
enc_flag = str1.translate(str.maketrans(string1, string2))
print(enc_flag)
