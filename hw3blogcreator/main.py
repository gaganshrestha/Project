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
import os
import jinja2
import datetime
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

#Mail handler class with all functions
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

#Creating instance
class Blog(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):
    
    def render_front(self,subject="",content="",error=""):
        self.render("front.html",subject=subject,content=content,error=error)

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            a = Blog(subject = subject, content = content)
            key = a.put()
            self.redirect("/list/%d" % key.id())
        else:
            error = "we need both subject and blog please !"
            self.render_front(subject,content,error)
    
    def get(self):
        self.render_front()

# Render a single post
class Permalink(Handler):
    def get(self, blog_id):
        blog = Blog.get_by_id(int(blog_id))
        self.render("list.html", blogs = [blog])

class ListHandler(Handler):
    def get(self):
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC limit 10")
        self.render("list.html",blogs=blogs)
        


app = webapp2.WSGIApplication([('/list/newpost',MainPage),
                               ('/list',ListHandler),
                               ('/list/(\d+)',Permalink)
                               ], debug=True)
