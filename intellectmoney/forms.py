# -*- coding: utf-8 -*-
from .helpers import cheskHashOnReceiveResult
from django import forms
from django.conf import settings


class _BaseForm(forms.Form):

    eshopId = forms.CharField(initial=settings.INTELLECTMONEY_SHOPID)
    orderId = forms.CharField(max_length=50)

    def clean_eshopId(self):
        eshopId = self.cleaned_data['eshopId']
        if eshopId != settings.INTELLECTMONEY_SHOPID:
            raise forms.ValidationError(u'Неверный eshopId')
        return eshopId


class _BasePaymentForm(_BaseForm):

    CURRENCY_CHOICES = map(lambda x: (x, x), ['RUR', 'TST'])
    serviceName = forms.CharField(label=u'Payment Description', required=False)
    recipientAmount = forms.DecimalField(max_digits=10, decimal_places=2)
    recipientCurrency = forms.ChoiceField(
        choices=CURRENCY_CHOICES,
        initial=settings.INTELLECTMONEY_DEBUG and 'TST' or 'RUR'
    )
    userName = forms.CharField(max_length=255, required=False)
    email = forms.EmailField(required=False)


class IntellectMoneyForm(_BasePaymentForm):
    """Payment request form."""

    PREFERENCE_CHOICES = [
        ('inner', 'IntellectMoney'),
        ('bankCard', 'Visa/MasterCard'),
        ('exchangers', u'Internet Exchangers'),
        ('terminals', u'Terminals'),
        ('bank', u'Bank'),
    ]

    successUrl = forms.CharField(
        required=False, max_length=512,
        initial=settings.INTELLECTMONEY_SUCCESS_URL
    )
    failUrl = forms.CharField(
        required=False, max_length=512,
        initial=settings.INTELLECTMONEY_FAIL_URL
    )
    preference = forms.ChoiceField(
        label=u'Payment Method', choices=PREFERENCE_CHOICES
    )
    expireDate = forms.DateTimeField(required=False)


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
        if settings.INTELLECTMONEY_SEND_SECRETKEY:
            self.fields['hash'].required = False
            self.fields['secretKey'].required = True
        else:
            self.fields['hash'].required = True
            self.fields['secretKey'].required = False

    def clean_secretKey(self):
        secretKey = self.cleaned_data['secretKey']
        if settings.INTELLECTMONEY_SEND_SECRETKEY:
            if secretKey != settings.INTELLECTMONEY_SECRETKEY:
                raise forms.ValidationError(u'Неверное значение')
        return secretKey

    def clean(self):
        data = self.cleaned_data
        if not settings.INTELLECTMONEY_SEND_SECRETKEY:
            if not cheskHashOnReceiveResult(data):
                raise forms.ValidationError(u'Неверный hash')
        return data


class AcceptingForm(_BaseForm):

    ACTION_CHOICES = [
        ('Refund', 'Refund'),
        ('ToPaid', 'ToPaid')
    ]

    action = forms.ChoiceField(choices=ACTION_CHOICES)
    secretKey = forms.CharField()
