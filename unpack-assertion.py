#!/usr/bin/python
#
# Unpack a BrowserID assertion (input on stdin) and display its contents
#
# The assertion format is described here:
#
#   https://wiki.mozilla.org/Identity/Verified_Email_Protocol/Latest
#   http://self-issued.info/docs/draft-jones-json-web-token.html

from common import decode, print_jwt
import sys


def unpack_assertion(packed_assertion):
    print_jwt(packed_assertion)
    return 0


def main(argv=None):
    if argv is None:
        argv = sys.argv

    assertion = sys.stdin.read()

    return unpack_assertion(assertion)


if __name__ == "__main__":
    sys.exit(main())
