# -*- coding: utf-8 -*-
import io
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bamp",
    version="1.1.0",
    install_requires=["Click", "dulwich", "six"],
    entry_points="""
        [console_scripts]
        bamp=bamp.main:bamp
        """,
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    zip_safe=True,
    description="Bamp version according to semantic versioning",
    author="Michał Klich",
    author_email="michal@klichx.dev",
    url="https://gitlab.com/the_speedball/bamp",
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Build Tools",
    ],
)
