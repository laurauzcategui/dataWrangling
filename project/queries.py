'''
In order to facilitate and store queries executed for the Project.
I have created a dictionary of queries with the following structure
 - queries  = {

        "query_name_1": ("query_to_execute", True)
        "query_name_2": ("query_to_execute", False)
        .
        .
        .
        "query_name_n": ("query_to_execute", True)
  }


- where:
    - each key of the dictionary represents the query_name
    - the value value is a tuple with 2 elements:
        * 1st element is query to execute
        * 2nd element is a boolean that indicates if the query is enabled or not for execution.
'''

ways_vs_nodes = '''
select nt.id as node_id, nt.value as node_value, wt.id as way_id, wt.value as way_value
  from (
    select distinct wn.id as way, wn.node_id as node
    from ways_nodes wn, nodes_tags nt, ways_tags wt
    where wn.id = wt.id and wn.node_id = nt.id
  ) a, nodes_tags nt, ways_tags wt
where wt.key='street' and
      nt.key = 'street'and
      a.way = wt.id and
      a.node = nt.id and
      wt.value != nt.value;
'''

queries = {
    'rows_per_table' : ('select count(*) as row_count from {}', True),
    'count_unique_user_by_node' : ('select count(distinct(user)) as distinct_users from nodes;', True),
    'nodes_most_used_keys': ("select a.* from ( select count(key) as count, key from nodes_tags group by key order by count desc ) a where a.count >= 1000;", True),
    'nodes_count_of_streets': ("select count(value) as 'Number of Streets' from (select distinct(value) as value from nodes_tags where key='street');", True),
    'ways_most_used_keys':  ("select a.* from ( select count(key) as count, key from ways_tags group by key order by count desc ) a where a.count >= 1000;", False),
    'street_types': ("select distinct(value) as street from nodes_tags where key='street' and value not like '%Street' order by value asc;", True),
    'ways_vs_nodes':(ways_vs_nodes, True)
}
