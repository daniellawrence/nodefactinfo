#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import pypuppetdb
from api.query import nodes_query

PUPPETDB_HOST='localhost'
PUPPETDB_PORT=49287


def argparser():
    parser = argparse.ArgumentParser(description='Query puppetdb from the cli')
    parser.add_argument('section', choices=['nodes', 'facts',],
                   help='Choose item that your interested in')
    parser.add_argument('query', nargs='*',
                        help='query that will be used to filter the response')

    args = parser.parse_args()
    return args

def main():
    args = argparser()
    db = pypuppetdb.connect(host=PUPPETDB_HOST, port=PUPPETDB_PORT)
    nodes_query(db, args.query)

if __name__ == '__main__':
    main()


