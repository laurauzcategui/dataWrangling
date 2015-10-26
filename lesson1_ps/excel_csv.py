# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the regions
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file.

import xlrd
import os
import csv
from zipfile import ZipFile
import numpy as np
import pprint

#datafile = "2013_ERCOT_Hourly_Load_Data.xls"
datafile = "2013_ERCOT_Hourly_Load_Data"
filename = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"
correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                    'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()

def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = {}
    elem = {}

    for idx, r in enumerate(correct_stations):
        region = sheet.col_values(idx+1, start_rowx=1, end_rowx=None)
        elem[fields[-1]] = max(region)
        row = region.index(elem[fields[-1]])+1
        cell_time = sheet.cell_value(row, 0)
        tuple_time = xlrd.xldate_as_tuple(cell_time, 0)
        for idx_f, z in enumerate(fields[:-1]):
            elem[fields[idx_f]] = tuple_time[idx_f]
        data[r] = elem
        elem = {}
    return data

def save_file(data, filename):
    with open(outfile, 'wb') as csvfile:
        out_writer= csv.writer(csvfile, delimiter='|')
        fields.insert(0,'Station')
        out_writer.writerow(fields)
        for r in data:
            l = [data[r][f] for f in fields[1:]]
            l.insert(0,r)
            out_writer.writerow(l)

def test():
    open_zip(datafile)
    data = parse_file(filename)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)


if __name__ == "__main__":
    #open_zip(datafile)
    #data = parse_file(filename)
    #save_file(data, outfile)
    test()
