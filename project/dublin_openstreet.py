#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import cerberus
import schema
import csv
import codecs
import pprint
from dublin_db import DB

OSMFILE = "dublin.osm"
DB_NAME = "dublin"

PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

street_type_re = re.compile(r'\b\S+\.?\s\b\S+\.?$', re.IGNORECASE)

# Expected Street types to map
expected = ["Street Lower", "Street", "Street Crescent", "Street Upper", "Street West", "Street East", "Street South","Street Little","Street North",
            "Avenue", "Avenue Upper", "Avenue Lower", "Place East", "Place West","Place Little", "Mews","Place South","Street Great", "Village", "Paddock",
            "Boulevard", "Drive", "Court", "Place", "Square", "Square North", "Square West", "Square East","Square South", "Lane",
            "Trail", "Parkway", "Commons", "Villas", "Terrace", "Cottages", "Park", "Quay", "Hill", "Grove", "Avenue Lower", "Place North",
            "Road Upper", "Road Lower", "Road", "Road West", "Road North", "Road South", "Road East",
            "Street Upper", "Lane South", "Lane East", "Lane North", "Lane West", "Lawn", "Lane Upper",
            "Grove North", "Grove South", "Dock", "Quay Lower", "Quay Upper", "Crescent", "Gardens", "Mews End", "View", "Place Upper"]

# If any mapping with the keys below appears we suggest a change to th values corresponding to that key
MAPPING = { "St": "Street",
            "St.": "Street",
            "Rd.": "Road",
            "Ave": "Avenue",
            "Ln": "Lane",
            "Rd": "Road"
            }

SCHEMA = schema.schema

#files to write schemas to
NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

# List of String Fields to transform
STRING_FIELDS = { 'node': ['user','timestamp'],
                  'ways': ['user', 'version', 'timestamp'],
                  'node_tags': ['key', 'value', 'type'],
                  'ways_tags': ['key','value', 'type'] }

def audit_street_type(street_types, street_name):
    ''' Perform an audit if the street name is expected or not
        :param street_types: Set to update with unxpected street types
        :param street_name: street name to audit
    '''
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        split_street = street_type.split(' ')
        if street_type in expected:
            return
        if (split_street[0] in expected and split_street[1] not in expected):
            street_types[street_type].add(street_name)

def is_street_name(elem):
    ''' Validate if the k attrib is type addr:street'''
    return (elem.attrib['k'] == "addr:street")

def audit(osmfile):
    ''' Perform an audit on the file to parse
        It will iterate over the tree with Start events only and
        tag type node or way.

        param: osmfile to audit
        return: a set of street types
    '''
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    print "finish audit"
    return street_types

def update_name(name):
    ''' Update the name of the street based on MAPPING map defined above
        param: name of the street to update
        return: suggested name
    '''
    names = name.split(' ')
    for idx, word in enumerate(names):
        if MAPPING.get(word):
            names[idx] = MAPPING[word]
            break
    nameit = ' '.join(names)
    return nameit

def does_not_have_problemchars(element):
    ''' It will discard all tags with problematic charts defined in PROBLEMCHARS regex
        param: element to verify if contains problematic char
        return: True if does not contain problematic chars, False otherwise
    '''
    k = element.attrib['k']
    prob_chars = PROBLEMCHARS.search(k)
    if prob_chars:
        return False
    return True

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    way_tags = []
    node_tags = []

    if element.tag == 'node':
        scan_and_update_attribs(node_attr_fields, element, node_attribs, 'node')
        update_tags(element, node_tags, 'node_tags')
        return { 'node': node_attribs, 'node_tags': node_tags }
    elif element.tag == 'way':
        scan_and_update_attribs(way_attr_fields, element, way_attribs, 'ways')
        build_way_nodes(element, way_nodes)
        update_tags(element, way_tags, 'ways_tags')
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': way_tags}

def build_way_nodes(elem, way_nodes):
    ''' Build the way_nodes list of dictionaries
        param: elem to lookup the nd tag
        param: way_nodes list to update
    '''
    pos_idx = 0
    for nd in elem.iter('nd'):
        if nd.attrib['ref']:
            way_nodes.append({'id': elem.attrib.get('id'), 'node_id': nd.attrib.get('ref'), 'position': pos_idx })
            pos_idx += 1

def to_str(attr_key, attr_value, type):
    if attr_key in STRING_FIELDS[type]:
        #attr_value = attr_value.replace("'","''")
        return attr_value.encode('utf-8')
    return attr_value

def scan_and_update_attribs(attr_fields, element, attribs, type):
    ''' Generic method to update attribute fields and update the attribs dictionary
        param: attr_fields list of attributes to lookup
        param: element to lookup the attribute
        param: attribs dictionary to update
    '''
    for attrib in attr_fields:
        if element.attrib[attrib]:
            attribs[attrib] = to_str(attrib, element.attrib.get(attrib),type)

def update_tags(element, tags, tag_type):
    ''' build tags list according to the element that is being passed '''
    for tag in element.iter('tag'):
        if tag.attrib['k'] and does_not_have_problemchars(tag):
            key, type = split_key_type(tag.attrib['k'])
            value = to_str('value', tag.attrib['v'], tag_type)
            key = to_str('key', key, tag_type)
            type = to_str('type', type, tag_type)
            tags.append({ 'id' : element.attrib.get('id') , 'key': key, 'value': value, 'type': type})

def split_key_type(elem, default_tag_type='regular'):
    ''' It will split the keys and key type based on the number of ":" it has
        if the number of : is greater than 1, it will split by character storing in
        element 0 of the list the type and in element 1 the key

        param: key to evaluate and split
        return: key, type values
    '''
    if elem.count(":") > 1:
        splits = elem.split(":", 1)
        # return key, type
        return splits[1],splits[0]
    elif elem.count(":") == 1:
        splits = elem.split(":")
        return splits[1], splits[0]
    return elem, default_tag_type

# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)

        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def update_street_type(element):
    audit(element)


def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate:
                    validate_element(el, validator)
                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])

if __name__ == '__main__':
    # let us first audit and update the dataset accordingly
    st_types = audit(OSMFILE)
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name)
            print name, "=>", better_name

    # It will process the map that is defined on the top as OMSFILE
    process_map(OSMFILE, validate=True)

    # let's create the DB and generate the tables
    dublin_db = DB(DB_NAME)
    dublin_db.create_tables()
    dublin_db.insert_records()
