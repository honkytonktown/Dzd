#Dzd specific rules
    #determine what signs mean
    #extract the numerical values out
    
    #When organism == Escherichia coli
    #If Value <=4: Susceptible
    #If 4 < Value < 16: Intermediate
    #If Value >=16: Resistant

import re
import pandas as pd


def set_response(value, dfRuleSet):
    """ set_response, if there is a matching rule set, applies new inequality comparisons
        to value. It compares existing value to appropriate value determined in dzd rules """ 
    if dfRuleSet.empty: 
        return responses[3]

    else:
        if (value <= float(dfRuleSet['susceptible'].values[0])):
            return responses[0]
        elif(value >= float(dfRuleSet['resistant'].values[0])):
            return responses[2]
        elif(value > float(dfRuleSet['intermediatelow'].values[0]) and value < float(dfRuleSet['intermediatehigh'].values[0])):
            return responses[1]
        

def extract_num(value):
    """ extract_num runs regex pattern against value to extract any number """
    try:
        numValue = re.search(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', value).group(1)
        if numValue is not None:
            return float(numValue)
    except: 
        msg = "Failed to find numerical value within: {}".format(value)
        return (msg)

def less_than(value, dfRuleSet):
    """ <4 returns 4 from extractNum, so need to reduce value slightly
        for inequality to remain true - (ie. 4 < 4 is false, but 3.99 < 4 is not) """
    temp = extract_num(value)
    temp -= 0.01  
    return set_response(temp, dfRuleSet)


def greater_than(value, dfRuleSet):
    """ >4 returns 4 from extractNum, so need to bump value slightly
        for inequality to remain true """ 
    temp = extract_num(value)
    temp += 0.01  
    return set_response(temp, dfRuleSet)     

def simple_handler(value, dfRuleSet):
    """ simple_handler handles regex patterns that don't require modification """
    temp = extract_num(value)
    return set_response(temp, dfRuleSet)

responses = ["Susceptible", "Intermediate", "Resistant", "No matching rule", "Value has no nums"] 


def mapper(id, value, dfRuleSet):
    """ mapper assigns a function to the regex pattern
        original matching function was part of list w/ the regex pattern
        but functions were being executed when the list was declared,
        slowing down the process """ 
    if id == 0:
        return simple_handler(value, dfRuleSet)
    elif id == 1:
        return less_than(value, dfRuleSet)
    elif id == 2:
        return greater_than(value, dfRuleSet)


def apply_logic(value, organism, method, antibiotic, dfRules):
    """ apply_logic deduces 'value' column through series of steps.
        Values containing only strings are returned immediately.
        Values that are just numbers jump to simple_handler, matching patterns
        are sorted by type """
    dfRuleSet = dfRules.loc[(dfRules['organism'] == organism) & (dfRules['antibiotic'] == antibiotic) & (dfRules['method'] == method)]
    if value.isalpha():
        return responses[4]

    elif value.isnumeric():
        return simple_handler(value, dfRuleSet)

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

