#!/usr/bin/python
#
# Uses the verifier at https://browserid.org/verify to check the given
# assertion.
#
# The audience is passed as a command line parameter while the
# assertion comes on stdin.

from common import stringify_time
import httplib2
import json
import sys


URL_TIMEOUT = 5  # in seconds
CACERTS = '/etc/ssl/certs/ca-certificates.crt'
VERIFIER_URL = 'https://browserid.org/verify' # Official verifier
#VERIFIER_URL = 'http://127.0.0.1:10000/verify' # Local verifier


def verify_assertion(assertion, audience):
    if not assertion:
        return (None, None)

    verification_data = 'assertion=%s&audience=%s' % (assertion.strip(), audience)
    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    client = httplib2.Http(timeout=URL_TIMEOUT, ca_certs=CACERTS)
    response = content = None
    try:
        response, content = client.request(VERIFIER_URL, 'POST', body=verification_data,
                                           headers=headers)
    except httplib2.HttpLib2Error as e:
        print 'BrowserID verification service failure: ' % e

    if not response or response.status != 200 or not content:
        return 1

    try:
        parsed_response = json.loads(content)
    except ValueError:
        parsed_response = None

    if not parsed_response:
        print 'BrowserID verifier returned non-JSON/empty output: %s' % content
        return 1

    print "\nRaw response:\n  %s\n" % parsed_response

    if 'status' not in parsed_response:
        print 'BrowserID verification service did not return a status code'
        return 1
    if 'failure' == parsed_response['status']:
        print 'Failure: %s' % parsed_response['reason']
        return 1
    if parsed_response['status'] != 'okay':
        print 'BrowserID verifier returned unexpected "%s" status code' % parsed_response['status']
        return 1

    if not 'email' in parsed_response:
        print 'Missing email address'
        return 1

    print "Email: %s" % parsed_response['email']
    print "Audience: %s" % parsed_response['audience']
    print "Expiration: %s" % stringify_time(parsed_response['expires'])
    print "Issuer: %s" % parsed_response['issuer']
    return 0


def main(argv=None):
    if argv is None:
        argv = sys.argv

    audience = None
    if len(argv) > 1:
        audience = argv[1]
    else:
        print "Usage: %s <audience>" % argv[0]
        return 2

    assertion = sys.stdin.read()

    return verify_assertion(assertion, audience)


if __name__ == "__main__":
    sys.exit(main())
