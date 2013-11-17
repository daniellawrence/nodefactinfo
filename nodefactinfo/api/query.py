#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pypuppetdb
import argparse
import logging
import re
import sys
from collections import namedtuple

PUPPETDB_HOST='localhost'
PUPPETDB_PORT=49205

OPERATORS = [
    '=',
    '~',
    '>',
    '<'
]

# 
RE_OPERATOR=r'(?P<fact>.+)(\s+|)(?P<operator>[%s])(\s+|)(?P<value>.+)' % "".join(OPERATORS)

def facts2dict(raw_facts):
    """
    Covert the facts generator from pypuppet into a simple dict().
    """

    facts = {}
    for fact in raw_facts:
        facts[fact.name] = fact.value
    return facts
    

def has_operator(query):
    """
    Check if the passed in query contains an OPERATOR
    
    This is used to work out if the raw input from the client is asking nfi to
    query puppetdb or customize how the results are passed back.

    """
    for char in query:
        if char in OPERATORS:
            return True
    return False

def simple2AST(queries):
    """
    Convert a very simple query into AST format for puppetdb
    
    This allows the client to pass in a very simple and have it converted into
    the AST format for puppetdb.
    
    for example.

    >>> simple2AST("hostname=bob")
    ["=", ["fact", "hostname"], "bob"]
    >>> simple2AST("hostname=bob hostname=fred")
    ["or",
      ["=", ["fact", "hostname"], "bob"]
      ["=", ["fact", "hostname"], "bob"]
    ]
    >>> simple2AST("hostname=bob kernel=Linux")
    ["and",
      ["=", ["fact", "hostname"], "bob"]
      ["=", ["fact", "kernel"], "linux"]
    ]
    """

    # split up strings into a list of queries
    if not isinstance(queries, str) and not isinstance(queries, unicode):
        raise Exception("simple2AST only converts a single query")

    # Make sure the query is a query
    if not has_operator(queries):
        raise Exception("simple2AST only converts queries: '%s'" % queries)

    re_match = re.match(RE_OPERATOR, queries)
    if not re_match:
        raise Exception("simple2AST failed to split query: '%s'" % RE_OPERATOR)

    #fact = re_match.groupdict()['fact']
    #if fact not in query_factnames:
    #    query_factnames.add(fact)
    #    if 'OR' not in queries:
    #        queries.append("OR")

    fact = re_match.groupdict()['fact']
    operator = re_match.groupdict()['operator']
    value = re_match.groupdict()['value']

    fact = fact.strip()
    value = value.strip()

    if not fact:
        raise Exception("simple2AST failed to find fact: '%s'" % queries)

    if not value:
        raise Exception("simple2AST failed to find value: '%s'" % queries)

    ASTquery = '["%s", ["fact", "%s"], "%s" ]' % (operator, fact, value)
    return ASTquery


def display_query_spliter(all_queries):
    """
    Reads over all the queries splitting them into display or AST
    
    """
    queries = []
    display = []
    Response = namedtuple('SplitInput', 'displable queries')

    # split up strings into a list of queries
    if isinstance(all_queries, str) or isinstance(all_queries, unicode):
        all_queries = all_queries.split()

    if all_queries:

        for query in all_queries:
            if has_operator(query):
                queries.append(simple2AST(query))
                continue
            elif query.upper() in ['AND', 'OR']:
                queries.append(query.upper())
                continue

            display.append(query)
            continue

    return Response(display, queries)

def _nodes_query(raw_client_input=None):
    query = None
    display = None

    client_input = display_query_spliter(raw_client_input)

    # If we have been given an AND, then everything is an AND
    if 'AND' in client_input.queries:
        client_input.queries.remove('AND')
        query = '["and", %s ]' % ", ".join(client_input.queries)


    # If we get an 'OR', then everything is an OR
    elif 'OR' in client_input.queries:
        client_input.queries.remove('OR')
        query = '["or", %s ]' % ", ".join(client_input.queries)

    # IF we didn't get an 'AND' or 'OR' then everything is an AND
    elif len(client_input.queries) > 1:
        query = '["and", %s ]' % ", ".join(client_input.queries)

    # If its a single query, then just set the query to be it.
    elif client_input.queries:
        query = client_input.queries[0]

    # No query is will in all the nodes.
    else:
        query = None

    # If we recieved any displable requests from the client input
    # Then format the nice output for them.
    displayformat = ''
    if client_input.displable:

        # Add the hostname to the output if we dont already have it.
        if 'hostname' not in client_input.displable:
            displayformat = "%(hostname)s "

        for display_item in client_input.displable:
            displayformat += '%%(%s)s ' % display_item

    results = namedtuple("NodeQuery", "query display displayformat")
    return results(query, display, displayformat)

def nodes_query(db, raw_client_input=None):
    """ 
    Allow for simple queries to return a list of node and facts.

    """

    # Process the raw input
    client_input = _nodes_query(raw_client_input)

    # Query puppetdb
    nodes = db.nodes(query=client_input.query)

    # Loop over the nodes, with the display_format
    for node in nodes:
        if client_input.displayformat:
            node_facts = facts2dict(node.facts())
            try:
                print client_input.displayformat % node_facts
            except KeyError as keyerror:
                print "node '%s' is missing fact %s" % (node, keyerror)
            continue
        print node

def fact_names(db):
    fact_list = db.fact_names()
    for fact_name in fact_list:
        print fact_name

def fact_query(db, raw_client_input=None):
    """
    Allow for simple query of facts.

    """
    
    if raw_client_input:
        return nodes_query(db, raw_client_input=raw_client_input)
    else:
        return fact_names(db)
    
    


