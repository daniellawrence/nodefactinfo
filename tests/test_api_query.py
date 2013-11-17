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

    def tearDown(self):
        pass


    def test_basic_ast(self):
        ast_query = query.simple2AST("hostname=bob")
        self.assertEqual(ast_query, '["=", ["fact", "hostname"], "bob" ]')

    def test_basic_ast_strip_spaces(self):
        ast_query = query.simple2AST("hostname = bob   ")
        self.assertEqual(ast_query, '["=", ["fact", "hostname"], "bob" ]')

    def test_basic_ast_strip_whitepsace(self):
        ast_query = query.simple2AST("hostname    =     bob       ")
        self.assertEqual(ast_query, '["=", ["fact", "hostname"], "bob" ]')

    def test_basic_ast_bad_queries(self):
        with self.assertRaises(Exception):
            ast_query = query.simple2AST("hostname")
        with self.assertRaises(Exception):
            ast_query = query.simple2AST()
        with self.assertRaises(Exception):
            ast_query = query.simple2AST("=")
        with self.assertRaises(Exception):
            ast_query = query.simple2AST("hostname=")
        with self.assertRaises(Exception):
            ast_query = query.simple2AST("=bob")
        with self.assertRaises(Exception):
            ast_query = query.simple2AST(" = bob")
        with self.assertRaises(Exception):
            ast_query = query.simple2AST(" = ")
        with self.assertRaises(Exception):
            ast_query = query.simple2AST(" hostname = ")

    def test_split_args(self):
        query.display_query_spliter([])
        query.display_query_spliter("")
        with self.assertRaises(Exception):
            query.display_query_spliter()
        with self.assertRaises(Exception):
            query.display_query_spliter(1)
        with self.assertRaises(Exception):
            query.display_query_spliter(1.0)

    def test_split_basic_query(self):
        r = query.display_query_spliter("hostname=bob")
        self.assertEqual(r.displable, [])
        self.assertEqual(len(r.queries), 1)
        self.assertEqual(r.queries, ['["=", ["fact", "hostname"], "bob" ]'])

    def test_split_basic_query(self):
        r = query.display_query_spliter("hostname=bob hostname=fred")
        self.assertEqual(r.displable, [])
        self.assertEqual(len(r.queries), 2)
        self.assertEqual(r.queries, [
            '["=", ["fact", "hostname"], "bob" ]',
            '["=", ["fact", "hostname"], "fred" ]',
        ])

    def test_split_basic_display(self):
        r = query.display_query_spliter("hostname")
        self.assertEqual(len(r.displable), 1)
        self.assertEqual(r.queries, [])
        self.assertEqual(r.displable, ["hostname"])
        
    def test_split_basic_display2(self):
        r = query.display_query_spliter("hostname uptime")
        self.assertEqual(len(r.displable), 2)
        self.assertEqual(r.queries, [])
        self.assertEqual(r.displable, ["hostname", "uptime"])

    def test_has_operator(self):
        for op in query.OPERATORS:
            self.assertEqual(query.has_operator(op), True)
        
    def test_has_operator2(self):
        self.assertEqual(query.has_operator("="), True)
        self.assertEqual(query.has_operator(" "), False)
        self.assertEqual(query.has_operator(" ==="), True)
        self.assertEqual(query.has_operator(" a=b"), True)
        self.assertEqual(query.has_operator(" AASDASD"), False)


if __name__ == '__main__':
    unittest.main()
