Wiki Tools
=========

[![Build](https://img.shields.io/travis/kadrlica/wikitools.svg)](https://travis-ci.org/kadrlica/wikitools)
[![Release](https://img.shields.io/github/release/kadrlica/wikitools.svg)](../../releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](../../)

Toolkit for working with wikis used by large scientific collaborations.

### Installation

Installation is provided through the usual python `setuptools`. The source code can either be cloned from github: 
```bash
git clone git@github.com:kadrlica/wikitools.git && cd wikitools
```
or downloaded and unzipped:
```bash
wget https://github.com/kadrlica/wikitools/archive/master.zip
unzip master.zip && cd wikitools-master
```

After downloading the source code, the package can be installed with:
```bash
python setup.py install
```

If you don't have `root` access, you can install locally with:
```bash
python setup.py install --user
```

### Redmine

Redmine provided through a light wrapper around the [`python-redmine`](https://github.com/maxtepkeev/python-redmine) module, which interfaces with the [Redmine REST API](http://www.redmine.org/projects/redmine/wiki/Rest_api). The primary value added is a simple command line interface allowing users automate their interactions with wiki pages and attachments.

##### Authentication Credentials

The preferred technique for passing your Redmine credentials to the command line interface is through the `.desservices.ini` file (the same file that stores you database credentials). To add your Redmine credentials to this file, add a new section with this format:
```ini
[redmine-des]
url     = https://cdcvs.fnal.gov/redmine
key     = <API-access-key>
user    = <username>
passwd  = <password>
```
The API access key is recommended, but not required for API access. Your API access key can be found by clicking the "My Account" link (upper right-hand corner) when logged into Redmine and looking "API access key" and clicking "Show" (as documented [here](http://www.redmine.org/projects/redmine/wiki/Rest_api#Authentication)).

If you don't add a section to your `.desservices.ini` file, then the command line tool will ask for your username and password at execution time. As mentioned before, access via API access key is preferred.

##### Example Usage
```bash
# The command line interface is focused on dealing with wiki pages and attachments

# First we create a test page:
url="https://cdcvs.fnal.gov/redmine/projects/des-sci-release/wiki/Test_Page" 
redmine-cli --create $url "This is a test page create with redmine-cli." 

# Next we create a few test files to attach to the page. Note that Redmine will not attach empty files.
seq 9 | xargs -i sh -c 'echo "hello world" > cli_test_attachment_{}.txt'

# We can attach a single file
redmine-cli --attach $url cli_test_attachment_1.txt 

# Or multiple files using the shell wildcard expansion
redmine-cli --attach $url cli_test_attachment_[1-9].txt

# Note that two versions of the first file have been attached

# We can download attachments using a regex (careful not to let the shell expand it)
redmine-cli --download $url 'cli_.*[1-5].txt'

# Note that both 'cli_test_attachment_1.txt' files were downloaded and a unique suffix was added 
# based on the Redmine attachment ID.


#Now what if we want to delete some of the attachments?
redmine-cli --detach $url cli_.*1.txt
  Delete 'https://cdcvs.fnal.gov/redmine/attachments/31251/cli_test_attachment_1.txt'? [Y/n] y
  Delete 'https://cdcvs.fnal.gov/redmine/attachments/31252/cli_test_attachment_1.txt'? [Y/n] n

# Here the regex is running into trouble because the files have the same name. However, we can 
# explicitly confirm which of the attachments we want to delete (we deleted the older one). To 
# override the confirmation request, we can add the '--force' option:
redmine-cli --force --detach $url cli_.*[7-9].txt
  INFO:root:Deleting https://cdcvs.fnal.gov/redmine/attachments/31258/cli_test_attachment_7.txt...
  INFO:root:Deleting https://cdcvs.fnal.gov/redmine/attachments/31259/cli_test_attachment_8.txt...
  INFO:root:Deleting https://cdcvs.fnal.gov/redmine/attachments/31260/cli_test_attachment_9.txt...
```

### Confluence

To come...
