#!/usr/bin/env python
import sys
from django.conf import settings


settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'test',
            'USER': '',
            'PASSWORD': '',
        }
    },
    INSTALLED_APPS=(
        'django_encrypt',
        'tests',
    ),
    USE_TZ=True,
    AES_SECRET_PASSWORD = 'AF616756C6E3C98ADA8A20624D5368E9',
)

from django.test.simple import DjangoTestSuiteRunner
test_runner = DjangoTestSuiteRunner(verbosity=1)

failures = test_runner.run_tests(['tests', ])
if failures:
    sys.exit(failures)
