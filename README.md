This is a collection of tools related to [BrowserID](https://browserid.org).

# get_assertion.html

This is a simple webpage used to request an assertion from browserid.org.

Copy the assertion you get into a text file so that you can run the other
tools on it.

# unpack-assertion

To display the contents of an [assertion](https://wiki.mozilla.org/Identity/Verified_Email_Protocol/Latest#Bundled_Assertion):

    ./unpack-assertion < assertion.txt

# verify-assertion

To verify an assertion using https://browserid.org/verify:

    ./verify-assertion http://audience.example.com < assertion.txt

# License

Copyright (C) 2012 Francois Marier <francois@fmarier.org>

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
