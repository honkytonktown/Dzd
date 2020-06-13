
def format_cols_coll(df): 
    """ format_cols_coll parses data to apply rules from rules table
        formatColsColl sets CollectionData column names. """
    df.columns = ["sampid", "hid", "isolate", "datecollected"]


def format_rows_coll(df): 
    """ format_rows_coll fills all the null cells with 1
        In production you'd use similar rules to PhenotypeData where
        values that aren't just integer isolates would be matched and replaced """
    df['isolate'] = df['isolate'].fillna('1')


def data_handler_coll(df):
    """ data_handler_coll formats columns, formats rows, converts to strings, removes white spaces. """
    format_cols_coll(df)
    format_rows_coll(df)
    df = df.astype(str)
    df = df.applymap(lambda x: x.strip())
    return df
