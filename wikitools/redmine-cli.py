#!/usr/bin/env python
"""
Simple command line interface (CLI) for working with
Redmine. Relies heavily on the python-redmine package
(http://python-redmine.readthedocs.org/).

"""
import os,sys
import logging
import argparse

from wikitools import DESRedmine
from wikitools import __version__

description = __doc__
parser = argparse.ArgumentParser(description=description)
parser.add_argument('url',help="URL of the page to edit.")
parser.add_argument('input',nargs='+',help="Input file(s), pattern(s), or text.")
parser.add_argument('-f','--force',action='store_true',
                    help="Force execution.")
parser.add_argument('-s','--section',default='redmine-des',
                    help="")
parser.add_argument('-v','--verbose',action='store_true',
                    help="Output verbosity (via logging).")
parser.add_argument('--version',action='version',version='%(prog)s '+str(__version__),
                    help="Print version and exit.")
parser.add_argument('-q','--quiet',action='store_true',
                    help="Silence output (via logging).")
parser.add_argument('-y','--yes',action='store_true',
                    help="Do not ask for confirmation (NOT IMPLEMENTED).")

group =parser.add_mutually_exclusive_group(required=True)
group.add_argument('--attach',action='store_true',
                   help="Attach a file to a wiki page.")
group.add_argument('--create',action='store_true',
                   help="Create a new wiki page (CAUTION).")
group.add_argument('--delete',action='store_true',
                   help="Delete a wiki page (CAUTION).")
group.add_argument('--detach',action='store_true',
                   help="Remove an attachment from wiki page.")
group.add_argument('--download',action='store_true',
                   help="Download attachment from wiki page.")
opts = parser.parse_args()


logging.basicConfig(stream=sys.stdout,level=logging.INFO)
logging.captureWarnings(True)

if opts.quiet:
    logging.getLogger().setLevel(logging.CRITICAL)
elif opts.verbose:
    logging.getLogger().setLevel(logging.DEBUG)
    ### # Prints requests
    ### import httplib
    ### httplib.HTTPConnection.debuglevel = 1
else:
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('redmine.packages.requests.packages.urllib3').setLevel(logging.WARNING)

# Create the interface
redmine = DESRedmine(section=opts.section)

# Parse the actions
if opts.attach:
    status = redmine.add_attachments(opts.url,opts.input)
if opts.create:
    redmine.create_wiki_page(opts.url,opts.force,text=opts.input)
if opts.delete:
    redmine.delete_wiki_page(opts.url,opts.force)
if opts.detach:
    status = redmine.delete_attachments(opts.url,opts.input,force=opts.force)
if opts.download:
    status = redmine.download_attachments(opts.url,opts.input)
