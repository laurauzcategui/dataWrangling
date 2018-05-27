##  The show was a huge hit! Congratulations on all your hard work :)
##  After the popularity of your first show you've decided to jump on the
##  railway for an Alternative & Punk tour through France!

##  What does the alternative punk scene look like throughout French
##  cities in your dataset?

##  Return the BillingCities in France, followed by the total number of
##  tracks purchased for Alternative & Punk music.
##  Order your output so that the city with the highest total number of
##  tracks purchased is on top.


QUERY = '''
SELECT i.BillingCity, count(t.TrackId) NumTracks
FROM Invoice i, InvoiceLine l, Track t, Genre g
ON i.InvoiceId = l.InvoiceId AND
   l.TrackId = t.TrackId AND
   t.GenreId = g.GenreId
WHERE i.BillingCountry = 'France' AND
g.Name = 'Alternative & Punk'
GROUP BY i.BillingCity
order by NumTracks desc
'''


'''
---Visual Guide---

Before Query...

#################       #################       #############      #############
#    Invoice    #       #  InvoiceLine  #       #   Track   #      #   Genre   #
#################       #################       #############      #############
|  InvoiceId    | --->  |  InvoiceId    |       |  GenreId  | ---> |  GenreId  |
+---------------+       +---------------+       +-----------+      +-----------+
|  BillingCity| |       |  TrackId      |  ---> |  TrackId  |      |  Name     |
+---------------+       +---------------+       +-----------+      +-----------+
| BillingCountry|
+---------------+

After Query..

###############################
#        InvoiceGenre         #
###############################
|  BillingCity  |  NumTracks  |
+---------------+-------------+

'''
