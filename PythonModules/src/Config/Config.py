import psycopg2

#define postgre db config
hostname = 'localhost'
username = 'postgres'
password = 'joe'
database = 'DzdProject'
port = 5432
msg = ("Connecting to database: host: {}, port: {}, dbname: {}").format(hostname, port, database)
print (msg)
#Provides a connection to postgre server. Used throughout the program
conn = psycopg2.connect( host=hostname, port = port, user=username, password=password, dbname=database )

#CloseConnection closes postgres db connection
def CloseConnection(): 
    conn.close()

