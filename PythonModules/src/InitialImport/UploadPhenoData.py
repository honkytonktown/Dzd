#This module inserts data from PhenotypeData.csv into Postgres DB table

import os
import psycopg2
import Config.Config as config
import csv
import pandas as pd
import Tables.CreatePhenoTable
import DataHelper.DataHelperPheno as dhp

#insertData receives a row and inserts it into sql table
def insertData(row):
    cur = config.conn.cursor()
    SQLInsert = """ INSERT INTO public."PhenotypeData"(hid, isolate, received, organism, source, test, antibiotic, value, antibioticinterpretation, method) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """
    data = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
    cur.execute(SQLInsert, data) 
    config.conn.commit()

#pushData iterates over df rows and calls insertData
#to insert them into sql table
def pushData(df):
    for i,row in df.iterrows():
        insertData(row)

#createTable creates a table for the data to be pushed to
def createTable(df):
    cur = config.conn.cursor()
    cmd = Tables.CreatePhenoTable.createTable
    cur.execute(cmd)
    config.conn.commit()

#phenoDataHandler is main func of this module
#if mode == 1, it will read, format csv and push the data to a sql table
#if mode == 0 itll simply read, format and print csv data
def phenoDataHandler(mode, CsvPath):
    print("Uploading PhenotypeData...")
    msg = "The phenoDataHandler is set to mode: {}".format(mode)
    print (msg)

    try: 
        df = pd.read_csv(os.path.join(CsvPath), skipinitialspace=True)
    except IOError as e:
        print (e)
        raise

    print("Dataframe column names: ")
    print(df.columns.values)

    Columns = ["hid", "isolate", "received", "organism", "source", "test","antibiotic", "value", "antibioticinterpretation", "method"]
    print("Dataframe desired column names: ")
    print(Columns)

    print("Formating data...")
    df = dhp.dataHandlerPheno(df)

    print("New dataframe column names: ")
    print(df.columns.values)

    if (mode == 0):
        print(df)
    elif (mode == 1):
        print("Creating table...")
        createTable(df)
        print("Pushing data to SQL db...")
        pushData(df)
    print("Done uploading PhenotypeData")

