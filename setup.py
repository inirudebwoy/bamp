# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='bamp',
    version='0.2.1',
    install_requires=['Click', 'dulwich', 'six'],
    entry_points='''
      [console_scripts]
      bamp=bamp.main:bamp
      ''',
    packages=find_packages(),
    long_description='Bamp version of your packages according to semantic versioning. Automagically create commits and tags.',
    include_package_data=True,
    zip_safe=True,
    description='Bamp version according to semantic versioning',
    author='Michał Klich',
    author_email='michal@michalklich.com',
    url='https://github.com/inirudebwoy/bamp',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    license='MIT',
    classifiers=['Development Status :: 4 - Beta', 'Environment :: Console',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Topic :: Software Development :: Build Tools'])
