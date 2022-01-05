#!/usr/bin/env python

from setuptools import setup

setup(name='pyvctrl',
      version='1.0',
      description='A simple Python wrapper for the vcontrold/vclient programs',
      author='Dirk Baechle',
      author_email='dl9obn@darc.de',
      url='https://github.com/dirkbaechle/pyvctrl',
      packages=['pyvctrl'],
      scripts = ['scripts/pyvctrl']
     )
