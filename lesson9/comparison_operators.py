#
# Find all the llamas born between January 1, 1995 and December 31, 1998.
# Fill in the 'where' clause in this query.

QUERY = '''
SELECT *
FROM animals
where birthdate > '1995-01-01' and birthdate < '1999-01-01'
and species = 'llama'
'''
