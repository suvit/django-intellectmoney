# -*- coding: utf-8 -*-
from .forms import ResultUrlForm
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import datetime


@csrf_exempt
@require_POST
def receive_result(request):
    ip = request.META['REMOTE_ADDR']
    preffix = 'IntellectMoney: '
    if ip != settings.INTELLECTMONEY_IP:
        subject = u'%sОповещение о платеже с неправильного ip'  % preffix
        #TODO: Send Mail
        raise Http404
    data = request.POST
    form = ResultUrlForm(data)
    if form.is_valid():
        data = form.cleaned_data
        body = u'Данные платежа:\n%s' % data
        orderId = data['orderId']
        recipientAmount = data['recipientAmount']
        invoice = None
        #TODO: Здесь все запихнуть в backend
        if invoice.paymentStatus is not None:
            subject = u'%sОповещение об уже обработанном платеже' % preffix
            #TODO: Send Mail
            return HttpResponse('OK')
        paymentStatus = data['paymentStatus']
        if paymentStatus in [5, 7]:
            paid = datetime.datetime.now()
            paymentId = data['paymentId']
            description = u'Оплата через intellectmoney #%s' % paymentId
            message = u'%sОплачен счет %s (%s руб)' % (preffix, orderId, recipientAmount)
            #TODO: Send Mail
        else:
            subject = u'%sПришло оповещение с неожидаемым статусом' % preffix
            #TODO: Send Mail
        return HttpResponse('OK')
    else:
        subject = u'%sФорма оповещения платежа: невалидные данные' % preffix
        body = u'Ошибки в форме: %s\n\nДанные:%s' % (
            unicode(form.errors), data.__dict__
        )
        #TODO: Send Mail
        return HttpResponse('Bad', status=400)


@csrf_exempt
def success(request):
    return render_to_response('intellectmoney/success.html')


@csrf_exempt
def fail(request):
    return render_to_response('intellectmoney/fail.html')
