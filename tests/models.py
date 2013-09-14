# coding=utf-8

from django.db import models
from django_encrypt.fields import EncryptedAESField


class TestModel(models.Model):
    data = EncryptedAESField(blank='')
