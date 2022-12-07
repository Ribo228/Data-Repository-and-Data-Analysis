import psycopg2
def createConnection():
    return psycopg2.connect(dbname='smart_db', user='smart',
    host='db', password='smart')


