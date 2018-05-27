##  Alright, now that you're warmed up let's get down to business!

##  In this problem set we'll pretend the Chinook database is the data for your own personal music shop!
##  We'll be marketing your shop and hosting Music Festival using answers we get from
##  the data stored in your database.
##  Let's get started :)

##  First, you'd like to run a promotion targeting the 3 countries with the
##  highest number of invoices.

##  Write a query that returns the 3 countries with the highest number of invoices, along with the number ##  of invoices for these countries.


QUERY ='''
SELECT Billingcountry, count(*) as number
from invoice
group by Billingcountry
order by number desc
limit 3;
'''

'''
---VISUAL GUIDE---
(The visual guides are meant to help show you how your queries are interacting with the database)

Before Query...

#################
#   Invoice     #              <----- FROM
#################
| BillingCountry|  COUNT(*)   <----- SELECT
+===============+

After Query...

################################
#           Invoice            #   <----- RESULT!
################################
| BillingCountry|   COUNT(*)   |
+===============+==============+
'''
