import string


def filter_to_list(filterFunc, l):
    return list(filter(filterFunc, l))


def keys_from_template_string(tempStr):
    stringTuples = list(string.Formatter.parse("", tempStr))
    # Special case: string with no template arguments
    firstTuple = stringTuples[0]
    if(firstTuple[1] == None and firstTuple[2] == None and firstTuple[3] == None):
        return []
    else:
        keyNames = list(map(lambda el: el[1], stringTuples))
        return list(filter(lambda x: x != None, keyNames))


def have_keys_for_template_string(d, tempStr):
    tempStrKeys = keys_from_template_string(tempStr)
    if(len(tempStrKeys) == 0):
        return True
    else:
        return set(tempStrKeys).issubset(set(d))