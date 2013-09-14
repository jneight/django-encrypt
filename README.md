django-encrypt
==============

Add field with integrated AES encryption to Django


How to generate an AES key
--------------------------

(modify `secret` to your secret passphrase)

For 128-bit key:
```bash
openssl enc -aes-128-cbc -k secret -P -md sha1
```
For 192-bit key:
```bash
openssl enc -aes-192-cbc -k secret -P -md sha1
```
For 256-bit key:
```
openssl enc -aes-256-cbc -k secret -P -md sha1
```

Settings
---------

Add your AES key to `AES_SECRET_PASSWORD` at settings, example:

```
AES_SECRET_PASSWORD = 'AF616756C6E3C98ADA8A20624D5368E9'
```

Block size is also configurable, `AES_BLOCK_SIZE`, must be 16, 24 or 32

```
AES_BLOCK_SIZE = 32  # default is set to 32
```
