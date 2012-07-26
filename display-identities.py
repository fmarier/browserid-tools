#!/usr/bin/python
#
# Parses a BrowserID key-ring (input on stdin) and display its contents
#
# The key-ring can be dumped using Chromium:
#
#   1- visit http://myfavoritebeer.org and login using BrowserID
#   2- visit https://browserid.org
#   3- right-click on the page and select "Inspect Element"
#   4- go to the "Resources" tab
#   5- expand "Local Storage" and click on "browserid.org"
#   6- select the "emails" key and double-click on its value to select it
#   7- use copy-paste (Ctrl+c) to dump the emails to a text file
#
# or using Firefox:
#
#   http://feeding.cloud.geek.nz/2012/07/dumping-contents-of-localstorage-in.html

from common import print_jwt
import json
import sys
#import time


def convert_time(iso8601_datetime):
    # FIXME: ISO8601 does allow for decimal fractions in the smallest
    # time value (and BrowserID uses it) but I can't get strptime to
    # parse it

    #t = time.strptime(iso8601_datetime, '%Y-%m-%dT%H:%M:%S%Z')
    #return time.strftime('%Y-%m-%d %H:%M:%S', t)
    return iso8601_datetime


def display_emails(local_storage):
    emails = json.loads(local_storage)

    first_run = True
    for email in emails:
        if not first_run:
            print
        else:
            first_run = False

        print "%s (%s)" % (email, emails[email]['type'])
        print "Created: %s" % convert_time(emails[email]['created'])
        if 'updated' in emails[email]:
            print "Updated: %s" % convert_time(emails[email]['updated'])

        if 'pub' in emails[email]:
            print "Public key: (algorithm=%s)" % emails[email]['pub']['algorithm']
            print "Private key: (algorithm=%s)" % emails[email]['priv']['algorithm']

            if 'cert' in emails[email]:
                print "Certificate:"
                print_jwt(emails[email]['cert'], email, emails[email]['pub'])
            else:
                print "No certificate associated with this key pair."
        else:
            print "No public/private keys available"
    return 0


def main(argv=None):
    if argv is None:
        argv = sys.argv

    local_storage = sys.stdin.read()

    return display_emails(local_storage)


if __name__ == "__main__":
    sys.exit(main())
