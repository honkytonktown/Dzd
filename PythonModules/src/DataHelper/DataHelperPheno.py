#DataHelper parses data to apply rules from rules table

#removeISO helper function to remove ISO from isolate
def removeISO(item):
    item = item.replace("ISO", "")
    return item

#formatData is where the raw csv data is modified to match db standards
def formatColsPheno(df): 
    df.columns = ["hid", "isolate", "received", "organism", "source", "test","antibiotic", "value", "antibioticinterpretation", "method"]

def formatRowsPheno(df): 
    #Remove ISO from Isolate
    df['isolate'] = df['isolate'].apply(removeISO)

def dataHandlerPheno(df):
    formatColsPheno(df)
    formatRowsPheno(df)
    return df
