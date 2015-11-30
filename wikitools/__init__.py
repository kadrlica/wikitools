"""
Wikitools: Python interface for working with wiki pages
(specifically in a scientific research context).
"""
__author__ = "Alex Drlica-Wagner"
__email__  = "kadrlica@fnal.gov"
__project__ = "wikitools"
__version__ = None

from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution(__project__).version
except DistributionNotFound:
    __version__ = "local"

from wikitools.deswiki import DESRedmine

__all__ = ['deswiki']
