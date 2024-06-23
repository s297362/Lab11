from database.DB_connect import DBConnect
from model.arco import Arco
from model.colore import Colore
from model.prodotto import Prodotto


class DAO():
    def __init__(self):
        pass
    @staticmethod
    def getColori():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT gp.Product_color
FROM go_sales.go_products gp """
        cursor.execute(query, ())
        results = []
        for row in cursor:
            results.append(Colore(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getProdotti(colore):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
FROM go_sales.go_products gp 
WHERE gp.Product_color = %s"""
        cursor.execute(query, (colore,))
        results = []
        for row in cursor:
            results.append(Prodotto(**row))
        cursor.close()
        conn.close()
        return results
    @staticmethod
    def getArchi(p1, p2, anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT COUNT(DISTINCT s1.Date) as weight
                   FROM go_daily_sales s1, go_daily_sales s2
                   WHERE s1.Date = s2.Date
                   AND s1.Retailer_code = s2.Retailer_code
                   AND s1.Product_Number = %s 
                   AND s2.Product_Number = %s
                   AND YEAR(s1.Date) = %s 
"""
        cursor.execute(query, (p1, p2, anno,))
        results = []
        for row in cursor:
            results.append(row['weight'])
        cursor.close()
        conn.close()
        return results

