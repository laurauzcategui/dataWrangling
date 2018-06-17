select sum(d.count) from (select count(a.TrackId) as count
from Track a, Genre b, MediaType c
on a.GenreId = b.GenreId and a.MediaTypeId = c.MediaTypeId
where b.Name = 'Pop' and
      c.Name = 'MPEG audio file'
group by a.TrackId) d;
