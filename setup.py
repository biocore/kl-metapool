#!/usr/bin/env python

# ----------------------------------------------------------------------------
# Copyright (c) 2015--, metapool development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import find_packages, setup
from glob import glob
from os.path import dirname

import versioneer

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'License :: OSI Approved :: MIT License',
    'Environment :: Console',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Operating System :: Unix',
    'Operating System :: POSIX',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows']


description = 'Metagenomic pooling Jupyter notebook helper'

with open('README.md') as f:
    long_description = f.read()

keywords = 'microbiome wetlab bioinformatics'

notebooks_fp = []
for fp in glob('notebooks/*.ipynb'):
    notebooks_fp.append((dirname(fp), [fp]))

setup(name='metapool',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      license='MIT',
      description=description,
      long_description=long_description,
      keywords=keywords,
      classifiers=classifiers,
      author="Jon Sanders",
      maintainer="Amanda Birmingham",
      url='https://github.com/biocore/kl-metapool',
      test_suite='nose.collector',
      packages=find_packages(),
      package_data={
          'metapool': ['data/*.tsv', 'data/*.xlsx', 'tests/data/*.csv']},
      include_package_data=True,
      # adding all the notebooks fps
      data_files=notebooks_fp,
      entry_points={
          'console_scripts': [
              'seqpro=metapool.scripts.seqpro:format_preparation_files',
              ('seqpro_mf=metapool.scripts.seqpro_mf:format_preparation_'
               'files_mf'),
          ],

      })
