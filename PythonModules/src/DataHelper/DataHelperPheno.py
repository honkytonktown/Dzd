#DataHelper parses data to apply rules from rules table
import Config.Config as config
import DataHelper.ApplyRules
import pandas as pd

def get_matching_rules():
    """ getMatchingRules pulls the matching rules table from db and saves them in a dataframe """
    SQLSelect = pd.read_sql_query(""" SELECT * FROM public."MatchingRules" """, config.conn)
    dfRules = pd.DataFrame(SQLSelect, columns=['columnname','replacementphrase', 'regexpattern'])
    return dfRules

def remove_iso(item):
    """ removeISO helper function to remove ISO from isolate """
    item = item.replace("ISO", "")
    return item

def format_cols_pheno(df): 
    """ formatData is where the raw csv data is modified to match db standards """
    df.columns = ["hid", "isolate", "received", "organism", "source", "test","antibiotic", "value", "antibioticinterpretation", "method"]


def format_rows_pheno(df, dfRules): 
    """ format_rows_pheno begins applying the matching rules. This is where table from SetupDataRules.py
        is used. If the cell is in an antibiotic column, use rules that are specific
        to antibiotics when it goes into the ApplyRules.handler function.
        If its an organism cell... etc...
        It then converts to strings and removes whitespaces
        see: ApplyRules.handler """ 
    df['isolate'] = df['isolate'].apply(remove_iso)

    #moving this out here to reduce load in DataHelper.ApplyRules
    dfRuleSet = dfRules.loc[(dfRules['columnname'] == 'antibiotic')]
    df['antibiotic'] = df['antibiotic'].apply(lambda x: DataHelper.ApplyRules.match_rules(x, dfRuleSet))

    dfRuleSet = dfRules.loc[(dfRules['columnname'] == 'organism')]
    df['organism'] = df['organism'].apply(lambda x: DataHelper.ApplyRules.match_rules(x, dfRuleSet))

    df = df.astype(str)
    df = df.applymap(lambda x: x.strip())

 
def data_handler_pheno(df):
    """ dataHandlerPheno handles the process of cleaning the data
        set column names and apply cell rules. """
    dfRules = get_matching_rules()
    format_cols_pheno(df)
    format_rows_pheno(df, dfRules)
    #pd.set_option('display.max_rows', None)
    #pd.set_option('display.max_columns', None)
    #print(df)
    return df
