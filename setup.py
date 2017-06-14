import sys
import os
try: from setuptools import setup
except ImportError: from distutils.core import setup
import versioneer

here = os.path.abspath(os.path.dirname(__file__))

URL = 'https://github.com/kadrlica/wikitools'
setup(
    name='wikitools',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    url=URL,
    author='Alex Drlica-Wagner',
    author_email='kadrlica@fnal.gov',
    scripts = ['bin/redmine-cli'],
    install_requires=[
        'python >= 2.7.0',
        'python-redmine >= 1.5.0',
        'requests >=2.0.0',
    ],
    packages=['wikitools'],
    description="Simple automated interface to scientific wiki tools.",
    long_description="See %s for more details."%URL,
    platforms='any',
    keywords='redmine wiki',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Intended Audience :: Science/Research',
    ]
)
