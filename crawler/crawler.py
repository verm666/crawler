# encoding: utf-8

from __future__ import absolute_import

from urlparse import urlparse
from itertools import ifilter

import requests
import eventlet

from bs4 import BeautifulSoup

from .utils import *
from .logger import *

# in crawler case we don't care about SSL warnings
requests.packages.urllib3.disable_warnings()

eventlet.monkey_patch()

def http_request(uri, timeout=20, method='GET'):
    try:
        with eventlet.timeout.Timeout(timeout):
            if method == 'GET':
                return requests.get(uri, allow_redirects=True).content
            elif method == 'HEAD':
                return requests.head(uri, allow_redirects=True)
            else:
                error("unknown http method: `{0}`".format(uri))
    except eventlet.timeout.Timeout as e:
        error("download timeout for `{0}`".format(uri))
    except requests.exceptions.InvalidSchema:
        warn("invalid scheme: `{0}`".format(uri))
    except requests.ConnectionError:
        error("couldn't download content from `{0}`".format(uri))

def get(uri, timeout=20):
    return http_request(uri, timeout)

def head(uri, timeout=20):
    return http_request(uri, timeout, method='HEAD')


class Crawler(object):
    def __init__(self, options):
        self.options = options

        self.queue = eventlet.Queue()
        self.result = eventlet.Queue()
        self.pool = eventlet.GreenPool(self.options.pool_size)

        self.processed_links = set()
        self.css_cache = {}

        self.scheme = self.options.scheme
        self.netloc = self.options.domain

        uri = self.scheme + '://' + self.netloc + '/'

        self.queue.put(uri)

    def crawl(self, uri):
        info("crawl: {0}".format(uri))

        assets = set()
        links_to = set()

        content = get(uri, timeout=self.options.timeout)
        if content is None:
            return

        parsed = BeautifulSoup(content)

        c = make_context(uri)
        # extract javascript
        scripts = ifilter(None, uris_filter_by_netloc(
            uris_normalize(uris_extract(parsed.find_all('script')), c),
            netloc=self.netloc))
        assets.update(scripts)

        # extract images
        images = ifilter(None, uris_filter_by_netloc(
            uris_normalize(uris_extract(parsed.find_all('img')), c),
            netloc=self.netloc))
        assets.update(images)

        # extract styles
        links = parsed.find_all('link', href=True, rel='stylesheet')
        for link in links:
            href = link.get('href')
            normalized_href = uri_normalize(href, c)

            if not uri_filter_by_netloc(normalized_href, self.netloc):
                continue

            if normalized_href in self.css_cache.keys():
                uris_in_css = self.css_cache[normalized_href]
                assets.add(normalized_href)
                assets.update(uris_in_css)

            else:
                css = get(normalized_href, timeout=self.options.timeout)
                if css is None:
                    continue
                css_c = make_context(normalized_href)
                uris_in_css = filter(None, uris_filter_by_netloc(
                    uris_normalize(uris_extract_from_css(css), css_c),
                    netloc=self.netloc))

                assets.add(normalized_href)
                assets.update(uris_in_css)

                self.css_cache[normalized_href] = uris_in_css

        # extract links_to
        links = parsed.find_all('a', href=True)
        for link in links:
            href = link.get('href')
            if href.startswith('#') or href.startswith('mailto:'):
                continue

            parsed_href = urlparse(href)
            if parsed_href.netloc and parsed_href.netloc != self.netloc:
                continue

            normalized_href = uri_normalize(href, c)
            r = head(normalized_href, timeout=self.options.timeout)
            if r is None:
                continue

            if r.headers['content-type'].startswith('text/html'):
                info("{0}: found links_to: {1}".format(uri, normalized_href))
                links_to.add(normalized_href)

                if normalized_href not in self.processed_links:
                    self.queue.put(normalized_href)

        self.result.put((uri, assets, links_to))

    def run(self):
        while True:
            while not self.queue.empty():
                uri = self.queue.get()
                if uri in self.processed_links:
                    continue

                self.processed_links.add(uri)
                self.pool.spawn_n(self.crawl, uri)

            self.pool.waitall()
            if self.queue.empty():
                break

        res = {}
        while not self.result.empty():
            (uri, assets, links_to) = self.result.get()
            res[uri] = {'assets': list(assets), 'links_to': list(links_to)}

        return res
