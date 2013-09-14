# coding=utf-8

from django.db import models
from django.core import validators
from django.utils.six import with_metaclass, string_types

from .encrypt import decode, encode


class EncryptedAESField(with_metaclass(models.SubfieldBase, models.TextField)):
    def _is_encrypted(self, value):
        return value and isinstance(value, string_types) and \
            value.startswith('-----BEGIN')

    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return ''
        if not self._is_encrypted(value):
            return value
        return decode(value)

    def get_prep_value(self, value):
        if value in validators.EMPTY_VALUES:
            return ''
        if self._is_encrypted(value):
            return value
        return encode(value)
