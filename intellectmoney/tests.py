# -*- coding:utf-8 -*-
from django import test
from django.core.urlresolvers import reverse
from django.test import Client

from intellectmoney import settings
from intellectmoney.forms import IntellectMoneyForm, ResultUrlForm
from intellectmoney.helpers import getHashOnReceiveResult, getHashOnHold
from intellectmoney.models import IntellectMoney
# Not avaliable in Django 1.3 yet
# from django.test.utils import override_settings


class IntellectMoneyTest(test.TestCase):

    def setUp(self):
        self.url = reverse('intellectmoney-result')
        self.client = Client(REMOTE_ADDR=settings.IP)
        self.data = {
            'serviceName': u'Тестовая оплата',
            'recipientAmount': '12222.32', 'recipientCurrency': 'RUR',
            'userName': '3434', 'email': 'test@example.com',
            'eshopId': settings.SHOPID, 'paymentId': '323',
            'secretKey': settings.SECRETKEY, 'orderId': '434000',
            'paymentStatus': 7, 'eshopAccount': '2212',
            'paymentData': '2011-01-01 01:01:01',
        }
        self.inv = IntellectMoney.objects.create(orderId='434000')

        self.data2 = { # from intellectmoney manual
            'eshopId': '17354',
            'orderId': 'order_0000001',
            'serviceName': u'Книга',
            'eshopAccount': '4356091274',
            'recipientAmount': '12.30',
            'recipientCurrency': 'RUB',
            'paymentStatus': '5',
            'userName': u'Артем Дворядкин',
            'userEmail': 'tema@intellectmoney.ru',
            'paymentData': '2010-01-17 13:12:03',
            'secretKey': 'myKey',
            'action': 'ToPaid'
        }
        self.valid_hash2 = '61620ea240928af649e44aaebb1c15dd'
        self.valid_holdhash2 = '8873d8442f5a9e1ad884114c15f11706'

    def tearDown(self):
        del self.data
        del self.inv

        del self.data2

    def testRequestForm(self):
        data = {
            'preference': 'bankCard', 'serviceName': u'Тестовый Платеж',
            'recipientAmount': '10000000.06', 'recipientCurrency': 'RUR',
            'userName': 'Test User Name', 'email': 'roman@netangels.ru',
            'orderId': 15, 'successUrl': '/dsdsd/', 'failUrl': '/dsdsda/',
            'eshopId': settings.SHOPID
        }
        form = IntellectMoneyForm(data)
        form.is_valid()
        self.assertTrue(form.is_valid())

    def testResultBadIp(self):
        client = Client(REMOTE_ADDR='992.993.994.995')
        response = client.post(self.url)
        self.assertEqual(response.status_code, 404)
        #self._assertTicketExists()

    # @override_settings(INTELLECTMONEY_SEND_SECRETKEY=False)
    def testResultBadShopId(self):
        settings.SEND_SECRETKEY = False
        data = self.data
        data['eshopId'] = '%s1' % settings.SHOPID
        data['hash'] = 1
        client = self.client
        response = client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        form = ResultUrlForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        self.assertTrue('eshopId' in form.errors)
        #self._assertTicketExists()

    # @override_settings(INTELLECTMONEY_SEND_SECRETKEY=False)
    def testResultBadHash(self):
        settings.SEND_SECRETKEY = False
        data = self.data
        hash = getHashOnReceiveResult(data)
        data['hash'] = hash + '343'
        client = self.client
        response = client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        form = ResultUrlForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue('__all__' in form.errors)
        self.assertTrue('hash' in unicode(form.errors['__all__']))
        #self._assertTicketExists()

        old_secretkey = settings.SECRETKEY
        settings.SECRETKEY = self.data2['secretKey']
        try:
            hash = getHashOnReceiveResult(self.data2)
        finally:
            settings.SECRETKEY = old_secretkey

        self.assertEqual(hash, self.valid_hash2)

    def testResultBadHoldHash(self):
        old_secretkey = settings.SECRETKEY
        settings.SECRETKEY = self.data2['secretKey']
        try:
            hash = getHashOnHold(self.data2)
        finally:
            settings.SECRETKEY = old_secretkey

        self.assertEqual(hash, self.valid_holdhash2)

    # @override_settings(INTELLECTMONEY_SEND_SECRETKEY=True)
    def testResultBadSecretKey(self):
        settings.SEND_SECRETKEY = True
        data = self.data
        data['secretKey'] = data['secretKey'] + '343'
        client = self.client
        response = client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        form = ResultUrlForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue('secretKey' in form.errors)
        #self._assertTicketExists()

    def testResultBadInvoiceDoesNotFound(self):
        data = self.data
        hash = getHashOnReceiveResult(data)
        data['hash'] = hash
        client = self.client
        response = client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        form = ResultUrlForm(data)
        self.assertTrue(form.is_valid())
        #TODO: Существование счетов
        #self.assertTrue(invoices.exists())
        #TODO: Существование платежей
        #self.assertTrue(payments.exists())
        #self._assertTicketExists()

    def testResultWithUnknownStatus(self):
        data = self.data
        data['paymentStatus'] = 4
        hash = getHashOnReceiveResult(data)
        data['hash'] = hash
        client = self.client
        response = client.post(self.url, data)
        form = ResultUrlForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 200)
        #TODO: Существование платежей
        #self.assertFalse(payments.exists())
        #self._assertTicketExists()

    def testResult(self):
        amount = '10.11'
        data = self.data
        data['orderId'] = self.inv.id
        hash = getHashOnReceiveResult(data)
        data['hash'] = hash
        client = self.client
        response = client.post(self.url, data)
        form = ResultUrlForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 200)
        orderId = data['orderId']
        recipientAmount = data['recipientAmount']
        #self.assertTrue(payments.exists())
        #payment = payments[0]
        #self.assertTrue(invoices.exists())

    def testResultAlreadyHavePaymentStatus(self):
        data = self.data
        data['orderId'] = self.inv.id
        hash = getHashOnReceiveResult(data)
        data['hash'] = hash
        client = self.client
        response = client.post(self.url, data)
        form = ResultUrlForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 200)
        #self.assertFalse(payments.exists())
        #self._assertTicketExists()

    def testResultBadFormData(self):
        data = self.data
        del data['eshopAccount']
        client = self.client
        response = client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        form = ResultUrlForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue('eshopAccount' in form.errors)
        #self._assertTicketExists()

