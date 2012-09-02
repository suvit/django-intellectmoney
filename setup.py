#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from setuptools import setup, find_packages


setup(
    name='django-intellectmoney',
    version='0.0.2',
    author='Ivan Petukhov',
    author_email='satels@gmail.com',
    packages=find_packages(exclude=['docs', 'tests']),
    url='http://satels.blogspot.com/',
    download_url='https://github.com/satels/django-intellectmoney/zipball/master',
    license='MIT license',
    description=u'Приложение для работы с intellectmoney.ru.',
    long_description=file(
        os.path.join(
            os.path.dirname(__file__),
            'README.md'
        )
    ).read(),
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
    install_requires=['django-annoying'],
    include_package_data=True,
)
