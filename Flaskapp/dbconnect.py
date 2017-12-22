import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",user = "root",passwd = "subbusummu",db = "miniproject")
    c = conn.cursor()

    return c, conn
		