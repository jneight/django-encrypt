# coding=utf-8

# armor and dearmor code modifiedfrom django-pgcrypto:
# https://bitbucket.org/dcwatson/django-pgcrypto


import base64
import struct
import re

from Crypto.Cipher import AES
from django.conf import settings

CRC24_INIT = 0xB704CE
CRC24_POLY = 0x1864CFB

AES_BLOCK_SIZE = getattr(settings, 'AES_BLOCK_SIZE', 32)


def _padding(text):
    """
        Add the needed chars to fill the block size,
        The chars added are the ASCII value of the number
        needed
    """
    num = AES_BLOCK_SIZE - (len(text) % AES_BLOCK_SIZE)
    return text + chr(num) * num


def _unpadding(text):
    if len(text) == 0:
        return text
    lastchar = ord(text[-1])
    if lastchar > AES_BLOCK_SIZE: # no padding
        return text
    return text.rstrip(chr(lastchar))


def encode(text, cipher = None):
    """
        Encode the text, adding the padding needed,
        if not cipher is set, uses AES encryption
    """
    if cipher is None:
        cipher = AES.new(settings.AES_SECRET_PASSWORD)
    return armor(base64.b64encode(cipher.encrypt(_padding(text))))


def decode(text, cipher = None):
    if cipher is None:
        cipher = AES.new(settings.AES_SECRET_PASSWORD)
    return _unpadding(cipher.decrypt(base64.b64decode(dearmor(text))))

def crc24( data ):
    crc = CRC24_INIT
    for byte in data:
        crc ^= (ord(byte) << 16)
        for i in range(8):
            crc <<= 1
            if crc & 0x1000000:
                crc ^= CRC24_POLY
    return crc & 0xFFFFFF


def armor( data ):
    """
        Returns a string in ASCII Armor format, for the given binary data. The
        output of this is compatiple with pgcrypto's armor/dearmor functions.
    """
    template = '-----BEGIN PGP MESSAGE-----\n%(headers)s\n\n%(body)s\n=%(crc)s\n-----END PGP MESSAGE-----'
    headers = ['Version: django-encrypt 1.0']
    body = base64.b64encode( data )
    # The 24-bit CRC should be in big-endian, strip off the first byte (it's already masked in crc24).
    crc = base64.b64encode(struct.pack('>L', crc24(data))[1:])
    return template % {
        'headers': '\n'.join(headers),
        'body': body,
        'crc': crc
    }


class BadChecksumError (Exception):
    pass


def dearmor( text, verify=True ):
    """
    Given a string in ASCII Armor format, returns the decoded binary data.
    If verify=True (the default), the CRC is decoded and checked against that
    of the decoded data, otherwise it is ignored. If the checksum does not
    match, a BadChecksumError exception is raised.
    """
    check_data = None
    if verify:
        check_data = re.search('(?<=^=)\w+', text, re.MULTILINE).group(0)

    # decode data removing armor text
    data = base64.b64decode(
        re.search('(?<=\n\n)\w+[=](?=\n=)', text,).group(0))

    if verify and check_data:
        # The 24-bit CRC is in big-endian,
        # so we add a null byte to the beginning.
        crc = struct.unpack(
            '>L', '\0'+base64.b64decode(check_data))[0]
        if crc != crc24(data):
            raise BadChecksumError()
    return data

