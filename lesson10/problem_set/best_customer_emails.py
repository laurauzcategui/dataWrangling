##  The customer who has spent the most money will be declared your best customer.
##  They definitely deserve an email thanking them for their patronage :)

##  Build a query that returns the person who has the highest sum of all invoices,
##  along with their email, first name, and last name.


QUERY ='''
SELECT c.Email, c.FirstName,c.LastName, sum(i.Total) Total
from customer c, invoice i on c.CustomerId = i.CustomerId
group by c.CustomerId
order by Total desc
limit 1;
'''

'''
---VISUAL GUIDE---

Before Query...

###############         ####################
#  Customer   #         #     Invoice      #
###############         ####################
|  CustomerId | = ON  = | CustomerId       |  <-----  FROM/JOIN
+=============+         +==================+
|  FirstName  |         | Total            |  <-----  sum Total and limit
+=============+         +==================+          to highest sum
|  LastName   |
+=============+
|  Email      |
+=============+

After Query...

###################################################
#             CustomerInvoice                     #   <-----  RESULT!
###################################################
|  Email  |  FirstName | LastName    |    Total   |
+=========+============+=============+============+

'''









    
