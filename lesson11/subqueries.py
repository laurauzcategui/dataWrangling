# Find the players whose weight is less than the average.
#
# The function below performs two database queries in order to find the right players.
# Refactor this code so that it performs only one query.
#

def lightweights(cursor):
    """Returns a list of the players in the db whose weight is less than the average."""
    # cursor.execute("select name, weight from players where weight < (select avg(weight) as av from players)")
    # also as
    cursor.execute("select name, weight from players, (select avg(weight) as av from players) as subq where weight < av")
    return cursor.fetchall()
