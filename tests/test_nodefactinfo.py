#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_nodefactinfo
----------------------------------

Tests for `nodefactinfo` module.
"""

import unittest
from nodefactinfo.api import query


class TestNodefactinfo(unittest.TestCase):

    def setUp(self):
        pass

    def test_node_query(self):
        q = query._nodes_query("hostname")

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
