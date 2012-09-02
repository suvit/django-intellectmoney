# -*- coding: utf-8 -*-
import datetime

from django.db import models


class IntellectMoney(models.Model):

    created = models.DateTimeField(editable=False,
                                   default=datetime.datetime.now)
    orderId = models.CharField(unique=True, editable=False, max_length=255)

