#!/usr/bin/env python
"""
Your task is as follows:
- read the provided Excel file
- find and return the min, max and average values for the COAST region
- find and return the time value for the min and max entries
- the time values should be returned as Python tuples

Please see the test function for the expected return format
"""

import xlrd
import numpy as np
from zipfile import ZipFile
import pprint

datafile = "2013_ERCOT_Hourly_Load_Data"
filename = "2013_ERCOT_Hourly_Load_Data.xls"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()

def find_row(value,sheet):
    for row in range(sheet.nrows):
        if row != 0:
            if sheet.cell_value(row,1) == value:
                return row

def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)

    data = {
            'maxtime': (0, 0, 0, 0, 0, 0),
            'maxvalue': 0,
            'mintime': (0, 0, 0, 0, 0, 0),
            'minvalue': 0,
            'avgcoast': 0
    }

    coast = sheet.col_values(1, start_rowx=0, end_rowx=None)

    data['avgcoast'] = np.mean(coast[1:])
    data['maxvalue'] = np.amax(coast[1:])
    data['minvalue'] = np.amin(coast[1:])

    max_time = sheet.cell_value(find_row(data['maxvalue'],sheet), 0)
    min_time = sheet.cell_value(find_row(data['minvalue'],sheet), 0)

    #find row can be done with: .index function
    # coast.index(data['maxvalue'])
    # coast.index(data['minvalue'])

    data['maxtime'] = xlrd.xldate_as_tuple(max_time, 0)
    data['mintime'] = xlrd.xldate_as_tuple(min_time, 0)


    return data

def test():
    open_zip(datafile)
    data = parse_file(filename)

    assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)
    assert round(data['maxvalue'], 10) == round(18779.02551, 10)


open_zip(datafile)
data = parse_file(filename)
pprint.pprint(data)
print test()
