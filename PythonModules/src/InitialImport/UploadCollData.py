#This module inserts data from CollectionsData.csv into Postgres DB table

import os
import psycopg2
import Config.Config as config
import csv
import pandas as pd
import Tables.CreateCollData
import DataHelper.DataHelperColl as dhc

def insert_data(row, Columns):
    """ insert_data receives a row and inserts it into sql table """
    cur = config.conn.cursor()
    SQLInsert = """ INSERT INTO public."CollectionsData"({}, {}, {}, {}) VALUES (%s, %s, %s, %s); """.format(Columns[0], Columns[1], Columns[2], Columns[3])
    data = (row[0], row[1], row[2], row[3])
    cur.execute(SQLInsert, data) 
    config.conn.commit()

def push_data(df, Columns):
    """ push_data iterates over df rows and calls insertData
        to insert them into sql table """
    for i,row in df.iterrows():
        insert_data(row, Columns)

def create_table(df):
    """ create_table creates a table for the data to be pushed to """
    cur = config.conn.cursor()
    cmd = Tables.CreateCollData.createTable
    cur.execute(cmd)
    config.conn.commit()


def coll_data_handler(mode, CsvPath):
    """ coll_data_handler is main func of this module
        if mode == 1, it will read, format csv and push the data to a sql table
        if mode == 0 itll read, format and print csv data
    print("Uploading CollectionsData...") """ 
    msg = "The coll_data_handler is set to mode: {}".format(mode)
    print (msg)

    try: 
        df = pd.read_csv(os.path.join(CsvPath), skipinitialspace=True)
    except IOError as e:
        print (e)
        raise

    print("Dataframe column names: ")
    print(df.columns.values)

    Columns = ["sampid", "hid", "isolate", "datecollected"]
    print("Dataframe desired column names: ")
    print(Columns)

    print("Formating data...")
    df = dhc.data_handler_coll(df)
    print("New dataframe column names: ")
    print(df.columns.values)

    if (mode == 0):
        print(df)
    elif (mode == 1):
        print("Creating table...")
        create_table(df)
        print("Pushing data to SQL db...")
        push_data(df, Columns)
    print("Done uploading CollectionsData")

    

