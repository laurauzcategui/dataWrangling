##  It would be really helpful to know what type of music everyone likes before
##  throwing this festival.
##  Lucky for us we've got the data to find out!
##  We should be able to tell what music people like by figuring out what music they're buying.

##  Write a query that returns the BillingCity,total number of invoices
##  associated with that particular genre, and the genre Name.

##  Return the top 3 most popular music genres for the city Prague
##  with the highest invoice total (you found this in the previous quiz!)

QUERY ='''
SELECT I.BillingCity,count(g.Name) , g.Name
from Genre g, Track t, InvoiceLine L, Invoice I
on g.GenreId = t.GenreId and
 t.TrackId = L.TrackId and
 L.InvoiceId = I.InvoiceId
where I.BillingCity = 'Prague'
group by g.Name
order by count(g.Name) desc
limit 3;
'''

'''
---Visual Guide---

Before Query...

###############       #################       #############      #############
#  Invoice    #       #  InvoiceLine  #       #   Track   #      #   Genre   #
###############       #################       #############      #############
|  InvoiceId  | --->  |  InvoiceId    |       |  GenreId  | ---> |  GenreId  |
+-------------+       +---------------+       +-----------+      +-----------+
|  BillingCity|       |  TrackId      |  ---> |  TrackId  |      |  Name     |
+-------------+       +---------------+       +-----------+      +-----------+

After Query..

#######################################
#            InvoiceGenre             #
#######################################
|  BillingCity  |  COUNT(*)  |  Name  |
+---------------+------------+--------+

'''
