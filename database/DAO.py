from database.DB_connect import DBConnect
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
    def getAllNodes():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """SELECT a.ArtistId 
                FROM Genre g , Artist a , Album a2 , Track t 
                WHERE a.ArtistId = a2.ArtistId and a2.AlbumId = t.AlbumId and t.GenreId = g.GenreId AND g.Name = %s
                group BY g.GenreId , a.ArtistId 
                having count(*) > 0"""

        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Genre(**row))

        cursor.close()
        cnx.close()
        return res

