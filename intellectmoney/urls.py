# -*- coding: utf-8 -*-
try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('intellectmoney.views',
    url(r'^result/$',  'receive_result', name='intellectmoney-result'),
    url(r'^success/result/$',  'success', name='intellectmoney-success'),
    url(r'^fail/result/$',  'fail', name='intellectmoney-fail'),

)
