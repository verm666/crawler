#!/usr/bin/env python
# encoding: utf-8

import os
import sys

sys.path.append(os.path.abspath(os.path.join(
  os.path.dirname(os.path.realpath(__file__)), '..')))

import unittest

from crawler.utils import *

class TestUriNormalize(unittest.TestCase):
    def test_unchange_absolute_uri(self):
        u = "http://example.com/test/image.jpg"
        c = make_context("http://example.com")
        r = uri_normalize(u, c)

        self.assertEqual(u, r)

    def test_collapse_slashes_in_absolute_uri(self):
        u = "http://example.com///test//image.jpg"
        c = make_context("http://example.com")
        r = uri_normalize(u, c)

        self.assertEqual(r, "http://example.com/test/image.jpg")

    def test_collapse_relative_path_in_absolute_uri(self):
        u = "http://example.com/test/../image.jpg"
        c = make_context("http://example.com")
        r = uri_normalize(u, c)

        self.assertEqual(r, 'http://example.com/image.jpg')

    def test_remove_fragments_from_absolute_uri(self):
        u = "http://example.com/test/index.html#Example"
        c = make_context("http://example.com")
        r = uri_normalize(u, c)

        self.assertEqual(r, 'http://example.com/test/index.html')

    def test_add_trailing_slash_to_absolute_uri(self):
        u = "http://example.com"
        c = make_context("http://example.com")
        r = uri_normalize(u, c)

        self.assertEqual(r, 'http://example.com/')

    def test_create_full_uri_from_abs_with_subdir_in_context(self):
        u = "/test/image.jpg"
        c = make_context("http://example.com/www")
        r = uri_normalize(u, c)

        self.assertEqual(r, "http://example.com/test/image.jpg")

    def test_create_full_uri_from_abs_without_subdir_in_context(self):
        u = "/test/image.jpg"
        c = make_context("http://example.com")
        r = uri_normalize(u, c)

        self.assertEqual(r, "http://example.com/test/image.jpg")

    def test_create_full_uri_from_realtive_with_subdir_in_context(self):
        u = "test/image.jpg"
        c = make_context("http://example.com/www")
        r = uri_normalize(u, c)

        self.assertEqual(r, "http://example.com/www/test/image.jpg")

    def test_create_full_uri_from_realtive_without_subdir_in_context(self):
        u = "test/image.jpg"
        c = make_context("http://example.com")
        r = uri_normalize(u, c)

        self.assertEqual(r, "http://example.com/test/image.jpg")


class TestUriFilterByNetloc(unittest.TestCase):
    def test_filter_true_netloc(self):
        u = uri_filter_by_netloc('http://example.com', 'example.com')
        self.assertEqual(u, 'http://example.com')

    def test_filter_false_netloc(self):
        u = uri_filter_by_netloc('http://example.com', 'example.org')
        self.assertEqual(u, None)

class TestUriRemoveNetloc(unittest.TestCase):
    def test_remove_from_only_netloc(self):
        u = uri_remove_netloc('http://example.com')
        self.assertEqual(u, '/')

    def test_remove_from_netloc_and_slash(self):
        u = uri_remove_netloc('http://example.com/')
        self.assertEqual(u, '/')

    def test_remove_from_netloc_and_slash(self):
        u = uri_remove_netloc('http://example.com/test/intro.html?test=10')
        self.assertEqual(u, '/test/intro.html?test=10')

    def test_dont_remove_fragments(self):
        u = uri_remove_netloc('http://example.com/test/intro.html#content')
        self.assertEqual(u, '/test/intro.html#content')

class TestMakeContext(unittest.TestCase):
    def test_make_context_without_path(self):
        u = 'http://example.com/'
        t = {
            'base_path': '/',
            'netloc': 'example.com',
            'scheme': 'http'
        }

        c = make_context(u)
        self.assertEqual(c, t)

    def test_make_context_with_path(self):
        u = 'http://example.com/test/'
        t = {
            'base_path': '/test/',
            'netloc': 'example.com',
            'scheme': 'http'
        }

        c = make_context(u)
        self.assertEqual(c, t)

class UrisExtractFromCss(unittest.TestCase):
    def test_extract_simple_urls(self):
        css = """
background-image: url("paper1.gif");
background-image:url("paper2.gif");
background-image:   url( "paper3.gif");
"""
        t = set(["paper1.gif", "paper2.gif", "paper3.gif"])
        u = uris_extract_from_css(css)
        self.assertEqual(t, u)

    def test_dont_extract_data_urls(self):
        css = """
background-image: url("paper1.gif");
background-image:url("paper2.gif");
background-image:   url( "paper3.gif");
background:
    url( data:image/gif;base64,R0lGODlhEAAQAMQAAORHHOVSKudfOulrSOp3WOyDZu6QdvCchPGolfO0o/XBs/fNwfjZ0frl3/zy7////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAkAABAALAAAAAAQABAAAAVVICSOZGlCQAosJ6mu7fiyZeKqNKToQGDsM8hBADgUXoGAiqhSvp5QAnQKGIgUhwFUYLCVDFCrKUE1lBavAViFIDlTImbKC5Gm2hB0SlBCBMQiB0UjIQA7)

"""
        t = set(["paper1.gif", "paper2.gif", "paper3.gif"])
        u = uris_extract_from_css(css)
        self.assertEqual(t, u)

if __name__ == "__main__":
    unittest.main()
