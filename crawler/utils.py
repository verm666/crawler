# encoding: utf-8

import re

from os.path import join, normpath, dirname, splitext
from urlparse import urlparse, ParseResult

"""
naming convention:

def uri_*() - must return uri
def uris_*() - must return generator or list of uris
"""

def uri_normalize(uri, context):
    parsed_uri = urlparse(uri)

    if parsed_uri.path == '':
        _path = '/'
    elif parsed_uri.path.startswith('/'):
        _path = normpath(re.sub('/{2,}', '/', parsed_uri.path))
    else:
        _path = normpath(join(context['base_path'], parsed_uri.path))

    return ParseResult(
        scheme=parsed_uri.scheme if parsed_uri.scheme else context['scheme'],
        netloc=parsed_uri.netloc if parsed_uri.netloc else context['netloc'],
        path=_path,
        params=parsed_uri.params,
        query=parsed_uri.query,
        fragment='').geturl()

def uris_normalize(uris, context):
     for uri in uris:
        yield uri_normalize(uri, context)

def uris_extract(elements):
    for x in elements:
        src = x.get('src')
        if src is not None:
            yield src

def uris_extract_from_css(css):
    uris = set()

    for uri in re.findall('url\(([^)]+)\)', css):
        uri = uri.strip().strip('"')
        if not uri.startswith('data:') and len(uri) != 0:
            uris.add(uri)

    return uris

def uri_filter_by_netloc(uri, netloc):
    return uri if urlparse(uri).netloc == netloc else None

def uris_filter_by_netloc(uris, netloc):
    for uri in uris:
        yield uri_filter_by_netloc(uri, netloc)

def make_context(uri):
    parsed_uri = urlparse(uri)

    (d, f) = splitext(parsed_uri.path)

    c = {
        'base_path': d,
        'netloc': parsed_uri.netloc,
        'scheme': parsed_uri.scheme
    }

    return c
