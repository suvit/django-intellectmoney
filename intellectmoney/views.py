# -*- coding: utf-8 -*-
from django.core.mail import mail_admins
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.template.context import RequestContext

from annoying.functions import get_object_or_None

from intellectmoney import settings
from intellectmoney.forms import ResultUrlForm
from intellectmoney.models import IntellectMoney
from intellectmoney.signals import result_received


@csrf_exempt
@require_POST
def receive_result(request):
    ip = request.META['REMOTE_ADDR']
    preffix = 'IntellectMoney: '
    info = request.POST
    if ip != settings.IP:
        subject = u'%sОповещение о платеже с неправильного ip'  % preffix
        mail_admins(subject, message=u'Дата: %s' % info)
        raise Http404
    form = ResultUrlForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        orderId = data['orderId']
        recipientAmount = data['recipientAmount']
        paymentId = data['paymentId']
        invoice = get_object_or_None(IntellectMoney, orderId=orderId)
        if not invoice:
            subject = u'%sОповещение об оплате несуществующего счета #%s' % (
                preffix, paymentId
            )
            mail_admins(subject, message=u'Дата: %s' % info)
            return HttpResponse('OK')
        paymentStatus = data['paymentStatus']
        if paymentStatus in [5, 6, 7]:
            subject = u'Оплата через intellectmoney #%s' % paymentId
            if paymentStatus == 6:
                message = u'%sОплачен счет %s (ЗАБЛОКИРОВАНО %s руб)' % (
                   preffix, orderId, recipientAmount,
                )
            else:
                message = u'%sОплачен счет %s (%s руб)' % (
                   preffix, orderId, recipientAmount,
                )
            mail_admins(subject, message=message)
            result_received.send(
                sender=invoice, orderId=orderId, recipientAmount=recipientAmount,
            )
        elif paymentStatus == 3:
            return HttpResponse('OK')
        else:
            subject = u'%sПришло оповещение с неожидаемым статусом' % preffix
            mail_admins(subject, message=u'Дата: %s' % info)
        return HttpResponse('OK')
    else:
        subject = u'%sФорма оповещения платежа: невалидные данные' % preffix
        body = u'Ошибки в форме: %s\n\nДанные:%s' % (unicode(form.errors), info)
        mail_admins(subject, message=body)
        return HttpResponse('Bad', status=400)


@csrf_exempt
def success(request):
    return render_to_response('intellectmoney/success.html',
        context_instance=RequestContext(request)
    )


@csrf_exempt
def fail(request):
    return render_to_response('intellectmoney/fail.html',
        context_instance=RequestContext(request)
    )
