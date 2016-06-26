# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(name='bamp',
      version='0.0.1',
      install_requires=['Click'],
      entry_points='''
      [console_scripts]
      bamp=bamp.main:bamp
      ''',
      packages=find_packages(),
      include_package_data=True,
      description='Bump version according to semantic versioning',
      author='Michał Klich',
      author_email='michal@michalklich.com',
      url='https://github.com/inirudebwoy/bamp',
      license='MIT',
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   'Topic :: Software Development :: Build Tools'])
