alphabets = "abcdefghijklmnopqrstuvwxyz"

def get13Char(inputChar):
    charindex = alphabets.index(inputChar)
    #print charindex
    newindex = charindex + 13
    if newindex > 25:
        newindex = charindex - 13
    return alphabets[newindex]

