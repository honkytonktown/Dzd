#DataHelper parses data to apply rules from rules table


def formatColsColl(df): 
    df.columns = ["sampid", "hid", "isolate", "datecollected"]

def formatRowsColl(df): 
    df['isolate'] = df['isolate'].fillna('1')
    
def dataHandlerColl(df):
    formatColsColl(df)
    formatRowsColl(df)
    df = df.astype(str)
    df = df.apply(lambda x: x.str.strip())
    return df
