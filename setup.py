import sys
import os
try: from setuptools import setup
except ImportError: from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))

def read(filename):
    return open(os.path.join(here,filename)).read()

setup(
    name='wikitools',
    version="0.0.0",
    url='https://github.com/kadrlica/wikitools',
    author='Alex Drlica-Wagner',
    author_email='kadrlica@fnal.gov',
    scripts = ['bin/redmine-cli'],
    install_requires=[
        'python-redmine >=1.5.0',
        'requests >=2.0.0',
    ],
    packages=['wikitools'],
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
