##  Rock Music Lives on!  After the success of your recent email campaign,
##  you're interested in targeting your long standing Rock Music audience!
##  You'll need to collect a list of emails containing each of your Rock Music listeners.

##  Use your query to return the email, first name, last name, and Genre of all Rock Music listeners!
##  Return you list ordered alphabetically by email address starting with A.
##  Can you find a way to deal with duplicate email addresses so no one receives multiple emails?


QUERY ='''
SELECT distinct c.Email, c.FirstName, c.LastName, g.Name
from Customer c, Invoice i, InvoiceLine il, Track t, Genre g
on t.GenreId = g.GenreId  and
   il.TrackId = t.TrackId and
   i.InvoiceId = il.InvoiceId and
   c.CustomerId = i.CustomerId
where g.name = 'Rock'
order by c.email asc
'''

'''
---VISUAL GUIDE---

Before query...

##############     ###############     #################     ############      ###########
#  Customer  #     #  Invoice    #     #  InvoiceLine  #     #  Track   #      #  Genre  #
##############     ###############     #################     ############      ###########
| CustomerId | --> | CustomerId  |     |  TrackId      | --> | TrackId  |      |  Name   |
+============+     +=============+     +===============+     +==========+      +=========+
|  Email     |     |  InvoiceId  | --> |  InvoiceId    |     | GenreId  | -->  | GenreId |
+============+     +=============+     +===============+     +==========+      +=========+
|  FirstName |
+============+
|  LastName  |
+============+

After query...

###############################################
#                 CustomerGenre               #   <-----RESULT!
###############################################
|  Email  |  FirstName  |  LastName  | Genre  |
+=========+=============+============+========+
'''
