# class OAuthSignIn(object):
# 	providers = None
	
# 	def __init__(self, provider_name):
# 		self.provider_name = provider_name
# 		credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
# 		self.consumer_id = credentials['id']
# 		self.consumer_secret = credentials['secret']

# 	def authorize(self):
# 		pass
	
# 	def callback(self):
# 		pass

# 	def get_callback_url(self):
# 		return url_for('oauth_callback', provider=self.provider_name,
# 					_external = True)

# 	@classmethod
# 	def get_provider(self, provider_name):
# 		if self.providers is None:
# 			self.providers = {}
# 			for provider_class in self.__subclasses__():
# 				provider = provider_class()
# 				self.providers[provider.provider_name] = provider
# 		return self.providers[provider_name]

# class QuizletSignIn(OAuthSignIn):
# 	def __init__(self):
# 		super(QuizletSignIn, self).__init__('quizlet')
# 		self.service = OAuth2Service(
# 			authorizeUrl = "https://quizlet.com/authorize?client_id={$myClientId}&response_type=code&scope=read%20write_set",
# 			tokenUrl= 'https://api.quizlet.com/oauth/token',
# 			myUrl = 'quizskim.com',
# 			mySecret = 'dEHBPDNqyWt8wtcA7VcdeK',
# 			myClientId = 'ZsDq2bcC9e'
# 		)
	
# 	def authorize(self):
# 		return redirect(self.service.get_authorize_url(
# 			scope='read%20write_set%20write_group',
# 			client_id='ZsDq2bcC9e',
# 			response_type='code',
# 			state='cczaq22',
# 			redirect_uri=self.get_callback_url())

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
		redir = "http://localhost:5032/auth2"
		redirect_url = "https://quizlet.com/authorize?response_type=" + response_type + "&client_id=" + self.myClientId + "&scope=" + scope + "&state=" + state + "&redirect_uri=" + redir
		return redirect_url

			
if __name__ == '__main__':
	__init__()
