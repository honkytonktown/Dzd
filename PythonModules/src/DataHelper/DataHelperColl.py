#DataHelper parses data to apply rules from rules table
#formatColsColl sets CollectionData column names.
def formatColsColl(df): 
    df.columns = ["sampid", "hid", "isolate", "datecollected"]

#formatRowsColl fills all the null cells with 1
#In production you'd use similar rules to PhenotypeData where
#values that aren't just integer isolates would be matched and replaced
def formatRowsColl(df): 
    df['isolate'] = df['isolate'].fillna('1')

#dataHandler is significantly more simple than its Phenotype counterpart
#format columns, format rows, convert to strings, remove white spaces.
def dataHandlerColl(df):
    formatColsColl(df)
    formatRowsColl(df)
    df = df.astype(str)
    df = df.apply(lambda x: x.str.strip())
    return df
