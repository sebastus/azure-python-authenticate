import requests
from requests_oauthlib import OAuth2, OAuth2Session

class oauth_code:
	def __init__(self):
		self.url = ''
		self.status_code = ''
		self.history = ''
		self.authorization_response = ''
		
		self.client_id = '86cc9609-4c6e-41e8-b00b-8016aa9a1ef5'
		self.client_key = 'AkK47kyLNVCyn7n4llQpFqlY6QRJ67C/3RUsBCnWqxE='
		self.authorization_base_url = 'https://login.windows.net/common/oauth2/authorize'
		self.token_url = 'https://login.windows.net/common/oauth2/token'
		self.get_subscriptions_url = 'https://management.core.windows.net/subscriptions'
		self.x_ms_version = '2013-08-01'
		self.redirect_uri = 'http://localhost:8000/hello'
		
		self.azure_session = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri, scope=['https://management.core.windows.net/subscriptions'])
		
	def do_common(self):
		# get the authorization url from the base url + creds
		authorization_url, state = self.azure_session.authorization_url(self.authorization_base_url)
		resp = requests.get(authorization_url)

		self.authorization_response = resp.url
		self.status_code = resp.status_code
		self.history = resp.history
	
	def get_subscriptions(self, token):
		header_dict = {'Authorization': 'Bearer ' + token}
		return requests.request('GET', self.get_subscriptions_url, headers = header_dict)
	
	def fetch_token(self, aad_code, auth_resp):
		print ('call fetch_token')
		token_dict = self.azure_session.fetch_token(self.token_url, client_secret=self.client_key, code=aad_code, authorization_response = auth_resp)
		print ('finished fetch_token')
		print (token_dict)
		return token_dict