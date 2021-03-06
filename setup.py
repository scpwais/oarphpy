#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2020 Maintainers of OarphPy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

## NB See notes on `extras_require` and `Optional Dependencies` below.

import os
import sys
import re

try:
  from setuptools import setup, find_packages
except ImportError:
  from distutils.core import setup, find_packages

# Function to parse __version__ in `oarphpy/__init__.py`
def find_version():
  here = os.path.abspath(os.path.dirname(__file__))
  with open(os.path.join(here, 'oarphpy', '__init__.py'), 'r') as fp:
    version_file = fp.read()
  version_match = re.search(
    r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
  if version_match:
    return version_match.group(1)
  raise RuntimeError("Unable to find version string.")


# Decide which pytest we can use; pytest 4.x is last with dual support
setup_requires = ['pytest-runner']
tests_require = ['pytest']
if sys.version_info[0] < 3:
  setup_requires = ['pytest-runner<5']
  tests_require = ['pytest<5']

## Optional Dependencies
# OarphPy works in standard python 2 and 3 environments, but we provide extras
# if you have tensorflow, spark, or for the full-race oarphpy/full environment.
# For mor info, see "Dockerized Development Environments" in the root project
# README.md.

SPARK_DEPS = [
  'findspark==1.3.0',
  'numpy',
  'pandas>=0.19.2',
]
HAVE_SYSTEM_SPARK = (
  os.environ.get('SPARK_HOME') or
  os.path.exists('/opt/spark'))
if not HAVE_SYSTEM_SPARK:
  SPARK_DEPS += ['pyspark>=2.4.4']

TF_DEPS = [
  'crcmod',
  'tensorflow<=1.15.0',
]

UTILS = [
  # For various
  'six',

  # For SystemLock
  # 'fasteners==0.14.1', TODO clean up util.SystemLock
  
  # For lots of things
  'pandas',

  # For ThruputObserver
  'humanfriendly',
  'tabulate',
  'tabulatehelper',

  # For misc image utils
  'imageio',

  # For oarphpy.plotting
  'bokeh==1.0.4',
]

ALL_DEPS = UTILS + SPARK_DEPS + TF_DEPS

dist = setup(
  name='oarphpy',
  version=find_version(),
  description='A collection of Python utils with an emphasis on Data Science',
  author='Oarph',
  author_email='py@oarph.me',
  url='https://github.com/pwais/oarphpy',
  license='Apache License 2.0',
  packages=find_packages(exclude=['oarphpy_test*']),
  long_description="See https://github.com/pwais/oarphpy",
  long_description_content_type="text/x-rst",
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries',
    'Topic :: Scientific/Engineering',
    'Topic :: System :: Distributed Computing',
  ],
  
  test_suite='oarphpy_test',
  setup_requires=setup_requires,
  tests_require=tests_require,
  
  extras_require={
    'all': ALL_DEPS,        # for oarphpy/full environment
    'utils': UTILS,         # for oarphpy/full environment
    'spark': SPARK_DEPS,    # for oarphpy/spark environment
    'tensorflow': TF_DEPS,  # for oarphpy/tensorflow environment
                            # NB: for vanilla oarphpy/base-py2 and
                            #   oarphpy/base-py3 environments, we simply
                            #   include none of these extras.
  },
)
