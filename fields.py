# coding=utf-8


import base64

from django.db import models
from django.core import validators

import encrypt


class EncryptedAESField(models.Field):
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return 'TextField'

    def _is_encrypted(self, value):
        return isinstance(value, basestring) and value.startswith('-----BEGIN')

    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return ''

        if not self._is_encrypted(value):
            return value
        return encrypt.decode(value)

    def get_prep_value(self, value):
        if value in validators.EMPTY_VALUES:
            return ''
        if self._is_encrypted(value):
            return value
        return encrypt.encode(value)
