#This module inserts data from PhenotypeData.csv into Postgres DB table

import os
import psycopg2
import Config.Config as config
import csv
import pandas as pd
import Tables.CreatePhenoTable
import DataHelper.DataHelperPheno as dhp


def insert_data(row):
    """ insert_data receives a row and inserts it into sql table """
    cur = config.conn.cursor()
    SQLInsert = """ INSERT INTO public."PhenotypeData"(hid, isolate, received, organism, source, test, antibiotic, value, antibioticinterpretation, method) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """
    data = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
    cur.execute(SQLInsert, data) 
    config.conn.commit()


def push_data(df):
    """ push_data iterates over df rows and calls insertData
        to insert them into sql table """
    for i,row in df.iterrows():
        insert_data(row)

def create_table(df):
    """ create_table creates a table for the data to be pushed to """
    cur = config.conn.cursor()
    cmd = Tables.CreatePhenoTable.createTable
    cur.execute(cmd)
    config.conn.commit()


def pheno_data_handler(mode, CsvPath):
    """pheno_data_handler is main func of this module
       if mode == 1, it will read, format csv and push the data to a sql table
       if mode == 0 itll simply read, format and print csv data
    print("Uploading PhenotypeData...") """
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
    df = dhp.data_handler_pheno(df)

    print("New dataframe column names: ")
    print(df.columns.values)

    if (mode == 0):
        print(df)
    elif (mode == 1):
        print("Creating table...")
        create_table(df)
        print("Pushing data to SQL db...")
        push_data(df)
    print("Done uploading PhenotypeData")

