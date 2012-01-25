# Common functions for all of these tools

import base64
import json
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


def stringify_time(utc_epoch):
    t = time.gmtime(int(utc_epoch) / 1000)
    return time.strftime('%Y-%m-%d %H:%M:%S', t)


def decode(string):
    return json.loads(base64_pad_decode(string))


def compare_keys(key1, key2):
    if ('y' in key1 and not 'y' in key2) or (not 'x' in key1 and 'x' in key2):
        return False # key1 is a public key while key2 is a private key
    if (not 'y' in key1 and 'y' in key2) or ('x' in key1 and not 'x' in key2):
        return False # key1 is a private key while key2 is a private key

    if 'y' in key1:
        if key1['y'] != key2['y']:
            return False
    if 'x' in key1:
        if key1['s'] != key2['s']:
            return False

    if key1['p'] != key2['p']:
        return False
    if key1['q'] != key2['q']:
        return False
    if key1['g'] != key2['g']:
        return False

    return True


def print_jwt(cert, email=None, public_key=None):
    (header, claim, crypto) = cert.split('.')
    decoded_header = decode(header)
    decoded_claim = decode(claim)
    print '  Algorithm: %s' % decoded_header['alg']
    if 'aud' in decoded_claim:
        print '  Audience: %s' % decoded_claim['aud']
    if 'iss' in decoded_claim:
        print '  Issuer: %s' % decoded_claim['iss']
        print '  Issued  at: %s' % stringify_time(decoded_claim['iat'])
    print '  Expiration: %s' % stringify_time(decoded_claim['exp'])
    if 'principal' in decoded_claim:
        if 'email' in decoded_claim['principal']:
            print '  Principal: %s' % decoded_claim['principal']['email']
            if email and email != decoded_claim['principal']['email']:
                print "  WARNING: this certificate is for a different email address: %s" % decoded_claim['principal']['email']
            if 'host' in decoded_claim['principal']:
                print '  Principal: %s' % decoded_claim['principal']['host']
    if 'public-key' in decoded_claim:
        print '  Public key: (algorithm=%s)' % decoded_claim['public-key']['algorithm']
        if public_key and not compare_keys(decoded_claim['public-key'], public_key):
            print "  WARNING: this certificate is for a different public key"
