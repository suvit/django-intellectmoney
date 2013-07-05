# -*- coding: utf-8 -*-
import datetime

from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class IntellectMoney(models.Model):

    created = models.DateTimeField(editable=False,
                                   default=datetime.datetime.now)
    orderId = models.CharField(unique=True, editable=False, max_length=255)

    content_type = models.ForeignKey(ContentType,
                                     blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    recipient = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return u'IM payment %s for %s' % (self.orderId, self.recipient)
