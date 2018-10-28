#!/usr/bin/env python
# -*- coding: utf-8 -*-

import queries
import argparse
import textwrap
import os

from prettytable import from_db_cursor
from prettytable import PrettyTable
from collections import deque

from dublin_db import DB, TABLES
from dublin_openstreet import NODES_PATH ,NODE_TAGS_PATH, WAYS_PATH, WAY_NODES_PATH, WAY_TAGS_PATH
from dublin_openstreet import expected

DB_NAME = "dublin"
QUERIES = queries.queries
QUERY_ALL = "ALL"
SPECIAL_QUERY = ["rows_per_table","street_types"]

class QUERY:
    def __init__(self):
        self.DB = DB(DB_NAME)
        self.conn = self.DB.connect_to_db()

    def print_description(self):
        return textwrap.dedent('''\
         |------------------------------------------------------------------
         | Execute your queries in the specified DB :) See the options below:
         |------------------------------------------------------------------
         | - Execute queries defined over queries.py map.
         | - Update queries.py with new queries
         | - Pass the option --query_name to execute an specific query
         | - Execute multiple queries at once by passing --queries_names option
         | Future Versions:
         | - Execute all queries
         |------------------------------------------------------------------
         ''')

    def main(self):
        ''' Cli to be able to execute a list of queries or one query only'''
        parser = argparse.ArgumentParser(description=self.print_description(),
                                         prog='dublin_queries',
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--queries_names', dest='query_name', nargs='*',
                            help='Execute a list of queries separated by an space. i.e --queries_names a b c')
        group.add_argument('--query_name', dest='query_name', help='Execute a query defined in queries.py')

        args = parser.parse_args()
        self.validate_args(args)
        return args

    def validate_args(self,args):
        ''' Validate that the query or queries passed by CLI args are valid'''
        if QUERY_ALL in args.query_name:
            return
        exist = self.query_exist(args.query_name)
        if len(exist) > 0:
            print "The following queries are not registered: {}".format(', '.join(map(str, exist)))
            exit(1)

    def query_exist(self,queries_to_check):
        ''' Will check if the query is defined at queries.py file'''
        invalid_queries = []

        queries_registered = QUERIES.keys()
        for query in queries_to_check:
            if query in queries_registered:
                continue
            else:
                invalid_queries.append(query)
        return invalid_queries

    def retrieve_query(self,query_to_lookup):
        ''' Will retrieve the query statement to be executed only if enabled'''
        if QUERIES.get(query_to_lookup) and QUERIES[query_to_lookup][1]:
            return QUERIES[query_to_lookup][0]
        else:
            return None

    def execute_queries(self,queries):
        ''' Will execute each query on the "queries" list
           if the query is on SPECIAL_QUERY it will call the method defined over the script
           else it will execute the regular query'''
        if QUERY_ALL in queries:
            queries = QUERIES.keys()
        for query in queries:
            if query in SPECIAL_QUERY:
                getattr(self, query)(query)
            else:
                statement = self.retrieve_query(query)
                if statement is not None:
                    print "Executing query_name:{}\nQuery: {}".format(query,statement)
                    rows, col_names = self.DB.execute_query(statement)
                    print format_result(deque(col_names), rows)
                else:
                    print "It looks like query: {} does not exist or it's disabled".format(query)

    def rows_per_table(self, query):
        ''' Will loop through the TABLES list and execute the same query for each table'''
        for table in TABLES:
            statement = self.retrieve_query(query)
            if statement is not None:
                st = statement.format(table)
                rows, col_names = self.DB.execute_query(st)
                print "Table: {}".format(table)
                print format_result(deque(col_names), rows)

    def street_types(self, query):
        ''' Will loop in street types cursor and find uniqueness'''
        st_types = set()
        statement = self.retrieve_query(query)
        if statement is not None:
            rows, col_names = self.DB.execute_query(statement)
        for row in rows:
            if row[0].split()[-1] in expected:
                st_types.add(row[0].split()[-1])
        print "Streets types"
        print "\n".join(st_types)


def format_result(col_names, rows):
    ''' It will format the result of the query with a table shape'''
    ptt=PrettyTable()
    ptt.padding_width = 1
    idx = 0
    while len(col_names) > 0:
        col_name = col_names.popleft()
        if len(col_names) == 0:
            # format(row[idx], ',d')
            ptt.add_column(col_name, [ "{}".format(str(row[idx])) for row in rows])
            ptt.align[col_name]="r"
        else:
            ptt.add_column(col_name,[row[idx] for row in rows])
            ptt.align[col_name]="l"
        idx += 1
    return ptt

def print_file_size():
    ''' It will print the size of each file'''
    files = ['dublin.osm', NODES_PATH ,NODE_TAGS_PATH, WAYS_PATH, WAY_NODES_PATH, WAY_TAGS_PATH]
    file_sizeMB = []
    for file in files:
        file_size = os.path.getsize(file)
        format_str = "{} {}MB\n".format(file, float(file_size >> 20))
        file_sizeMB.append(format_str)
    print textwrap.dedent('''\
|--------------------------
| Size of Files
|--------------------------
| {}---------------------------'''.format("| ".join(file_sizeMB)))


if __name__ == '__main__':
    queries = QUERY()
    args = queries.main()

    # Get size of files
    print_file_size()

    # Now let's have fun executing queries
    queries.execute_queries(args.query_name)
