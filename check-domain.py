#!/usr/bin/python
#
# Checks whether or not a domain is a primary authority for BrowserID
#
# Return codes:
#
#  0 - domain is correctly setup as a primary
#  1 - domain doesn't advertise itself as a primary
#  2 - domain configuration problem
#  3 - tool error

import httplib2
import json
import socket
import sys


CACERTS = '/etc/ssl/certs/ca-certificates.crt'
URL_TIMEOUT = 5  # in seconds
WELLKNOWN_FILENAME = '/.well-known/browserid'


def fetch_url(domain, path):
    url = 'https://%s%s' % (domain, path)
    client = httplib2.Http(timeout=URL_TIMEOUT, ca_certs=CACERTS)

    response = content = None
    error = False
    try:
        response, content = client.request(url, 'GET')
    except socket.error as e:
        print "%s doesn't listen on port 443: %s" % (domain, e)
        error = True
    except httplib2.HttpLib2Error as e:
        print 'Error while trying to retrieve the well-known file: %s' % e
        error = True

    return (response, content, error)


def parse_wellknown_file(domain, wellknown_content):
    try:
        details = json.loads(wellknown_content)
    except Exception as e:
        print "Error parsing well-known file: %s" % e
        return 2

    auth_page = None
    if 'authentication' in details:
        auth_page = details['authentication']

        (response, content, error) = fetch_url(domain, auth_page)
        if error or int(response.status) != 200:
            print "%s points to an invalid authentication page: https://%s%s" % (domain, domain, auth_page)
            return 2

    prov_page = None
    if 'provisioning' in details:
        prov_page = details['provisioning']

        (response, content, error) = fetch_url(domain, prov_page)
        if error or int(response.status) != 200:
            print "%s points to an invalid provisioning page: https://%s%s" % (domain, domain, prov_page)
            return error

    if 'public-key' not in details:
        print "%s is missing a public key." % domain
        return 2

    if auth_page and prov_page:
        print '%s is a primary authority for BrowserID.' % domain
        print '  Authentication: https://%s%s' % (domain, auth_page)
        print '  Provisioning: https://%s%s' % (domain, prov_page)
    elif not auth_page and not prov_page:
        print '%s looks like a secondary authority for BrowserID.' % domain
    elif prov_page:
        print '%s has a provisioning page but no authentication page.' % domain
        return 2
    elif auth_page:
        print '%s has an authentication page but no provisioning page.' % domain
        return 2

    print '  Public key: (algorightm=%s)' % details['public-key']['algorithm']
    return 0


def check_domain(domain):
    (response, content, error) = fetch_url(domain, WELLKNOWN_FILENAME)
    if error:
        return error

    if 404 == int(response['status']):
        print "No '%s' file available on %s." % (WELLKNOWN_FILENAME, domain)
        return 1

    if int(response['status']) != 200:
        print 'Received a %s status code while trying to retrieve the well-known file.' % response['status']
        return 2

    if 'application/json' not in response['content-type']:
        print "Received a '%s' response (instead of 'application/json') while trying to retrieve the well-known file." % response['content-type']
        return 2

    return parse_wellknown_file(domain, content)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    domain = None
    if len(argv) > 1:
        domain = argv[1]
    else:
        print "Usage: %s <domain>" % argv[0]
        return 3

    return check_domain(domain)


if __name__ == "__main__":
    sys.exit(main())
