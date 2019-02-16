# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bamp',
    version='0.2.3',
    install_requires=['Click', 'dulwich', 'six'],
    entry_points='''
      [console_scripts]
      bamp=bamp.main:bamp
      ''',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    zip_safe=True,
    description='Bamp version according to semantic versioning',
    author='Michał Klich',
    author_email='michal@michalklich.com',
    url='https://gitlab.com/the_speedball/bamp',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    license='MIT',
    classifiers=['Development Status :: 4 - Beta', 'Environment :: Console',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Topic :: Software Development :: Build Tools'])
