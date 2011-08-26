#coding:utf-8
from django.db import models
import datetime


class IntellectMoney(models.Model):

    created = models.DateTimeField(editable=False, default=datetime.datetime.now)
    orderId = models.CharField(unique=True, editable=False, max_length=255)

