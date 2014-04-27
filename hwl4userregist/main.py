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
import jinja2
import json
import os
import random
import validateForm
import hashlib
import hmac
from google.appengine.ext import db
from string import letters

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

secret = 'GOD'

def hash_str(s):
	return hashlib.md5(s).hexdigest()

def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))
	
def make_secure_val(val):
	return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def make_pw_hash(name,passwd,salt=None):
        if not salt:
                salt = make_salt()
        h = hashlib.sha256(name + passwd + salt).hexdigest()
        return '%s,%s' % (salt, h)
        
def valid_pw(name,pw,pw_hash):
        salt = pw_hash.split(',')[0]
        return pw_hash == make_pw_hash(name,pw,salt)

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




#Mail handler class with all functions
class Handler(webapp2.RequestHandler):
        def write(self, *a, **kw):
                self.response.out.write(*a, **kw)
        def render_str(self, template, **params):
                t = jinja_env.get_template(template)
                return t.render(params)
        def render(self, template, **kw):
                self.write(self.render_str(template, **kw))
        def logout(self):
                self.response.headers.add_header('Set-Cookie','user=;Path=/')

        def render_json(self,d):
                json.txt = json.dumps(d)
                self.response.headers['content-type']='application/json; charset=UTF-8'
                self.response.out.write(json.txt)


#Instance for blog                
class Blog(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    

#Creating instance
class Registration(db.Model):
        username = db.StringProperty(required = True)
        pw_hash = db.StringProperty(required = True)
        email = db.StringProperty

        @classmethod
        def by_name(cls, name):
                u = cls.all().filter('username =', name).get()
                return u

        @classmethod
        def login(cls,name,passwd):
                u = cls.by_name(name)
                if u and valid_pw(name, passwd, u.pw_hash):
                        return u

        @classmethod
        def register(cls,name,passwd,email=None):
                pw_hash = make_pw_hash(name,passwd)
                return Registration(username=name,pw_hash=pw_hash,email=email)           
                
user=""

class MainHandler(Handler):     

    def write_form(self,name='',nameerror='',passwderror='',matcherror='',email='',emailerror=''):
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
                    u = Registration.by_name(usr_name)
                    if u:
                            nameerror = "The user already exists!"
                            self.write_form(usr_name,nameerror,passwderror,matcherror,usr_email,emailerror)
                    else:
                            
                            a = Registration.register(usr_name,usr_passwd,usr_email)
                            a.put()
                            cookie_val=make_secure_val(str(usr_name))
                            self.response.headers.add_header('Set-Cookie', 'user=%s; Path=/'%cookie_val)    
                            self.redirect("/welcome")
                            
                                               
            else:
                    self.write_form(usr_name,nameerror,passwderror,matcherror,usr_email,emailerror)
            
class NewPost(Handler):
        def render_front(self,subject="",content="",error=""):
                self.render("front.html",subject=subject,content=content,error=error)

        def post(self):
                subject = self.request.get("subject")
                content = self.request.get("content")

                if subject and content:
                    a = Blog(subject = subject, content = content)
                    key = a.put()
                    self.redirect("/blog/%d" % key.id())
                else:
                    error = "we need both subject and blog please !"
                    self.render_front(subject,content,error)
    
        def get(self):
                self.render_front()


class Permalink(Handler):
        def get(self, blog_id):
                               
                if self.request.url.endswith('.json'):
                        blog_id = blog_id.split(".")[0]                        
                        self.format = 'json'
                else:
                        self.format = 'html'

                blog = Blog.get_by_id(int(blog_id))

                if self.format == 'html':
                        self.render("list.html", blogs = [blog])
                else:
                        time_fmt = '%b %d, %Y'
                        dObj = {'subject':blog.subject,'content':blog.content,'created':blog.created.strftime(time_fmt)}
                        self.render_json(dObj)
                        

        
                    
class Login(Handler):

        def render_front(self,name="",error=""):
                self.render("login-form.html",username=name,error=error)
        
        def get(self):
                self.render_front()

        def post(self):
                username = self.request.get("username")
                password = self.request.get("password")

                if username and password:
                        u = Registration.login(username,password)
                        if u:
                                cookie_val=make_secure_val(str(username))
                                self.response.headers.add_header('Set-Cookie', 'user=%s; Path=/'%cookie_val)
                                self.redirect('/welcome')
                        else:
                               error="Invalid login!"
                               self.render_front(username,error)
                else:
                        error="Please enter both username and password !"
                        self.render_front(username,error)
                        
class Logout(Handler):
               
        def get(self):
                self.logout()
                self.redirect('/signup')
                              
class ListHandler(Handler):
    def get(self):
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC limit 10")
        if self.request.url.endswith('.json'):
                self.format = 'json'
        else:
                self.format = 'html'
                
        if self.format == 'html':
                self.render("list.html",blogs=blogs)
        else:
                time_fmt = '%b %d, %Y'
                dObj = []
                for blog in blogs:
                       element = {'subject':blog.subject,'content':blog.content,'created':blog.created.strftime(time_fmt)}
                       dObj.append(element)
                       
                self.render_json(dObj)
                
class WelcomeHandler(MainHandler):
    def get(self):
        user = self.request.cookies.get('user').split('|')[0]
        self.response.out.write("<font size=30><b>Welcome, " + user + " !!!</b></font>")
   

app = webapp2.WSGIApplication([
    ('/signup', MainHandler),
    ('/welcome',WelcomeHandler),
    ('/newpost',NewPost),
    ('/blog/?(?:.json)?',ListHandler),
    ('/blog/([0-9]+)(?:.json)?',Permalink),
    ('/login',Login),
    ('/logout',Logout)
    ], debug=True)

