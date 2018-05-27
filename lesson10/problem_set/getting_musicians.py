##  Now that we know that our customers love rock music, we can decide which musicians to
##  invite to play at the concert.

##  Let's invite the artists who have written the most rock music in our dataset.
##  Write a query that returns the Artist name and total track count of the top 10 rock bands.


QUERY ='''
SELECT A.Name, count(g.Name) as counter
FROM Artist a, Album b, Track t, Genre g
ON a.ArtistId = b.ArtistId AND
   b.AlbumId = t.AlbumId AND
   t.GenreId = g.GenreId
where g.Name = 'Rock'
group by A.ArtistId
order by counter desc
limit 10;

'''

'''
---Visual Guide---

Before Query...

#############      #############      #############      ############
#    Genre  #      #   Track   #      #   Album   #      #  Artist  #
#############      #############      #############      ############
|  GenreId  | ---> |  GenreId  |      |  ArtistId  | --->| ArtistId |
+-----------+      +-----------+      +-----------+      +----------+
|  Name     |      |  AlbumId   |---> |  AlbumId  |      |  Name    |
+-----------+      +-----------+      +-----------+      +----------+

After Query...

#######################################
#             GenreArtist             #
#######################################
|  Artist.Name  |  COUNT(Genre.Name)  |
+---------------+---------------------+

'''
