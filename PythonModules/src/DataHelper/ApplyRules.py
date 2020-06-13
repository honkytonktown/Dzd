import re


def match_rules(x, dfRuleSet):
    """ match_rules takes in a string value (x) and a ruleset
    iterates through the rules and looks for a regex match on the string value
    when a match is found, string value is replaced with whatever value
    has been set for that regex. For the example provided in the assessment,
    I used the pattern /.*\\b(Trimeth.*|Sulfa.*)\\b.*. Any match is replaced with
    'Trimethoprim/Sulfamethoxazole', as seen in the MatchingRules table.
    row[0] == column type
    row[1] == replacement phrase
    row[2] == regex pattern """

    if not dfRuleSet.empty:
        for i, row in dfRuleSet.iterrows():
            result = re.search((r'{}').format(row[2]), x)
            if result is not None:
                x = row[1]   
    return x



