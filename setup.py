from setuptools import setup


README = """
=====================
Django SlackIn Public
=====================

**Slack invitation page for Django (like rauchg/slackin)**

* PyPI: https://pypi.python.org/pypi/django-slackin-public
* Code: https://github.com/mtlpy/django-slackin-public
* |travis-ci|

.. |travis-ci| image::
   https://travis-ci.org/mtlpy/django-slackin-public.svg?branch=master
   :target: https://travis-ci.org/mtlpy/django-slackin-public
   :alt: Tests on Travis-CI

`More information on Github <https://github.com/mtlpy/django-slackin-public/blob/master/README.md>`_.
"""


setup(
    name='django-slackin-public',
    version='0.0.1',
    packages=['django_slackin_public'],
    include_package_data=True,
    license='MIT License',
    description='Slack invitation page for Django (like rauchg/slackin)',
    long_description=README,
    url='https://github.com/mtlpy/django-slackin-public',
    author='Pior Bastida',
    author_email='pior@pbastida.net',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
