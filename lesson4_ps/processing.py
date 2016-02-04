#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with another type of infobox data, audit it, clean it,
come up with a data model, insert it into a MongoDB and then run some queries against your database.
The set contains data about Arachnid class.
Your task in this exercise is to parse the file, process only the fields that are listed in the
FIELDS dictionary as keys, and return a list of dictionaries of cleaned values.

The following things should be done:
- keys of the dictionary changed according to the mapping in FIELDS dictionary #DONE
- trim out redundant description in parenthesis from the 'rdf-schema#label' field, like "(spider)" #DONE
- if 'name' is "NULL" or contains non-alphanumeric characters, set it to the same value as 'label'. #DONE
- if a value of a field is "NULL", convert it to None #DONE
- if there is a value in 'synonym', it should be converted to an array (list)
  by stripping the "{}" characters and splitting the string on "|". Rest of the cleanup is up to you,
  eg removing "*" prefixes etc. If there is a singular synonym, the value should still be formatted
  in a list.
- strip leading and ending whitespace from all fields, if there is any #DONE
- the output structure should be as follows:
{ 'label': 'Argiope',
  'uri': 'http://dbpedia.org/resource/Argiope_(spider)',
  'description': 'The genus Argiope includes rather large and spectacular spiders that often ...',
  'name': 'Argiope',
  'synonym': ["One", "Two"],
  'classification': {
                    'family': 'Orb-weaver spider',
                    'class': 'Arachnid',
                    'phylum': 'Arthropod',
                    'order': 'Spider',
                    'kingdom': 'Animal',
                    'genus': None
                    }
}
  * Note that the value associated with the classification key is a dictionary with
    taxonomic labels.
"""
import codecs
import csv
import json
import pprint
import re

DATAFILE = 'arachnid.csv'
FIELDS ={'rdf-schema#label': 'label',
         'URI': 'uri',
         'rdf-schema#comment': 'description',
         'synonym': 'synonym',
         'name': 'name',
         'family_label': 'family',
         'class_label': 'class',
         'phylum_label': 'phylum',
         'order_label': 'order',
         'kingdom_label': 'kingdom',
         'genus_label': 'genus'}

synos = []
CLASSIFIERS = ['family','class','phylum','order','kingdom','genus']


def fix_schema_label(field):
    result = re.split('\(.*\)',field)
    return  result[0]

def fix_schema_name(name,label):
    if name == "NULL" or re.findall('\W',name):
        name = label
    return name

def fix_schema_general(field):
    if field == "NULL":
        field = None
    elif type(field) == str:
        field = field.strip()
    return field

def fix_schema_synom(field):
    fiedList = []
    if re.search('.*{.*', str(field)):
        field = [i.strip('*').strip() for i in re.split('[|]', field.strip('{').strip('}'))]
    return field

def fix_schema_class(field, classifiers):
    field['classification'] = {}
    pprint.pprint(field)
    for key,value in field.items():
        if key in CLASSIFIERS:
            field['classification'][key] = field.pop(key)
    return field

def audit_fields(value,key):
    if key == "synonym" and value != "NULL":
        synos.append(value)

def process_file(filename, fields):
    process_fields = fields.keys()
    values_fields = fields.values()
    data = []
    clasification = {}
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for i in range(3):
            l = reader.next()

        for field in reader:
            for key,value in field.items():
                if (key in process_fields):
                    #audit_fields(value,key)
                    if key == 'rdf-schema#label':
                        value = fix_schema_label(value)
                    elif key == 'name':
                        value = fix_schema_name(value,field['label'])
                    elif key == 'synonym':
                        value = fix_schema_synom(value)
                    value = fix_schema_general(value)
                    field[fields[key]] = field.pop(key)
                else:
                    field.pop(key)
            field = fix_schema_class(field, CLASSIFIERS)
            data.append(field)
    return data


def parse_array(v):
    if (v[0] == "{") and (v[-1] == "}"):
        v = v.lstrip("{")
        v = v.rstrip("}")
        v_array = v.split("|")
        v_array = [i.strip() for i in v_array]
        return v_array
    return [v]


def test():
    data = process_file(DATAFILE, FIELDS)
    print "Your first entry:"
    pprint.pprint(data[0])
    first_entry = {
        "synonym": None,
        "name": "Argiope",
        "classification": {
            "kingdom": "Animal",
            "family": "Orb-weaver spider",
            "order": "Spider",
            "phylum": "Arthropod",
            "genus": None,
            "class": "Arachnid"
        },
        "uri": "http://dbpedia.org/resource/Argiope_(spider)",
        "label": "Argiope",
        "description": "The genus Argiope includes rather large and spectacular spiders that often have a strikingly coloured abdomen. These spiders are distributed throughout the world. Most countries in tropical or temperate climates host one or more species that are similar in appearance. The etymology of the name is from a Greek name meaning silver-faced."
    }

    assert len(data) == 76
    assert data[0] == first_entry
    assert data[17]["name"] == "Ogdenia"
    assert data[48]["label"] == "Hydrachnidiae"
    assert data[14]["synonym"] == ["Cyrene Peckham & Peckham"]

if __name__ == "__main__":
    test()
