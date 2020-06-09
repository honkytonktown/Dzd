#Dzd specific rules
    #determine what signs mean
    #extract the import values out
    #if it contains <= x then 
    #apply new rules
    
    #If Value <=4: Susceptible
    # If 4 < Value < 16: Intermediate
    #If Value >=16: Resistant

import re
import pandas as pd

def setResponse(y):
    temp = float(y)
    if (temp <= 4):
        return responses[0]
    elif (4 < temp < 16):
        return responses[1]
    else: 
        return responses[2]

def extractNum(value):
    pattern = re.compile('[-+]?\d*\.?\d+')
    temp = pattern.match(value)
    if (type(temp) == re.Match):
        return temp[1]
    else:
         #This should never happen, but does = issue w/ regex pattern
         return "NaN"

def inequalityLessThan(value):
    temp = extractNum(value)   
    return setResponse(temp)

def inequalityGreaterThan(value):
    temp = extractNum(value)
    return setResponse(temp)     

def numWithUnits(value):
    temp = extractNum(value)
    return setResponse(temp) 

def funcMap(value, num):
    if num == 0:
       return inequalityLessThan(value)
    elif num == 1:
       return inequalityGreaterThan(value)
    elif num == 2:
      return  inequalityLessThan(value)
    elif num == 3:
       return inequalityGreaterThan(value)
    elif num == 4:
       return numWithUnits(value)

responses = ["Susceptible", "Intermediate", "Resistant", "NaN"]

regexArray = [
    [re.compile('[<=]'), 0],
    [re.compile('[>=]'), 1],
    [re.compile('[<]'), 2],
    [re.compile('[>]'), 3],
    [re.compile('/(?=.*ug.*)'), 4]
]

def applyLogic(value, organism, method, antibiotic, dfRules):
    #if str contains no nums return immediately
    if value.isalpha():
        return responses[3]
    #if str contains only nums jump to setResponse
    if value.isnumeric():
        return setResponse(value)
        
    dfRuleSet = dfRules.loc[(dfRules['organism'] == organism) & (dfRules['antibiotic'] == antibiotic) & (dfRules['method'] == method)]
    if not dfRuleSet.empty:
        print(dfRuleSet)
    #regex[0] is regex pattern
    #regex[1] is mapper identifier num
    for regex in regexArray:
        n = regex[0].match(value)
        if (type(n) == re.Match):
            return funcMap(value, regex[1])

    return "Did not match any regex"

