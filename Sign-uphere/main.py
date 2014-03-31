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
import validateForm

user=""

form="""
<form method="post">

        <font size=10 style="bold">Signup</font>
        <br><br>
        <table border=0>
                <tr>
                        <td align="right"><font size=5>Name</font></td>
                        <td><input type="text" name="username" value="%(name)s"></td>
                        <td><div style="color: red">%(nameerror)s</div></td>
                </tr>
                <tr>
                        <td align="right"><font size=5>Password</font></td>
                        <td><input type="password" name="password" value=""></td>
                        <td><div style="color: red">%(passwderror)s</div></td>
                </tr>
                <tr>
                        <td align="right"><font size=5>Confirm Password</font></td>
                        <td><input type="password" name="verify" value=""></td>
                        <td><div style="color: red">%(matcherror)s</div></td>
                </tr>
                <tr>
                         <td align="right"><font size=5>Email (Optional)</font></td>
                         <td><input type="text" name="email" value="%(email)s"></td>
                         <td><div style="color: red">%(emailerror)s</div></td>
                </tr>
        </table>
        <br>
        <br>
	<input type="submit">
	
</form>
"""

def escape_html(str):
        dic = {'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}
        for i, j in dic.iteritems():
            str = str.replace(i,j)
        return str

user=""

class MainHandler(webapp2.RequestHandler):
    
    def write_form(self,name='',nameerror='',passwderror='',matcherror='',
                   email='',emailerror=''):
        self.response.out.write(form %{"name": name,
                                       "nameerror": nameerror,
                                       "passwderror": passwderror,
                                       "matcherror": matcherror,
                                       "email": email,
                                       "emailerror": emailerror})

            
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.write_form()

    def post(self):
            usr_name = self.request.get('username')
            usr_passwd = self.request.get('password')
            usr_cpasswd = self.request.get('verify')
            usr_email = self.request.get('email')

            name, nameerror = validateForm.validateName(usr_name)
            passwd, passwderror = validateForm.validatePasswd(usr_passwd)
            passwd_match, matcherror = validateForm.comparePasswd(usr_passwd,usr_cpasswd)
            emailerror=''
            email=1
            
            if usr_email:
                    email,emailerror = validateForm.validateEmail(usr_email)

            if (name and passwd and passwd_match and email):
                                      
                    self.redirect("/welcome?username=%s" %usr_name)
                    
            else:
                    self.write_form(usr_name,nameerror,passwderror,matcherror,usr_email,emailerror)
                    
                    
                
class WelcomeHandler(MainHandler):
    def get(self):
        self.response.out.write("<font size=30><b>Welcome, " + self.request.get('username') + " !!!</b></font>")
   

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome',WelcomeHandler,)
    ], debug=True)

