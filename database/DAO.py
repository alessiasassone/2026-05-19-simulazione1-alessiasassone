from database.DB_connect import DBConnect
from model.Artist import Artist
from model.genre import Genre


class DAO():

    @staticmethod
    def getAllGeneri():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select * FROM Genre g"""

        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Genre(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllNodes(genere):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """SELECT a.ArtistID, a.Name
                FROM Genre g , Artist a , Album a2 , Track t 
                WHERE a.ArtistID = a2.ArtistID and a2.AlbumId = t.AlbumId and t.GenreId = g.GenreId 
                AND g.Name = %s
                group BY a.ArtistID, a.Name"""

        cursor.execute(query, (genere,))

        res = []
        for row in cursor:
            res.append(Artist(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getCustomerArtistCounts(genere):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select i.CustomerId, art.ArtistID, count(*) as ntracks
                    from invoice i, invoiceline i2, track t, genre g, artist art,album a
                    where i.InvoiceId  = i2.InvoiceId 
                    and t.TrackId = i2.TrackId 
                    and t.AlbumId = a.AlbumId
                    and g.GenreId = t.GenreId
                    and art.ArtistID = a.ArtistID
                    and g.Name = %s
                    group by i.CustomerId, art.ArtistID"""

        cursor.execute(query, (genere,))

        res = []
        for row in cursor:
            res.append((row["CustomerId"], row["ArtistID"], row["ntracks"]))

        cursor.close()
        cnx.close()
        return res

