#This module inserts data from CollectionsData.csv into Postgres DB table

import os
import psycopg2
import Config.Config as config
import csv
import pandas as pd
import Tables.CreateCollData
import DataHelper.DataHelperColl as dhc

#insertData receives a row and inserts it into sql table
def insertData(row, Columns):
    cur = config.conn.cursor()
    SQLInsert = """ INSERT INTO public."CollectionsData"({}, {}, {}, {}) VALUES (%s, %s, %s, %s); """.format(Columns[0], Columns[1], Columns[2], Columns[3])
    data = (row[0], row[1], row[2], row[3])
    cur.execute(SQLInsert, data) 
    config.conn.commit()

#pushData iterates over df rows and calls insertData
#to insert them into sql table
def pushData(df, Columns):
    for i,row in df.iterrows():
        insertData(row, Columns)

#createTable creates a table for the data to be pushed to
def createTable(df):
    cur = config.conn.cursor()
    cmd = Tables.CreateCollData.createTable
    cur.execute(cmd)
    config.conn.commit()

#clctDataHandler is main func of this module
#if mode == 1, it will read, format csv and push the data to a sql table
#if mode == 0 itll read, format and print csv data
def collDataHandler(mode, CsvPath):
    print("Uploading CollectionsData...")
    msg = "The clctDataHandler is set to mode: {}".format(mode)
    print (msg)

    try: 
        df = pd.read_csv(os.path.join(CsvPath))
    except IOError as e:
        print (e)
        raise

    print("Dataframe column names: ")
    print(df.columns.values)

    Columns = ["sampid", "hid", "isolate", "datecollected"]
    print("Dataframe desired column names: ")
    print(Columns)

    print("Formating data...")
    df = dhc.dataHandlerColl(df)
    print("New dataframe column names: ")
    print(df.columns.values)

    if (mode == 0):
        print(df)
    elif (mode == 1):
        print("Creating table...")
        createTable(df)
        print("Pushing data to SQL db...")
        pushData(df, Columns)
    print("Done uploading CollectionsData")

    

