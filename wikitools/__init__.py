"""
Wikitools: Python interface for working with wiki pages
(specifically in a scientific research context).
"""
__author__ = "Alex Drlica-Wagner"
__email__  = "kadrlica@fnal.gov"
__project__ = "wikitools"

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

__all__ = ['deswiki']

from wikitools.deswiki import DESRedmine


