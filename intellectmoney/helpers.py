#coding:utf-8
from django.conf import settings
import hashlib


def cheskHashOnReceiveResult(data):
    hash = getHashOnReceiveResult(data)
    if hash == data.get('hash'):
        return True
    return False


def getHashOnReceiveResult(data):
    secretKey = getSecretKey()
    serviceName = data.get('serviceName', '')
    eshopId = data.get('eshopId')
    orderId = data.get('orderId')
    eshopAccount = data.get('eshopAccount')
    recipientAmount = data.get('recipientAmount')
    recipientCurrency = data.get('recipientCurrency')
    paymentStatus = data.get('paymentStatus')
    userName = data.get('userName')
    email = data.get('email')
    paymentData = data.get('paymentData')
    key = '%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s' % (
         eshopId, orderId, serviceName, eshopAccount, recipientAmount,
         recipientCurrency, paymentStatus, userName, email, paymentData,
         secretKey,
    )
    key = key.encode('windows-1251')
    hash = hashlib.md5(key).hexdigest()
    return hash


def getHashOnRequest(data):
    secretKey = getSecretKey()
    serviceName = data.get('serviceName', '')
    eshopId = data.get('eshopId')
    orderId = data.get('orderId')
    purchaseAmount = data.get('recipientAmount')
    currency = data.get('recipientCurrency')
    key = '%s::%s::%s::%s::%s::%s' % (
         eshopId, orderId, serviceName, purchaseAmount, currency, secretKey,
    )
    key = key.encode('windows-1251')
    hash = hashlib.md5(key).hexdigest()
    return hash

def getSecretKey():
    if settings.INTELLECTMONEY_SEND_SECRETKEY:
        return settings.INTELLECTMONEY_SECRETKEY
    return ''