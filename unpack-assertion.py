#!/usr/bin/python
#
# Unpack a BrowserID assertion (input on stdin) and display its contents
#
# The assertion format is described here:
#
#   https://wiki.mozilla.org/Identity/Verified_Email_Protocol/Latest
#   http://self-issued.info/docs/draft-jones-json-web-token.html

import base64
import json
import sys
import time


def base64_pad_decode(string):
    # pad base64 encoding
    # https://en.wikipedia.org/wiki/Base64#Decoding_Base64_with_padding
    string = string.strip()
    l = len(string)
    if l % 4 == 0:
        pass # no need to pad
    elif l % 4 == 2:
        string += '=='
    elif l % 4 == 3:
        string += '='
    else:
        print "Invalid Base64 input"
        return None

    return base64.b64decode(string)


def decode(string):
    return json.loads(base64_pad_decode(string))


def stringify_time(utc_epoch):
    t = time.gmtime(int(utc_epoch) / 1000)
    return time.strftime('%Y-%m-%d %H:%M:%S', t)


def unpack_assertion(packed_assertion):
    bundled_assertion = decode(packed_assertion)

    print "%s certificate(s):" % len(bundled_assertion['certificates'])
    for cert in bundled_assertion['certificates']:
        (header, claim, crypto) = cert.split('.')
        decoded_header = decode(header)
        decoded_claim = decode(claim)
        print '  Algorithm: %s' % decoded_header['alg']
        print '  Issuer: %s' % decoded_claim['iss']
        print '  Issued at: %s' % stringify_time(decoded_claim['iat'])
        print '  Expiration: %s' % stringify_time(decoded_claim['exp'])
        if 'email' in decoded_claim['principal']:
            print '  Principal: %s' % decoded_claim['principal']['email']
        if 'host' in decoded_claim['principal']:
            print '  Principal: %s' % decoded_claim['principal']['host']
        print '  Public key: (algorithm=%s)' % decoded_claim['public-key']['algorithm']
        print

    print 'Identity Assertion:'
    (header, claim, crypto) = bundled_assertion['assertion'].split('.')
    decoded_header = decode(header)
    decoded_claim = decode(claim)
    print '  Algorithm: %s' % decoded_header['alg']
    print '  Audience: %s' % decoded_claim['aud']
    print '  Expiration: %s' % stringify_time(decoded_claim['exp'])

    return 0


def main(argv=None):
    if argv is None:
        argv = sys.argv

    assertion = sys.stdin.read()

    return unpack_assertion(assertion)


if __name__ == "__main__":
    sys.exit(main())
