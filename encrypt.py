# coding=utf-8


from Crypto.Cipher import AES
from django.conf import settings
import base64

#AES_BLOCK_SIZE = 32
#AES_SECRET_PASSWORD = 'AF616756C6E3C98ADA8A20624D5368E9'

def _padding(text):
    """
        Add the needed chars to fill the block size,
        The chars added are the ASCII value of the number
        needed
    """
    num = settings.AES_BLOCK_SIZE - (len(text) % settings.AES_BLOCK_SIZE)
    return text + chr(num) * num

def _unpadding(text):
    if len(text) == 0:
        return text
    
    lastchar = text[:-1]
    if lastchar > settings.AES_BLOCK_SIZE: # no padding
        return text
    return text.rstrip(lastchar)


def encode(text, cipher = None):
    """
        Encode the text, adding the padding needed,
        if not cipher is set, uses AES encryption
    """
    if cipher is None:
        cipher = AES.new(settings.AES_SECRET_PASSWORD)
        
    return base64.b64encode(cipher.encrypt(_padding(text)))


def decode(text, cipher = None):
    if cipher is None:
        cipher = AES.new(settings.AES_SECRET_PASSWORD)
        
    try:
        return _unpadding(cipher.decrypt(base64.b64decode(text)))
    except:
        return text
