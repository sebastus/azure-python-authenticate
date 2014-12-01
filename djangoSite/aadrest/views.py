from xml.dom.minidom import parseString
from django.shortcuts import render, redirect
import requests
from requests_oauthlib import OAuth2Session
from django.conf import settings
import logging
logging.basicConfig(level=logging.INFO)

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def index(request):
	context = {'initialize':''}
	return render(request, 'aadrest/index.html', context)
	
def step1(request):
	
	# initialization
	constants = settings.CONSTANTS
	CLIENT_ID = constants['CLIENT_ID']
	STEP_1_TEMPLATE_NAME = constants['STEP_1_TEMPLATE_NAME']
	REDIRECT_URI = constants['REDIRECT_URI']
	AUTHORIZATION_BASE_URL = constants['AUTHORIZATION_BASE_URL']
	
	context = {'initialize':''}
	
	# GET as a result of initial invocation
	if request.method == 'GET':
		
		# initial invocation, just render
		return render(request, STEP_1_TEMPLATE_NAME, context)
		
	# OAUTH STEP 1 - POST as a result of clicking the LogIn submit button	
	elif request.method == 'POST':

		# create a 'requests' Oauth2Session
		azure_session = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)

		# do the outreach to https://login.windows.net/common/oauth2/authorize
		authorization_url, state = azure_session.authorization_url(AUTHORIZATION_BASE_URL % 'common')
		resp = requests.get(authorization_url)		
		
		# go to the login page of AAD & authenticate
		return redirect(resp.url)

def step2(request):

	# initialization
	constants = settings.CONSTANTS
	STEP_2_TEMPLATE_NAME = constants['STEP_2_TEMPLATE_NAME']
	STEP_3_TEMPLATE_NAME = constants['STEP_3_TEMPLATE_NAME']
	BASE_TOKEN_URL = constants['BASE_TOKEN_URL']
	REDIRECT_URI = constants['REDIRECT_URI']
	CLIENT_ID = constants['CLIENT_ID']
	CLIENT_KEY = constants['CLIENT_KEY']
	RESOURCE_URI = constants['RESOURCE_URI']
	
	context = {'initialize':''}
	azure_session = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
	
	if request.method == 'GET':
	
		# get the code returned by AAD and save it in session
		aad_code = request.GET.get('code','')
		request.session['aad_code'] = aad_code

		# display the code
		context['aad_code'] = aad_code
		
		return render(request, STEP_2_TEMPLATE_NAME, context)
		
	elif request.method == 'POST':
	
		# get code back from session
		aad_code = request.session['aad_code']

		# OAUTH STEP 2 - go fetch the token
		token_dict = azure_session.fetch_token(BASE_TOKEN_URL % 'common', code=aad_code, client_secret=CLIENT_KEY, resource=RESOURCE_URI)
		
		# pass the token to the next step on session
		request.session['token'] = token_dict

		# display the token
		context['token'] = token_dict
		
		return render(request, STEP_3_TEMPLATE_NAME, context)
		
def step3(request):

	# initialization
	constants = settings.CONSTANTS
	STEP_3_TEMPLATE_NAME = constants['STEP_3_TEMPLATE_NAME']
	STEP_4_TEMPLATE_NAME = constants['STEP_4_TEMPLATE_NAME']
	CLIENT_ID = constants['CLIENT_ID']
	REDIRECT_URI = constants['REDIRECT_URI']
	GET_SUBSCRIPTIONS_URL = constants['GET_SUBSCRIPTIONS_URL']
	MS_API_VERSION_HEADER = constants['MS_API_VERSION_HEADER']
	MS_API_VERSION_HEADER_VALUE = constants['MS_API_VERSION_HEADER_VALUE']

	context = {'initialize':''}
	
	if request.method == 'GET':
		return render(request, STEP_3_TEMPLATE_NAME, context)
		
	elif request.method == 'POST':

		# create a requests session with the token we got previously
		token = request.session['token']
		azure_session = OAuth2Session(CLIENT_ID, redirect_uri = REDIRECT_URI, token=token)
		
		# OAUTH STEP 3 - go get the subscriptions
		resp = azure_session.get(GET_SUBSCRIPTIONS_URL, headers = {MS_API_VERSION_HEADER: MS_API_VERSION_HEADER_VALUE})
		
		# extract the juice
		dom = parseString(resp.content)
		subscriptions = dom.getElementsByTagName("Subscription")
		output = []
		tenantText = 'No subscriptions found in list.'
		for subscription in subscriptions:
			name = subscription.getElementsByTagName("SubscriptionName")[0]
			nameText = getText(name.childNodes)
			output.append(nameText)

			tenantid = subscription.getElementsByTagName("AADTenantID")[0]
			tenantText = getText(tenantid.childNodes)
			output.append(tenantText)

		# stick them in context & display
		context['subscriptions'] = output
		
		# store the tenant id in session
		request.session['tenantid'] = tenantText

		return render(request, STEP_4_TEMPLATE_NAME, context)

def step4(request):

	# initialization
	constants = settings.CONSTANTS
	STEP_4_TEMPLATE_NAME = constants['STEP_4_TEMPLATE_NAME']
	STEP_5_TEMPLATE_NAME = constants['STEP_5_TEMPLATE_NAME']
	REDIRECT_URI = constants['REDIRECT_URI']
	BASE_TOKEN_URL = constants['BASE_TOKEN_URL']
	CLIENT_ID = constants['CLIENT_ID']
	CLIENT_KEY = constants['CLIENT_KEY']
	RESOURCE_URI = constants['RESOURCE_URI']

	context = {'initialize':''}

	if request.method == 'GET':
		return render(request, STEP_4_TEMPLATE_NAME, context)

	# OAUTH STEP 1 - POST as a result of clicking the LogIn submit button	
	elif request.method == 'POST':

		# get the tenant id and AAD code
		tenantid = request.session['tenantid']
		aad_code = request.session['aad_code']
		
		# create a 'requests' Oauth2Session
		azure_session = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)

		# OAUTH STEP 4 - go fetch the token for the tenant as opposed to Common
		token_dict = azure_session.fetch_token(BASE_TOKEN_URL % tenantid, code=aad_code, client_secret=CLIENT_KEY, resource=RESOURCE_URI)
		
		# put the token into context for display
		context['token'] = token_dict
		
		# present results
		return render(request, STEP_5_TEMPLATE_NAME, context) 
		
def step1_live(request):
	
	# initialization
	constants = settings.CONSTANTS
	CLIENT_ID = constants['CLIENT_ID']
	STEP_1_TEMPLATE_NAME = constants['STEP_1_TEMPLATE_NAME_LIVE']
	REDIRECT_URI = constants['REDIRECT_URI_LIVE']
	AUTHORIZATION_BASE_URL = constants['AUTHORIZATION_BASE_URL']
	
	context = {'initialize':''}
	
	# GET as a result of initial invocation
	if request.method == 'GET':
		
		# initial invocation, just render
		return render(request, STEP_1_TEMPLATE_NAME, context)
		
	# OAUTH STEP 1 - POST as a result of clicking the LogIn submit button	
	elif request.method == 'POST':

		# get the tenant name
		tenant_name = request.POST['tenantname']
		logging.info('tenant name = ' + tenant_name)
		resource_name = tenant_name + '.onmicrosoft.com'
		request.session['resource_name'] = resource_name
		
		# create a 'requests' Oauth2Session
		azure_session = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)

		# do the outreach to https://login.windows.net/common/oauth2/authorize
		authorization_url, state = azure_session.authorization_url(AUTHORIZATION_BASE_URL % resource_name)
		resp = requests.get(authorization_url)		
		
		# go to the login page of AAD & authenticate
		return redirect(resp.url)

def step2_live(request):

	# initialization
	constants = settings.CONSTANTS
	STEP_2_TEMPLATE_NAME = constants['STEP_2_TEMPLATE_NAME_LIVE']
	STEP_3_TEMPLATE_NAME = constants['STEP_3_TEMPLATE_NAME_LIVE']
	BASE_TOKEN_URL = constants['BASE_TOKEN_URL']
	REDIRECT_URI = constants['REDIRECT_URI_LIVE']
	CLIENT_ID = constants['CLIENT_ID']
	CLIENT_KEY = constants['CLIENT_KEY']
	RESOURCE_URI = constants['RESOURCE_URI']
	
	context = {'initialize':''}
	azure_session = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
	
	if request.method == 'GET':
	
		# get the code returned by AAD and save it in session
		aad_code = request.GET.get('code','')
		request.session['aad_code'] = aad_code

		# display the code
		context['aad_code'] = aad_code
		
		return render(request, STEP_2_TEMPLATE_NAME, context)
		
	elif request.method == 'POST':
	
		# get code back from session
		aad_code = request.session['aad_code']
		resource_name = request.session['resource_name']
		
		# OAUTH STEP 2 - go fetch the token
		token_dict = azure_session.fetch_token(BASE_TOKEN_URL % resource_name, code=aad_code, client_secret=CLIENT_KEY, resource=RESOURCE_URI)
		
		# pass the token to the next step on session
		request.session['token'] = token_dict

		# display the token
		context['token'] = token_dict
		
		return render(request, STEP_3_TEMPLATE_NAME, context)
				
def step3_live(request):

	# initialization
	constants = settings.CONSTANTS
	STEP_3_TEMPLATE_NAME = constants['STEP_3_TEMPLATE_NAME_LIVE']
	STEP_4_TEMPLATE_NAME = constants['STEP_4_TEMPLATE_NAME_LIVE']
	CLIENT_ID = constants['CLIENT_ID']
	REDIRECT_URI = constants['REDIRECT_URI_LIVE']
	GET_SUBSCRIPTIONS_URL = constants['GET_SUBSCRIPTIONS_URL']
	MS_API_VERSION_HEADER = constants['MS_API_VERSION_HEADER']
	MS_API_VERSION_HEADER_VALUE = constants['MS_API_VERSION_HEADER_VALUE']

	context = {'initialize':''}
	
	if request.method == 'GET':
		return render(request, STEP_3_TEMPLATE_NAME, context)
		
	elif request.method == 'POST':

		# create a requests session with the token we got previously
		token = request.session['token']
		azure_session = OAuth2Session(CLIENT_ID, redirect_uri = REDIRECT_URI, token=token)
		
		# OAUTH STEP 3 - go get the subscriptions
		resp = azure_session.get(GET_SUBSCRIPTIONS_URL, headers = {MS_API_VERSION_HEADER: MS_API_VERSION_HEADER_VALUE})
		
		# extract the juice
		dom = parseString(resp.content)
		subscriptions = dom.getElementsByTagName("Subscription")
		output = []
		tenantText = 'No subscriptions found in list.'
		for subscription in subscriptions:
			name = subscription.getElementsByTagName("SubscriptionName")[0]
			nameText = getText(name.childNodes)
			output.append(nameText)

			tenantid = subscription.getElementsByTagName("AADTenantID")[0]
			tenantText = getText(tenantid.childNodes)
			output.append(tenantText)

		# stick them in context & display
		context['subscriptions'] = output
		
		# store the tenant id in session
		request.session['tenantid'] = tenantText

		return render(request, STEP_4_TEMPLATE_NAME, context)

def step4_live(request):

	# initialization
	constants = settings.CONSTANTS
	STEP_4_TEMPLATE_NAME = constants['STEP_4_TEMPLATE_NAME_LIVE']
	STEP_5_TEMPLATE_NAME = constants['STEP_5_TEMPLATE_NAME_LIVE']
	REDIRECT_URI = constants['REDIRECT_URI_LIVE']
	BASE_TOKEN_URL = constants['BASE_TOKEN_URL']
	CLIENT_ID = constants['CLIENT_ID']
	CLIENT_KEY = constants['CLIENT_KEY']
	RESOURCE_URI = constants['RESOURCE_URI']

	context = {'initialize':''}

	if request.method == 'GET':
		return render(request, STEP_4_TEMPLATE_NAME, context)

	# OAUTH STEP 1 - POST as a result of clicking the LogIn submit button	
	elif request.method == 'POST':

		# get the tenant id and AAD code
		tenantid = request.session['tenantid']
		aad_code = request.session['aad_code']
		
		# create a 'requests' Oauth2Session
		azure_session = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)

		# OAUTH STEP 4 - go fetch the token for the tenant as opposed to Common
		token_dict = azure_session.fetch_token(BASE_TOKEN_URL % tenantid, code=aad_code, client_secret=CLIENT_KEY, resource=RESOURCE_URI)
		
		# put the token into context for display
		context['token'] = token_dict
		
		# present results
		return render(request, STEP_5_TEMPLATE_NAME, context) 
		