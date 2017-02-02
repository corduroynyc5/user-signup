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
import cgi
import re

form = """
<!DOCTYPE html>
<html>
<head>
	<title>Sign Up</title>
	<style type="text/css">
		.error {
			color: red;
		}
	</style>
</head>
<body>
	<h1>
		Sign Up
	</h1>
	
			<form action="/" method="post">
				<table>
					<tbody><tr>
						<td><label for="username">Username</label></td>
						<td>
							<input name="username" value="%(username)s" required="" type="text">
							<span class="error" name="error_username">%(error_username)s</span>
						</td>
					</tr>
					<tr>
						<td><label for="password">Password</label></td>
						<td>
							<input name="password" required="" type="password">
							<span class="error" name="error_password">%(error_password)s</span>
						</td>
					</tr>
					<tr>
						<td><label for="verify">Verify Password</label></td>
						<td>
							<input name="verify" required="" type="password">
							<span class="error" name="error_verify">%(error_verify)s</span>
						</td>
					</tr>
					<tr>
						<td><label for="email">Email (optional)</label></td>
						<td>
							<input name="email" value="%(email)s" type="text">
							<span class="error" name="error_email">%(error_email)s</span>
						</td>
					</tr>
				</tbody></table>
				<input type="submit">
			</form>
		
		
</body>
</html>
"""
#regular expressions for validation
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
	return not email or EMAIL_RE.match(email)

class Index(webapp2.RequestHandler):
	"""
		Handles requests coming in to '/'
	"""
	def write_form(self, error_username="", error_password="", error_verify="", error_email="", username="", email=""):
		self.response.out.write(form % ({"error_username": error_username, "error_password": error_password, "error_verify": error_verify, "error_email": error_email, "username": username, "email": email}))
		
	def get(self):
		self.write_form()
		
	def post(self):
		page_error = False		
		username = self.request.get("username")		
		password = self.request.get("password")		
		verify = self.request.get("verify")		
		email = self.request.get("email")
		e_username = ""
		e_password = ""
		e_verify = ""
		e_email = ""
									
		if not valid_username(username):
			e_username = "That's not a valid username."
			page_error = True			

		if not valid_password(password):
			e_password = "That wasn't a valid password."
			page_error = True			
		elif password != verify:
			e_verify = "Your passwords didn't match."
			page_error = True
			
		if not valid_email(email):
			e_email = "That's not a valid email."
			page_error = True			
				
		if page_error:
			self.write_form(e_username, e_password, e_verify, e_email, username, email)			
		else:			
			self.redirect('/welcome?username=' + username)
			
class Welcome(webapp2.RequestHandler):
	"""
		Handles requests coming in to '/welcome'
	"""

	def get(self):		
		username = self.request.get("username")				
		content = "Welcome, " + username + "!"
		self.response.write(content)

app = webapp2.WSGIApplication([
	('/', Index),
	('/welcome', Welcome)
], debug=True)
