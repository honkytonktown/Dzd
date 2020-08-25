import psycopg2

#define postgre db config
hostname = 'localhost'
username = 'postgres'
password = 'nicetry'
database = 'GenomeData'
port = 5432
msg = ("Connecting to database: host: {}, port: {}, dbname: {}").format(hostname, port, database)
print (msg)
#Provides a connection to postgre server. Used throughout the program
#try catch me
conn = psycopg2.connect( host=hostname, port = port, user=username, password=password, dbname=database )


def close_connection(): 
    """ close_connection closes postgres db connection """
    conn.close()

