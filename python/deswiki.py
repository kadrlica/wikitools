#!/usr/bin/env python
import redmine
import requests
import re

def get_config(filename):
    if 
    if getenv('DES_SERVICES'):
        desfile = getenv('DES_SERVICES')
    else:
        desfile = join(getenv('HOME'),'.desservices.ini')
    config = ConfigParser()
    config.read(desfile)


class DESRedmine(redmine.Redmine):
    def __init__(self,*args,**kwargs):
        auth = self.authenticate
        super(self,DESRedmine).__init__(*args,**kwargs)
    
    def add_attachments(url,attachments):
        pass

    def download_attachments(url,attachments):
        pass

    def delete_attachments(url,attachments):
        pass
    
    def get_page_from_url(url):
        self.url
        self.wiki_page.get(fields['title'],project_id=fields['project_id'])

    def parse_url(url):
        pass

    def authenticate():
        config = get_des_config()

        baseurl = config.get('redmine-des','url')
        key = config.get('redmine-des','key')
        username = config.get('redmine-des','user')
        password = config.get('redmine-des','passwd')

        

if __name__ == "__main__":
    import argparse
    description = "python script"
    parser = argparse.ArgumentParser(description=description)
    opts = parser.parse_args()
