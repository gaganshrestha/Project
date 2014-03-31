#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import get13Char

form="""
<form method="post">
        <font size=6><b>Enter some text to my version of ROT13: </b></font>
        <br><br>
        <textarea rows="10" cols="30" name="text">%(input)s</textarea>
        <br><br>
	<input type="submit">	
</form>
"""

'''def escape_html(str):
        dic = {'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}
        for i, j in dic.iteritems():
            str = str.replace(i,j)
        return str
'''


class MainHandler(webapp2.RequestHandler):
        
    def get13Char(self,inputChar):
        charindex = alphabets.index(inputChar)
        newindex = charindex + 13
        if newindex > 25:
             newindex = charindex - 13
             return alphabets[newindex]
     
   
    def write_form(self,rot13=""):
        self.response.out.write(form %{"input": rot13})
           
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.write_form()

    def post(self):
            
            userInput = self.request.get('text')
            outPut = ''
            for letter in userInput:
                    if letter.isalpha():
                            case = letter.isupper()
                            if case:
                                    letter = letter.lower()
                                    newLetter = get13Char.get13Char(letter)
                                    newLetter = newLetter.upper()
                            else:
                                    newLetter = get13Char.get13Char(letter)
                            outPut = outPut + newLetter
                    else:
                            outPut = outPut + letter
      
            self.write_form(outPut)
        
'''class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("thanks! valid day !")'''


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ], debug=True)

