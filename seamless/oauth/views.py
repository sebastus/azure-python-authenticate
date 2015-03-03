from xml.dom.minidom import parseString
from django.shortcuts import render
from requests_oauthlib import OAuth2Session
from django.conf import settings
import requests
from django.shortcuts import render, redirect

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

# Create your views here.
def index(request):
	context = {'initialize':''}
	return render(request, 'oauth/index.html', context)
	
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
	BASE_TOKEN_URL = constants['BASE_TOKEN_URL']
	REDIRECT_URI = constants['REDIRECT_URI']
	CLIENT_ID = constants['CLIENT_ID']
	CLIENT_KEY = constants['CLIENT_KEY']
	RESOURCE_URI = constants['RESOURCE_URI']
	GET_SUBSCRIPTIONS_URL = constants['GET_SUBSCRIPTIONS_URL']
	MS_API_VERSION_HEADER = constants['MS_API_VERSION_HEADER']
	MS_API_VERSION_HEADER_VALUE = constants['MS_API_VERSION_HEADER_VALUE']
	
	context = {'initialize':''}
	azure_session = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
	
	if request.method == 'GET':
	
		# get the code returned by AAD
		aad_code = request.GET.get('code','')

		# OAUTH STEP 2 - go fetch the token
		token_dict = azure_session.fetch_token(BASE_TOKEN_URL % 'common', code=aad_code, client_secret=CLIENT_KEY, resource=RESOURCE_URI)
		
		# OAUTH STEP 3 - go get the subscriptions (or whatever service management API you want to call - this is just a sample)
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
		
		return render(request, STEP_2_TEMPLATE_NAME, context)


