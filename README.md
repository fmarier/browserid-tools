This is a collection of tools related to [BrowserID](https://browserid.org).

# check-domain.py

To check whether a domain is a primary or secondary authority for BrowserID based on the well-known file it needs to publish.

    ./check-domain.py eyedee.me

# display-identities.py

To view the details of identities stored in your browser's [local storage](https://developer.mozilla.org/en/DOM/Storage):

    ./display-identities.py < localstorage.txt

# get_assertion.html

This is a simple webpage used to request an assertion from browserid.org.

Copy the assertion you get into a text file so that you can run the other
tools on it.

# unpack-assertion.py

To display the contents of an [assertion](https://wiki.mozilla.org/Identity/Verified_Email_Protocol/Latest#Bundled_Assertion):

    ./unpack-assertion.py < assertion.txt

# verify-assertion.py

To verify an assertion using the [official verifier](https://browserid.org/verify):

    ./verify-assertion.py http://audience.example.com < assertion.txt

# License

Copyright (C) 2012 Francois Marier \<francois@fmarier.org\>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
