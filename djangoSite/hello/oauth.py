import requests
from requests_oauthlib import OAuth2, OAuth2Session

class oauth_code:
	def __init__(self):
		self.url = ''
		self.status_code = ''
		self.history = ''
	
		self.client_id = '86cc9609-4c6e-41e8-b00b-8016aa9a1ef5'
		self.client_key = 'AkK47kyLNVCyn7n4llQpFqlY6QRJ67C/3RUsBCnWqxE='
		self.authorization_base_url = 'https://login.windows.net/common/oauth2/authorize'
		self.token_url = 'https://login.windows.net/common/oauth2/token'
		self.get_subscriptions_url = 'https://management.core.windows.net/subscriptions'
		self.x_ms_version = '2013-08-01'
		
	def do_common(self):
		azure = OAuth2Session(self.client_id, redirect_uri='http://localhost:8000/hello')
		
		authorization_url, state = azure.authorization_url(self.authorization_base_url)
		resp = requests.get(authorization_url)		
		self.url = resp.url
		self.status_code = resp.status_code
		self.history = resp.history
	
	def get_subscriptions(self, auth_code):
		header_dict = {'Authorization': 'Bearer ' + auth_code}
		return requests.request('GET', self.get_subscriptions_url, headers = header_dict)
