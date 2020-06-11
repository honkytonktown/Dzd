#Dzd specific rules
    #determine what signs mean
    #extract the numerical values out
    
    #When organism == Escherichia coli
    #If Value <=4: Susceptible
    #If 4 < Value < 16: Intermediate
    #If Value >=16: Resistant

import re
import pandas as pd

#setResponse, if there is a matching rule set, applies new inequality comparisons
#to value. It compares existing value to appropriate value determined in dzd rules
def setResponse(value, dfRuleSet):
    if not dfRuleSet.empty:
        if (value <= float(dfRuleSet['susceptible'].values[0])):
            return responses[0]
        elif(value > float(dfRuleSet['intermediatelow'].values[0]) and value < float(dfRuleSet['intermediatehigh'].values[0])):
            return responses[1]
        elif(value >= float(dfRuleSet['resistant'].values[0])):
            return responses[2]
    #if there is no rule set, return there is no match
    else:
        return responses[3]

#extractNum runs regex pattern against value to extract any number
def extractNum(value):
    try:
        numValue = re.search(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', value).group(1)
        if numValue is not None:
            return float(numValue)
    except: 
        msg = "Failed to find numerical value within: {}".format(value)
        return (msg)

#<4 returns 4 from extractNum, so need to reduce value slightly
#for inequality to remain true - (ie. 4 < 4 is false, but 3.99 < 4 is not)
def lessThan(value, dfRuleSet):
    temp = extractNum(value)
    temp -= 0.01  
    return setResponse(temp, dfRuleSet)

#>4 returns 4 from extractNum, so need to bump value slightly
#for inequality to remain true
def greaterThan(value, dfRuleSet):
    temp = extractNum(value)
    temp += 0.01  
    return setResponse(temp, dfRuleSet)     

#simpleHandler handles regex patterns that don't require modification
def simpleHandler(value, dfRuleSet):
    temp = extractNum(value)
    return setResponse(temp, dfRuleSet)

responses = ["Susceptible", "Intermediate", "Resistant", "No matching rule", "Value has no nums"] 

#mapper assigns a function to the regex pattern
#original matching function was part of list w/ the regex pattern
#but functions were being executed when the list was declared,
#slowing down the process
def mapper(id, value, dfRuleSet):
    if id == 0:
        return simpleHandler(value, dfRuleSet)
    elif id == 1:
        return lessThan(value, dfRuleSet)
    elif id == 2:
        return greaterThan(value, dfRuleSet)

#applyLogic deduce 'value' column through series of steps.
#Values containing only strings are returned immediately.
#Values that are just numbers jump to
def applyLogic(value, organism, method, antibiotic, dfRules):
    dfRuleSet = dfRules.loc[(dfRules['organism'] == organism) & (dfRules['antibiotic'] == antibiotic) & (dfRules['method'] == method)]
    if value.isalpha():
        return responses[4]

    elif value.isnumeric():
        return simpleHandler(value, dfRuleSet)

    #Logic: if string match regex pattern, call corresponding function
    #these could be refined more by combining the three that work the same way
    regexArray = [
                [re.compile(r'(<=.*)'), 0],
                [re.compile(r'(>=.*)'), 0],
                [re.compile(r'<(\?!=)'), 1],
                [re.compile(r'>(\?!=)'), 2],
                [re.compile(r'(?=.*ug.*)'), 0]
                ]
    for regexPair in regexArray:
        temp = regexPair[0].match(value)
        if (type(temp) == re.Match):
            return mapper(regexPair[1], value, dfRuleSet)

    return "Did not match any regex"

