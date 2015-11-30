Wiki Tools
=========

Toolkit for working with wikis targeted at scientific collaborations. 

### Installation

Installation is provided through the usual python `setuptools`. After downloading the source code, the package can be installed with:

    python setup.py install
    
If you don't have `root` access:

    python setup.py install --user

### Redmine

Redmine provided through a light wrapper around the [`python-redmine`](https://github.com/maxtepkeev/python-redmine) module, which interfaces with the [Redmine REST API](http://www.redmine.org/projects/redmine/wiki/Rest_api). The primary value added is a simple command line interface allowing users automate their interactions with wiki pages and attachments.

##### Example Usage
```bash
# The command line interface is focused on dealing with wiki pages and attachments

# First we create a test page:
url="https://cdcvs.fnal.gov/redmine/projects/des-sci-release/wiki/Redmine_Command_Line_Interface/Test_Page" 
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
