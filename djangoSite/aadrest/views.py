from xml.dom.minidom import parseString
from django.shortcuts import render, redirect
import requests
from requests_oauthlib import OAuth2Session

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def index(request):

	# initialization
	client_id = '54da33ea-bd9b-4391-9863-33af3f005b53'
	template_name = 'aadrest/step1.html'
	redirect_uri = 'http://localhost:8000/aadrest/step2/'
	authorization_base_url = 'https://login.windows.net/common/oauth2/authorize'
	
	context = {'initialize':''}
	
	# GET as a result of initial invocation
	if request.method == 'GET':
		
		# initial invocation, just render
		return render(request, template_name, context)
		
	# OAUTH STEP 1 - POST as a result of clicking the LogIn submit button	
	elif request.method == 'POST':

		# create a 'requests' Oauth2Session
		azure_session = OAuth2Session(client_id, redirect_uri=redirect_uri)

		# do the outreach to https://login.windows.net/common/oauth2/authorize
		authorization_url, state = azure_session.authorization_url(authorization_base_url)
		resp = requests.get(authorization_url)		
		
		# go to the login page of AAD & authenticate
		return redirect(resp.url)

def step2(request):

	# initialization
	template_name = 'aadrest/step2.html'
	template_name_next_page = 'aadrest/step3.html'
	token_url = 'https://login.windows.net/common/oauth2/token'
	redirect_uri = 'http://localhost:8000/aadrest/step2/'
	client_id = '54da33ea-bd9b-4391-9863-33af3f005b53'
	client_key = 'gvky5/Jf2Ig4SCa472Gt0z82KWE6Bl9s+nH2BOYPlW8='
	resource_uri = 'https://management.core.windows.net/'
	
	context = {'initialize':''}
	azure_session = OAuth2Session(client_id, redirect_uri=redirect_uri)
	
	if request.method == 'GET':
	
		# get the code returned by AAD and save it in session
		aad_code = request.GET.get('code','')
		request.session['aad_code'] = aad_code

		# display the code
		context['aad_code'] = aad_code
		
		return render(request, template_name, context)
		
	elif request.method == 'POST':
	
		# get code back from session
		aad_code = request.session['aad_code']

		# OAUTH STEP 2 - go fetch the token
		token_dict = azure_session.fetch_token(token_url, code=aad_code, client_secret=client_key, resource=resource_uri)
		
		# pass the token to the next step on session
		request.session['token'] = token_dict

		# display the token
		context['token'] = token_dict
		
		return render(request, template_name_next_page, context)
		
def step3(request):

	# initialization
	template_name = 'aadrest/step3.html'
	template_name_next_page = 'aadrest/step4.html'
	client_id = '54da33ea-bd9b-4391-9863-33af3f005b53'
	redirect_uri = 'http://localhost:8000/aadrest/step2/'
	get_subscriptions_url = 'https://management.core.windows.net/subscriptions'
	ms_api_version_header = 'x-ms-version'
	ms_api_version_header_value = '2013-08-01'

	context = {'initialize':''}
	
	if request.method == 'GET':
		return render(request, template_name, context)
		
	elif request.method == 'POST':

		# create a requests session with the token we got previously
		token = request.session['token']
		azure_session = OAuth2Session(client_id, redirect_uri = redirect_uri, token=token)
		
		# OAUTH STEP 3 - go get the subscriptions
		resp = azure_session.get(get_subscriptions_url, headers = {ms_api_version_header: ms_api_version_header_value})
		
		# extract the juice
		dom = parseString(resp.content)
		subscriptions = dom.getElementsByTagName("Subscription")
		output = []
		for subscription in subscriptions:
			name = subscription.getElementsByTagName("SubscriptionName")[0]
			nameText = getText(name.childNodes)
			output.append(nameText)

			tenantid = subscription.getElementsByTagName("AADTenantID")[0]
			tenantText = getText(tenantid.childNodes)
			output.append(tenantText)

		# stick them in context & display
		context['subscriptions'] = output

		return render(request, template_name_next_page, context)

def step4(request):
	template_name = 'aadrest/step4.html'
	redirect_uri = 'http://localhost:8000/aadrest/step2/'
	authorization_base_url = 'https://login.windows.net/{x}/oauth2/authorize'

	context = {'initialize':''}

	if request.method == 'GET':
		return render(request, template_name, context)

	# OAUTH STEP 1 - POST as a result of clicking the LogIn submit button	
	elif request.method == 'POST':

		# create a 'requests' Oauth2Session
		azure_session = OAuth2Session(client_id, redirect_uri=redirect_uri)

		# do the outreach to https://login.windows.net/common/oauth2/authorize
		authorization_url, state = azure_session.authorization_url(authorization_base_url)
		resp = requests.get(authorization_url)		
		
		# go to the login page of AAD & authenticate
		return redirect(resp.url)