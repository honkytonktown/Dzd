#Dzd specific rules
    #determine what signs mean
    #extract the numerical values out
    
    #When organism == Escherichia coli
    #If Value <=4: Susceptible
    #If 4 < Value < 16: Intermediate
    #If Value >=16: Resistant

import re
import pandas as pd

def setResponse(value, dfRuleSet):
    if not dfRuleSet.empty:
        susceptible = float(dfRuleSet['susceptible'].values[0])
        intermediatelow = float(dfRuleSet['intermediatelow'].values[0])
        intermediatehigh = float(dfRuleSet['intermediatehigh'].values[0])
        resistant = float(dfRuleSet['resistant'].values[0])
        if (value <= susceptible):
            return responses[0]
        elif(value > intermediatelow and value < intermediatehigh):
            return responses[1]
        elif(value >= resistant):
            return responses[2]
    #if there is no rule set, return there is no match
    else:
        return responses[3]

def extractNum(value):
    #print(value)
    #this regex finds integers and floats in provided string
    numValue = re.search(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', value).group(1)
    if numValue is not None:
        return numValue
    else: 
        #This should not happen
        return "NaN"

def lessThan(value, dfRuleSet):
    temp = extractNum(value)
    tempF = float(temp)
    #<4 returns 4, so need to reduce value slightly
    #for inequality to remain true (ie. 4 < 4 is false)
    tempF = tempF - 0.01  
    return setResponse(tempF, dfRuleSet)

def greaterThan(value, dfRuleSet):
    temp = extractNum(value)
    tempF = float(temp)
    #>4 returns 4, so need to bump value slightly
    #for inequality to remain true
    tempF = tempF + 0.01  
    return setResponse(tempF, dfRuleSet)     

def lessThanOrEqual(value, dfRuleSet):
    temp = extractNum(value)
    tempF = float(temp)
    return setResponse(tempF, dfRuleSet)

def greaterThanOrEqual(value, dfRuleSet):
    temp = extractNum(value)
    tempF = float(temp)
    return setResponse(tempF, dfRuleSet)  

def numWithUnits(value, dfRuleSet):
    temp = extractNum(value)
    tempF = float(temp)
    return setResponse(tempF, dfRuleSet) 

def funcMap(value, id, dfRuleSet):
    if id == 0:
        response = lessThanOrEqual(value, dfRuleSet)
        return response
    elif id == 1:
        response = greaterThanOrEqual(value, dfRuleSet)
        return response
    elif id == 2:
        response = lessThan(value, dfRuleSet)
        return response
    elif id == 3:
        response = greaterThan(value, dfRuleSet)
        return response 
    elif id == 4:
        response = numWithUnits(value, dfRuleSet)
        return response

responses = ["Susceptible", "Intermediate", "Resistant", "No matching rule", "Value has no nums"]

#common 'value' formats
regexArray = [
    [re.compile(r'(<=.*)'), 0],
    [re.compile(r'(>=.*)'), 1],
    [re.compile(r'<(\?!=)'), 2],
    [re.compile(r'>(\?!=)'), 3],
    [re.compile(r'(?=.*ug.*)'), 4]
]

def applyLogic(value, organism, method, antibiotic, dfRules):
    #selecting appropriate rule for the current row
    dfRuleSet = dfRules.loc[(dfRules['organism'] == organism) & (dfRules['antibiotic'] == antibiotic) & (dfRules['method'] == method)]
    # if not dfRuleSet.empty:
    #     print (dfRuleSet)
    #if str contains no nums return immediately
    if value.isalpha():
        return responses[4]
    #if str contains only nums jump to setResponse
    if value.isnumeric():
        temp = extractNum(value)
        tempF = float(temp)
        response = setResponse(tempF, dfRuleSet)
        return setResponse(tempF, dfRuleSet)

    #regex[0] is regex pattern
    #regex[1] is mapper identification num
    for regex in regexArray:
        n = regex[0].match(value)
        if (type(n) == re.Match):
            return funcMap(value, regex[1], dfRuleSet)

    return "Did not match any regex"

