# -*- coding: utf-8 -*-
import datetime

from django import forms

from intellectmoney import settings
from intellectmoney.helpers import checkHashOnReceiveResult, getHashOnRequest


class _BaseForm(forms.Form):

    eshopId = forms.CharField(initial=settings.SHOPID)
    orderId = forms.CharField(max_length=50)

    def clean_eshopId(self):
        eshopId = self.cleaned_data['eshopId']
        if eshopId != settings.SHOPID:
            raise forms.ValidationError(u'Неверный eshopId')
        return eshopId


class _BasePaymentForm(_BaseForm):

    CURRENCY_CHOICES = map(lambda x: (x, x), ['RUR', 'TST', 'RUB'])
    serviceName = forms.CharField(label=u'Payment Description', required=False)
    recipientAmount = forms.DecimalField(max_digits=10, decimal_places=2)
    recipientCurrency = forms.ChoiceField(
        choices=CURRENCY_CHOICES,
        initial=settings.DEBUG and 'TST' or 'RUB'
    )
    userName = forms.CharField(max_length=255, required=False)
    userEmail = forms.EmailField(required=False)


class IntellectMoneyForm(_BasePaymentForm):
    """Payment request form."""

    PREFERENCE_CHOICES = [
        # common
        ('inner', 'IntellectMoney'),
        ('bankCard', 'Visa/MasterCard'),
        ('exchangers', u'Internet Exchangers'),
        ('terminals', u'Terminals'),
        ('transfers', u'Transfers'),
        ('sms', 'SMS'),
        ('bank', u'Bank'),

        # exchangers
        ('telemoney', 'Telemoney'),
        ('rbkmoney', 'RBKMoney'),
        ('yandex', u'Яндекс.деньги'),
        ('moneymail', u'MoneyMail'),
        ('walet', u'Единый кошелек'),
        ('easypay', u'EasyPay'),
        ('liqpay', u'LiqPay'),
        ('zpayment', u'Zpayment'),
        ('qiwipurse', u'QIWI Кошелек'),
        ('vkontaktebank', u'В Контакте'),
        ('mailru', u'Деньги@Mail.Ru'),
        ('amegaeko', u'Единая Кнопка Оплаты'),
        ('mobimoney', u'С баланса телефона'),
        ('rapida', u'В салонах связи'),
        ('alfaclick', u'AlfaClick'),

        # groups
        ('inner,bankCard,exchangers,terminals,bank,transfers,sms', u'All'),
        ('bankCard,exchangers,terminals,bank,transfers,sms', u'All without inner'),
    ]

    successUrl = forms.CharField(
        required=False, max_length=512,
        initial=settings.SUCCESS_URL
    )
    failUrl = forms.CharField(
        required=False, max_length=512,
        initial=settings.FAIL_URL
    )
    preference = forms.ChoiceField(
        label=u'Payment Method', choices=PREFERENCE_CHOICES, required=False
    )
    expireDate = forms.DateTimeField(required=False)
    holdMode = forms.BooleanField(required=False,
                                  initial=settings.HOLD_MODE)
    hash = forms.CharField(required=settings.REQUIRE_HASH)

    def __init__(self, *args, **kwargs):
        initial = kwargs.setdefault('initial', {})
        if settings.REQUIRE_HASH:
            initial['hash'] = getHashOnRequest(initial)
        if settings.HOLD_MODE:
            exp_date = datetime.datetime.now() + settings.EXPIRE_DATE_OFFSET
            initial['expireDate'] = exp_date

        super(IntellectMoneyForm, self).__init__(*args, **kwargs)


class ResultUrlForm(_BasePaymentForm):

    STATUS_CHOICES = [
        (3, u'Создан счет к оплате (СКО) за покупку'),
        (4, u'СКО аннулирован, деньги возвращены пользователю'),
        (7, u'СКО частично оплачен'),
        (5, u'СКО полностью оплачен'),
        (6, u'Cумма заблокирована на СКО, ожидается запрос на списание'),
    ]

    paymentId = forms.CharField(label=u'IntellectMoney Payment ID')
    paymentData = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])
    paymentStatus= forms.TypedChoiceField(choices=STATUS_CHOICES, coerce=int)
    eshopAccount = forms.CharField()
    hash = forms.CharField()
    secretKey = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(ResultUrlForm, self).__init__(*args, **kwargs)
        if settings.SEND_SECRETKEY:
            self.fields['hash'].required = False
            self.fields['secretKey'].required = True
        else:
            self.fields['hash'].required = True
            self.fields['secretKey'].required = False

    def clean_secretKey(self):
        secretKey = self.cleaned_data['secretKey']
        if settings.SEND_SECRETKEY:
            if secretKey != settings.SEND_SECRETKEY:
                raise forms.ValidationError(u'Неверное значение')
        return secretKey

    def clean(self):
        data = self.cleaned_data
        if not settings.SEND_SECRETKEY:
            if not checkHashOnReceiveResult(data):
                raise forms.ValidationError(u'Неверный hash')
        return data


class AcceptingForm(_BaseForm):

    ACTION_CHOICES = [
        ('Refund', 'Refund'),
        ('ToPaid', 'ToPaid')
    ]

    action = forms.ChoiceField(choices=ACTION_CHOICES)
    secretKey = forms.CharField()
