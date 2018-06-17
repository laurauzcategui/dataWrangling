select count(d.CustomerId) from (select c.CustomerId
FROM Customer c, Invoice i, InvoiceLine l, Track t, Genre g
ON c.CustomerId = i.CustomerId and
   i.InvoiceId = l.InvoiceId and
   l.TrackId = t.TrackId and
   t.GenreId = g.GenreId
where
g.Name = "Jazz"
group by c.CustomerId) d;
