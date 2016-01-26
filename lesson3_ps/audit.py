#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up. In the first exercise we want you to audit
the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- NoneType if the value is a string "NULL" or an empty string ""
- list, if the value starts with "{"
- int, if the value can be cast to int
- float, if the value can be cast to float, but CANNOT be cast to int.
   For example, '3.23e+07' should be considered a float because it can be cast
   as float but int('3.23e+07') will throw a ValueError
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and a
SET of the types that can be found in the field. e.g.
{"field1: set([float, int, str]),
 "field2: set([str]),
  ....
}

All the data initially is a string, so you have to do some checks on the values
first.
"""
import codecs
import csv
import json
import pprint
import pandas as pd

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode", "populationTotal",
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long",
          "areaLand", "areaMetro", "areaUrban"]


def audit_file(filename, fields):
    fieldtypes = {}
    listtypes = []
    x = 0
    # YOUR CODE HERE
    df = pd.read_csv(filename)
    df_cities = pd.DataFrame(df,columns=FIELDS)
    for field in fields:
        for elem in df_cities[field]:
            if (elem == "NULL" or elem == "") and (NoneType not in listtypes):
                listtypes.append(NoneType)
            else if elem.startswith('{') and list not in listtypes:
                listtypes.append(list)
            else if type(elem) == float:
                try:
                    x = int(elem)
                    if int not in listtypes:
                        listtypes.append(int)
                except ValueError:
                    if float not in listtypes:
                        listtypes.append(float)
            else
                if str no in listtypes:
                    listtypes.append(str)
        fieldtypes[field] = set(listtypes)
        listtypes = []
    '''
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            for i,field in enumerate(fields):
                if (row[i] == "NULL" or row[i] == "") and (NoneType not in listtypes):
                    listtypes.append(NoneType)
                else if row[i].startswith('{') and list not in listtypes:
                    listtypes.append(list)
                else if type(row[i]) == float:
                    try:
                        x = int(row[i])
                        if int not in listtypes:
                            listtypes.append(int)
                    except ValueError:
                        if float not in listtypes:
                            listtypes.append(float)
                else
                    if str no in listtypes:
                        listtypes.append(str)
    '''

    return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])

if __name__ == "__main__":
    test()
