# coding=utf-8


import encrypt
from django.db import models
import base64


class EncryptedAESField(models.Field):
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return 'TextField'

    def _is_encrypted(self, value):
        # FIXME : no reconoce cadena cifrada
        if value == '':
            return False
        try:
            return isinstance(value, basestring) and base64.b64decode(value).startswith('-----BEGIN')
        except:
            return False

    def to_python(self, value):
        if value == '':
            return ''

        return encrypt.decode(value)

    def get_prep_value(self, value):
        if value == '':
            return value
        return encrypt.encode(value)
