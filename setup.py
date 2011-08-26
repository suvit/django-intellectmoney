#!/usr/bin/env python
#coding:utf-8
from distutils.core import setup
import sys


reload(sys).setdefaultencoding("UTF-8")


setup(
    name='django-intellectmoney',
    version='0.0.1',
    author='Ivan Petukhov',
    author_email='satels@gmail.com',
    packages=['intellectmoney',],
    url='http://satels.blogspot.com/',
    download_url = 'https://github.com/satels/django-intellectmoney/zipball/master',
    license = 'MIT license',
    description = u'Приложение для работы с inellectmoney.ru.'.encode('utf8'),
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: Russian',
    ),
    install_requires=['django-annoying']
)
