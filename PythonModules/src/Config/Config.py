import psycopg2

hostname = 'localhost'
username = 'postgres'
password = 'Listennow55'
database = 'GenomeData'
port = 5432


msg = ("Connecting to database: host: {}, port: {}, dbname: {}").format(hostname, port, database)
print (msg)
#Provides a connection to postgre server. Used throughout the program
conn = psycopg2.connect( host=hostname, port = port, user=username, password=password, dbname=database )

def CloseConnection(): 
    conn.close()

