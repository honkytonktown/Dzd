import re


#loop through regex patterns and find a match
#when a match is found, change x to that regex patterns value
#row[2] is regex
def matchRules(x, dfRuleSet):
    #print(dfRuleSet)
    for row in dfRuleSet.iterrows():
        result = re.search((r'{}').format(row[2]), x)
        if not result is None:
            x = row[1]   
    return x

def handler(x, dfRules, column):
    dfRuleSet = dfRules.loc[(dfRules['columnname'] == column)]
    x = matchRules(x, dfRuleSet)
    return x



