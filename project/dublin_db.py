import sqlite3
import csv
from subprocess import call
import re

TABLES = ['nodes', 'nodes_tags', 'ways', 'ways_tags', 'ways_nodes']

class DB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.tables = {
            'nodes': { 'fields': "(id, lat, lon, user, uid, version, changeset, timestamp)",
                       'values': '(?,?,?,?,?,?,?,?)' },
            'nodes_tags': { 'fields': "(id, key, value, type)",
                            'values': '(?,?,?,?)' },
            'ways': { 'fields': "(id, user, uid, version, changeset, timestamp)",
                      'values': '(?,?,?,?,?,?)'},
            'ways_tags': { 'fields': "(id, key, value, type)",
                           'values': '(?,?,?,?)' },
            'ways_nodes': { 'fields': "(id, node_id, position)",
                            'values': '(?,?,?,?)' }
        }

    def connect_to_db(self):
        ''' It will create a db connection with the db_name
            return: connection
        '''
        if self.connection is None:
            try:
                self.connection = sqlite3.connect("{}.db".format(self.db_name))
            except Error as e:
                print e

    def drop_table_if_exist(self, table):
        ''' It will drop the table pass as argument only if exists
            param: table name to drop from DB
        '''
        self.connect_to_db()
        # Get a cursor object
        cursor = self.connection.cursor()
        drop_table_sql = "DROP TABLE IF EXISTS {}".format(table)
        cursor.execute(drop_table_sql)

    def drop_all_tables(self):
        ''' It will drop all the tables defined in TABLES array'''
        for table in TABLES:
            self.drop_table_if_exist(table)

    def create_tables(self, schemas_file='schema.sql'):
        ''' It will create the tables defined in the file you pass by parameter
            param: schemas_file containing the table(s) definition
        '''
        # let us drop all tables first before creation. If you are passing a different table
        # TABLES array needs to be updated
        self.drop_all_tables()
        print "Creating tables at db:{}.db".format(self.db_name)
        command = "cat {} | sqlite3 {}.db".format(schemas_file, self.db_name)
        call(command, shell=True)

    def insert_records(self, sqlite3_file='insert_records.sqlite3'):
        ''' It will insert all records generated in csv files
            param sqlite3_file will contain all imports of csv to tables
            Update sqlite3_file accordingly if you are adding new tables
        '''
        print "Inserting records at db: {}.db, tables at:{}".format(self.db_name,sqlite3_file)
        command = "cat {} | sqlite3 {}.db".format(sqlite3_file, self.db_name)
        call(command, shell=True)

    def close_connection(self):
        ''' Close the connection but first check if it's open'''
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def execute_query(self, query_statement):
        ''' It will execute a query passed by parameter
            param: query_statement is a string with query to be executed
            return: a list with the result of executing the statement'''

        # get a cursor
        cursor = self.connection.cursor()
        # execute the query
        cursor.execute(query_statement);
        # fetch all results
        rows = cursor.fetchall()
        col_names = [cn[0] for cn in cursor.description]
        return rows, col_names
