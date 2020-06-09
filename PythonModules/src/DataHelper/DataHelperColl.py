#DataHelper parses data to apply rules from rules table




def formatColsColl(df): 
    df.columns = ["sampid", "hid", "isolate", "datecollected"]

def formatRowsColl(df): 
    df['isolate'] = df['isolate'].fillna(1)
    df['isolate'] = df['isolate'].astype(int)
    
def dataHandlerColl(df):
    formatColsColl(df)
    formatRowsColl(df)
    return df
