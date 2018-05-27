#
# Uncomment one of these QUERY variables at a time by deleting the #.
# Use "Test Run" to run it.
# You'll see the results below.  Then try your own queries as well!
#

QUERY = "select max(name) from animals;"

QUERY = "select * from animals limit 10;"

QUERY = "select * from animals where species = 'orangutan' order by birthdate;"

QUERY = "select name from animals where species = 'orangutan' order by birthdate desc;"

QUERY = "select name, birthdate from animals order by name limit 10 offset 20;"

QUERY = "select species, min(birthdate) from animals group by species;"

QUERY = '''
select name, count(*) as num from animals
group by name
order by num desc
limit 5;
'''
