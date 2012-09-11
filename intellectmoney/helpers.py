# -*- coding: utf-8 -*-
import hashlib

from intellectmoney import settings


def checkHashOnReceiveResult(data):
    hash = getHashOnReceiveResult(data)
    return hash == data.get('hash')


def checkHashOnHold(data):
    hash = getHashOnHold(data)
    return hash == data.get('hash')


def getHashOnKeys(data, *keys, **kwargs):
    secretKey = settings.SECRETKEY

    key = u'::'.join(unicode(data.get(key, '')) for key in keys)
    key = u'%s::%s' % (key, secretKey)

    encoding = kwargs.get('encoding', 'utf8')
    key = key.encode(encoding)

    return hashlib.md5(key).hexdigest()


def getHashOnReceiveResult(data):
    return getHashOnKeys(data,
                         'eshopId',
                         'orderId',
                         'serviceName',
                         'eshopAccount',
                         'recipientAmount',
                         'recipientCurrency',
                         'paymentStatus',
                         'userName',
                         'userEmail',
                         'paymentData',
                         encoding='cp1251'
                        )


def getHashOnRequest(data):
    return getHashOnKeys(data,
                         'eshopId',
                         'orderId',
                         'serviceName',
                         'recipientAmount',
                         'recipientCurrency',
                         encoding='cp1251'
                        )


def getHashOnHold(data):
    return getHashOnKeys(data,
                         'eshopId',
                         'orderId',
                         'action',
                         encoding='cp1251'
                        )
