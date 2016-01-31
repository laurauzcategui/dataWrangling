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

The audit_file function should return a cictionary containing fieldnames and a
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
import re
import math
import numpy as np

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode", "populationTotal",
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long",
          "areaLand", "areaMetro", "areaUrban"]


def audit_file(filename, fields):
    fieldtypes = {}
    listtypes = []
    x = 0
    is_nan = 0
    # YOUR CODE HERE
    df = pd.read_csv(filename)
    df_cities = pd.DataFrame(df,columns=FIELDS)
    for field in fields:
        for elem in df_cities.loc[3:,field]:
            try:
                float(elem) and int(elem)
                listtypes.append(int)
            except ValueError:
                try:
                    math.isnan(float(elem))
                    if float(str(elem)) != float(str(elem)):
                        is_nan = 1
                        raise ValueError
                    else:
                        listtypes.append(float)
                except ValueError:
                    if (is_nan == 1 or elem is None or type(elem) is None):
                        listtypes.append(type(None))
                        is_nan = 0
                    elif re.search('^{.*',str(elem).strip()) is not None:
                        print str(elem) + "field=" + field
                        listtypes.append(list)
                    else:
                        listtypes.append(str)
        fieldtypes[field] = set(listtypes)
        listtypes = []

    return fieldtypes

def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])

if __name__ == "__main__":
    test()
