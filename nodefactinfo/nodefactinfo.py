#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import requests
import sys
import traceback

import pypuppetdb


from api.query import nodes_query, fact_query

PUPPETDB_HOST = os.getenv('PUPPETMASTER', 'localhost')
PUPPETDB_PORT = os.getenv('PUPPETDBPORT', 8080)


def argparser():
    parser = argparse.ArgumentParser(description='Query puppetdb from the cli')
    parser.add_argument('section', choices=['nodes', 'facts', ],
                        help='Choose item that your interested in')
    parser.add_argument('query', nargs='*',
                        help='query that will be used to filter the response')

    args = parser.parse_args()
    return args


def make_it_so():
    args = argparser()
    db = pypuppetdb.connect(host=PUPPETDB_HOST, port=PUPPETDB_PORT)

    if args.section == 'nodes':
        nodes_query(db, args.query)

    if args.section == 'facts':
        fact_query(db, args.query)


def main():
    try:
        make_it_so()
        sys.exit(0)
    except requests.exceptions.ConnectionError as error:
        print("Connection Error")
        print("-----------------")
        print("%s" % error)
        traceback.print_exc(file=sys.stdout)
        print("You can give environment varibles to change puppetdb's")
        print("export PUPPETMASTER=localhost")
        print("export PUPPETDBPORT=8080")
        sys.exit(1)
    except Exception as error:
        print("Unknown Exception")
        print("-----------------")
        print("%s" % error)
        traceback.print_exc(file=sys.stdout)
        sys.exit(2)

    print("Unknown PATH")
    print("-----------------")
    sys.exit(3)


if __name__ == '__main__':
    main()
