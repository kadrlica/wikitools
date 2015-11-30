#!/usr/bin/env python
"""
Package for interfacing with the Dark Energy Survey (DES) wikis.

Currently supports Redmine access through the `DESRedmine` class.

"""

import os
import sys
import re
import requests
import getpass
import logging
from collections import OrderedDict as odict

import redmine

# Utility Functions
def get_des_config(desfile=None):
    """
    Simplified version of despyServiceAccess from DESDM. 
    Access file description in DESDM-3:
    https://opensource.ncsa.illinois.edu/confluence/x/lwCsAw
    """
    from ConfigParser import SafeConfigParser

    if not desfile: desfile = os.getenv('DES_SERVICES')
    if not desfile: desfile = os.path.join(os.getenv('HOME'),'.desservices.ini')
    
    # ConfigParser throws confusing error if file doesn't exist
    open(desfile)
    
    config = SafeConfigParser()
    config.read(desfile)
    return config

def confirm(question,default=True):
    """
    Simple function for getting yes/no response from raw_input

    From: http://stackoverflow.com/a/3041990
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False, 
             True:True, False:False}

    if default is None:
        prompt = " [y/n] "
    elif valid[default]:
        prompt = " [Y/n] "
    elif not valid[default]:
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower().strip()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

class DESRedmine(redmine.Redmine):

    baseurl = "https://cdcvs.fnal.gov/redmine"

    def __init__(self,**kwargs):
        """ Wrapper around redmine.Redmine """
        kw = self.authenticate()
        kw.update(**kwargs)
        super(DESRedmine,self).__init__(**kw)
    
    def add_attachments(self,url,attachments,descriptions=None):
        """ 
        Attach files to wiki page at the given url.
        """
        page = self.wiki_page_from_url(url)
        
        if isinstance(attachments,basestring):
            attachments = [attachments]

        default_desc='automated upload'
        if descriptions is None: 
            descriptions = len(attachments)*[default_desc]
        elif isinstance(descriptions,basestring):
            descriptions = [descriptions]

        uploads = []
        for a,d in zip(attachments,descriptions):
            uploads += [dict(path=a,filename=os.path.basename(a),description=d)]

        fields = dict(
            resource_id=page.internal_id,
            project_id=page.manager.params.get('project_id',0),
            text = page.text,
            uploads = uploads,
        )
        logging.info("Attaching files:\n"+"/n".join(attachments))
        return self.wiki_page.update(**fields)

    def download_attachments(self,url,patterns=None):
        """ 
        Download attachment(s) that match given pattern(s).
        """
        attachments = self.attachments_from_patterns(url,patterns)
        
        # For large files:
        # self.requests['stream'] = True
        savepath = ''
        for a in attachments:
            outname = a.filename
            if filenames.count(outname) > 1:
                outname += '.%i'%a.internal_id
            #print msg

            if os.path.exists(os.path.join(savepath,outname)):
                msg = "Found %s; skipping..."%outname
                logging.info(msg)
                continue
            else:
                msg = "Downloading %s..."%outname
                logging.info(msg)
                a.download(savepath='',filename=outname)

        return True

    def delete_attachments(self,url,patterns=None,force=False):
        """ 
        Delete attachment(s) that match given pattern(s) 
        """
        LOGIN_BUTTON = "Login &#187;"

        # The Redmine API explicitly does not support DELETE requests
        # for attachments. The work around is to start a login session.
        session = requests.session()
        loginurl = self.url + '/login'
        token = self.get_authenticity_token(session.get(loginurl))
        data = dict(username=self.username,password=self.password,
                    login=LOGIN_BUTTON,authenticity_token=token)
        response = session.post(loginurl,data=data)
        token = self.get_authenticity_token(response)        

        # Grab the attachments that we are going to delete
        attachments = self.attachments_from_patterns(url,patterns)
        if not len(attachments):
            msg = "No matching attachments found."
            raise Exception(msg)

        for a in attachments:
            data = dict(_method='delete',authenticity_token=token)
            if not force:
                question = "Delete '%s/%s'?"%(a.url,a.filename)
                if not confirm(question,default=True): continue

            msg = "Deleting %s/%s..."%(a.url,a.filename)
            logging.info(msg)
            r = session.post(a.url,data=data,cookies=response.cookies)
            self.status_code(r)
            
        session.close()
        return True

    def create_wiki_page(self,url,force=False,**kwargs):
        """
        Tiny wrapper around `redmine.wiki_page.create`
        """
        project_id,resource_id = self.parse_url(url)
        fields = dict(resource_id=resource_id,project_id=project_id,
                      title=resource_id.replace('_',' '),text=' ')
        fields.update(**kwargs)
        if not force:
            question = "Create '%s'?"%url
            if not confirm(question,default=False): 
                return None

        logging.info("Creating %s..."%url)
        return self.wiki_page.create(**fields)

    def delete_wiki_page(self,url,force=False,**kwargs):
        """
        Tiny wrapper around `redmine.wiki_page.delete`.
        """
        project_id,resource_id = self.parse_url(url)
        fields = dict(resource_id=resource_id,project_id=project_id)
        fields.update(**kwargs)
        if not force:
            question = "Delete '%s'?"%url
            if not confirm(question,default=False): 
                return None
        logging.info("Deleting %s..."%url)
        return self.wiki_page.delete(**fields)
        
    def attachments_from_patterns(self,url,patterns=None):
        """ 
        Attachments with filenames that match the given pattern(s).
        """
        if patterns is None:
            patterns = ['']
        if isinstance(patterns,basestring):
            patterns = [patterns]

        page = self.wiki_page_from_url(url)
        attachments = page.attachments
        filenames = [a.filename for a in attachments]
        index = [i for p in patterns for i,f in enumerate(filenames) if re.match(p,f)]

        return [attachments[i] for i in index]


    def parse_url(self, url):
        if not url.startswith(self.url):
            msg = "Requested URL not in DES domain: %s"%url
            raise Exception(msg)

        # Stripped url should now be of the form: 
        # /projects/<project_id>/.../<resource_id>
        content = url[len(self.url):].strip('/').split('/')
        project_id = content[1]
        resource_id = content[-1]
        return project_id,resource_id

    def wiki_page_from_url(self,url):
        project_id,resource_id = self.parse_url(url)
        fields = dict(resource_id=resource_id,project_id=project_id)
        return self.wiki_page.get(**fields)

    def authenticate(self,section='redmine-des'):
        """
        Grab redmine authentication
        """
        auth = odict(
            url    = self.baseurl,
            key    = None,
            user   = None,
            passwd = None,
        )
        def defaults(): return auth

        config = get_des_config()
        config.defaults = defaults
        
        if section in config.sections():
            auth = dict([(k,config.get(section,k)) for k in auth.keys()])

        if (auth['user'] is None) or (auth['passwd'] is None):
            auth['user'] = raw_input('Username: ')
            auth['passwd'] = getpass.getpass()

        auth['username'] = auth.pop('user')
        auth['password'] = auth.pop('passwd')

        return auth
        
    @staticmethod
    def get_authenticity_token(response):
        """ Get the CSRF authenticity token from a response """
        pattern = 'meta content="(.*)" name="csrf-token"'
        token = re.search(pattern,str(response.content)).group(1)
        return token

    @staticmethod
    def status_code(response):
        if response.status_code in (200, 201):
            return response
        elif response.status_code == 401:
            raise redmine.exceptions.AuthError
        elif response.status_code == 403:
            raise redmine.exceptions.ForbiddenError
        elif response.status_code == 404:
            raise redmine.exceptions.ResourceNotFoundError
        elif response.status_code == 409:
            raise redmine.exceptions.ConflictError
        elif response.status_code == 412:
            raise redmine.exceptions.ImpersonateError
        elif response.status_code == 413:
            raise redmine.exceptions.RequestEntityTooLargeError
        elif response.status_code == 422:
            errors = response.json()['errors']
            raise redmine.exceptions.ValidationError(to_string(', '.join(e if is_string(e) else ': '.join(e) for e in errors)))
        elif response.status_code == 500:
            raise redmine.exceptions.ServerError
         
        raise redmine.exceptions.UnknownError(response.status_code)
    
if __name__ == "__main__":
    import argparse
    description = "python script"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-v','--verbose',action='store_true')
    opts = parser.parse_args()
    
    logging.getLogger().setLevel(logging.INFO)
    if opts.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
