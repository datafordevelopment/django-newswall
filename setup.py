#!/usr/bin/env python

from distutils.core import setup
import os
import setuplib

packages, package_data = setuplib.find_packages('newswall')

setup(name='django-newswall',
    version=__import__('newswall').__version__,
    description='A django-based news aggregator',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read().decode('utf-8'),
    author='Matthias Kestenholz',
    author_email='mk@feinheit.ch',
    url='http://github.com/matthiask/django-newswall/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=packages,
    package_data=package_data,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)
