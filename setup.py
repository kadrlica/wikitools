import sys
import os
from setuptools import setup, find_packages

import wikitools

here = os.path.abspath(os.path.dirname(__file__))

def read(filename):
    return open(os.path.join(here,filename)).read()

setup(
    name='wikitools',
    version=wikitools.__version__,
    url='https://github.com/kadrlica/wikitools',
    author='Alex Drlica-Wagner',
    author_email='kadrlica@fnal.gov',
    scripts = ['bin/redmine-cli'],
    install_requires=[
        'python-redmine>=1.5.0',
        'requests>=2.0.0',
    ],
    packages=find_packages(),
    description="Simple automated interface to scientific wiki tools.",
    long_description=read('README.md'),
    platforms='any',
    keywords='redmine wiki',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Intended Audience :: Science/Research',
    ]
)
