# encoding: utf-8

from __future__ import print_function

import sys
import json
import urlparse

from optparse import OptionParser

from .crawler import Crawler

__all__ = ('run_crawler')
__version__ = "1.0.0"
__author__ = "Eduard Snesarev"
__author_email__ = "verm666@gmail.com"

def run_crawler():
    try:
        p = OptionParser()
        p.add_option("-d", "--domain",
            help="uri for crawling, example: example.com")

        p.add_option("-s", "--scheme", default="https",
            help="available schemas: http and https, [default: %default]")

        p.add_option("-r", "--report", default="/tmp/report.json",
            help="path to report.json, [default: %default]")

        p.add_option("-p", "--pool-size", default=100, type="int",
            help="eventlet pool size, [default: %default]")

        p.add_option("-t", "--timeout", default=20, type="int",
            help="http request timeout in seconds, [default: %default]")

        (options, args) = p.parse_args()
        if options.domain is None:
            print("error: missing required argument `domain`, see {0} --help".format(
                sys.argv[0]))
            sys.exit(1)

        if options.scheme not in ['http', 'https']:
            print("error: ivalid scheme `{0}`, see {1} --help".format(
                options.scheme, sys.argv[0]))
            sys.exit(1)

        c = Crawler(options)
        r = c.run()
        try:
            with open(options.report, 'w') as f:
                f.write(json.dumps(r, indent=4) + "\n")
        except (OSError, IOError) as e:
            print("error: couldn't save report to `{0}`, reason: {1}".format(
                options.report, e))
            sys.exit(1)

    except KeyboardInterrupt:
        sys.exit(1)
