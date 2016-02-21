

from flask import Flask, redirect
import requests
class OmnAuth(object):

	def __init__(self):
		self.myClientId = 'ZsDq2bcC9e'
		self.mySecret = 'dEHBPDNqyWt8wtcA7VcdeK'
		self.myUrl = 'quizskim.com'
		self.authorizeUrl = "https://quizlet.com/authorize?client_id=" + self.myClientId + "&response_type=code&scope=read+write_set"
		self.tokenUrl = 'https://api.quizlet.com/oauth/token'

	def redirect_user(self):
		response_type = 'code'
		scope = 'read+write_set+write_group'
		state = '123'
		redir = "http://localhost:5033/auth2"
		redirect_url = "https://quizlet.com/authorize?response_type=" + response_type + "&client_id=" + self.myClientId + "&scope=" + scope + "&state=" + state + "&redirect_uri=" + redir
		return redirect_url

			
if __name__ == '__main__':
	__init__()
