import re

def validateName(input):
    result=''
    if input:
        criteria = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        result = criteria.match(input)
      
    if not result or not input:
            return 0, "That's not a valid username."
    else:
            return 1,''
    
           
def validatePasswd(input):
    result=''
    if input:
        criteria = re.compile(r"^.{3,20}$")
        result = criteria.match(input)
      
    if not result or not input:
            return 0, "That's not a valid password."
    else:
            return 1,''

def comparePasswd(p1, p2):
    if p1 == p2:
        return 1, ''
    else:
        return 0, "Your passwords didn't match."


def validateEmail(input):
    result=''
    if input:
        criteria = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
        result = criteria.match(input)
      
    if not result:
            return 0,"That's not a valid email address."
    else:
            return 1,''
