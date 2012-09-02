# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.functional import lazy

from django.contrib.sites.models import get_current_site

URL = getattr(settings, 'INTELLECTMONEY_URL',
              'https://merchant.intellectmoney.ru/ru/')
IP = getattr(settings, 'INTELLECTMONEY_IP', '91.212.151.242')

SHOPID = getattr(settings, 'INTELLECTMONEY_SHOPID', None)
SECRETKEY = getattr(settings, 'INTELLECTMONEY_SECRETKEY', None)

DEBUG = getattr(settings, 'INTELLECTMONEY_DEBUG', True)
UNIQUE_ID = getattr(settings, 'INTELLECTMONEY_UNIQUE_ID', False)
REQUIRE_HASH = getattr(settings, 'INTELLECTMONEY_REQUIRE_HASH', False)
SEND_SECRETKEY = getattr(settings, 'INTELLECTMONEY_SEND_SECRETKEY', False)
HOLD_MODE = getattr(settings, 'INTELLECTMONEY_HOLD_MODE', False)
EXPIRE_DATE_OFFSET = getattr(settings, 'INTELLECTMONEY_EXPIRE_DATE_OFFSET',
                             datetime.timedelta(days=7)
                            )

def get_url(name):
    return 'http://%s%s' % (
               get_current_site(request=None), reverse(name)
           )

SUCCESS_URL = getattr(settings, 'INTELLECTMONEY_SUCCESS_URL',
                      lazy(lambda: get_url('intellectmoney-success'), str),
                     )
FAIL_URL = getattr(settings, 'INTELLECTMONEY_FAIL_URL',
                   lazy(lambda: get_url('intellectmoney-fail'), str)
                  )
