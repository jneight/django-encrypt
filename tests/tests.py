# coding=utf-8


from django.utils.unittest import TestCase

from .models import TestModel


class EncryptTest(TestCase):
    def setUp(self):
        # AES key can be changed at runtests.py
        self.text = u'test data'
        # encrypted using test key at runtests.py
        self.text_encrypted = u'-----BEGIN PGP MESSAGE-----' \
            '\nVersion: django-encrypt 1.0\n\n' \
            'M1dEUHY3cHpwMTcyd05RNFZnbW5VM25HQTlQY3o3cUpSNU5XaDNpVWpCUT0=\n' \
            '=WmeC\n-----END PGP MESSAGE-----'

    def test_initialization(self):
        obj = TestModel.objects.create()
        self.assertEquals(obj.data, '')

    def test_model_save(self):
        obj = TestModel.objects.create(data=self.text)
        self.assertEquals(obj.data, self.text)

        # test text is saved encrypted in query
        self.assertEquals(
            self.text_encrypted,
            TestModel.objects.filter(
                pk=obj.pk).values_list(u'data', flat=True)[0])

        # test text is decrypted after query
        obj = TestModel.objects.get(pk=obj.pk)
        self.assertEquals(obj.data, self.text)

    def test_read_no_encrypted(self):
        obj = TestModel.objects.create()
        TestModel.objects.filter(pk=obj.pk).update(data=u'no encrypted')

        obj = TestModel.objects.get(pk=obj.pk)
        self.assertEquals(obj.data, u'no encrypted')

        # calling save will encrypt the text
        obj.save()
        obj = TestModel.objects.get(pk=obj.pk)
        self.assertFalse(TestModel.objects.filter(
            pk=obj.pk).values_list(u'data', flat=True)[0] == u'no encrypted')

