Installing
==========

1. ```pip install git+https://github.con/satels/django-intellectmoney```

2. Добавить в `settings.py` правильные настройки для магазина.

3. Добавить страницу, где будет выводиться форма заказа.

Settings
========

*  `INTELLECTMONEY_SHOPID`

   ИД магазина в системе Интелектмани

*  `INTELLECTMONEY_SECRETKEY`

   секретный ключ магазина

*  `INTELLECTMONEY_DEBUG`

   режим отладки, по умолчанию *да*

*  `INTELLECTMONEY_UNIQUE_ID`

   разрешить только уникальные ИД заказов, по умолчанию *нет*

*  `INTELLECTMONEY_REQUIRE_HASH`

   требовать хэш, по умолчанию *нет*

*  `INTELLECTMONEY_SEND_SECRETKEY`

   высылать секретный ключ магазина, по умолчанию *нет*

*  `INTELLECTMONEY_HOLD_MODE`

   использовать режим OnHold, по умолчанию *нет*

*  `INTELLECTMONEY_EXPIRE_DATE_OFFSET`

   временой интервал действия режима OnHold, по умолчанию *7 дней*

   не применяется если `INTELLECTMONEY_HOLD_MODE` ложь
