from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, redirect
from hello.oauth import oauth_code

def index(request):
	template = loader.get_template('hello/step1.html')
	if request.method == 'GET':
	
		# see if we're coming back from the redirect to authenticate
		aad_code = request.GET.get('code','')
		if aad_code != '':
			context = {'aad_code':aad_code}
			oauth_obj = oauth_code()
			resp = oauth_obj.get_subscriptions(aad_code)
			context['subscriptions'] = resp.text
			context['requestheaders'] = resp.request.headers
			
		# if not coming back from redirect, just render
		return render(request, 'hello/step1.html', context)
		
	elif request.method == 'POST':
	
		# POST as a result of clicking the LogIn submit button
		oauth_obj = oauth_code()
		
		# do the outreach to https://login.windows.net/common/oauth2/authorize
		oauth_obj.do_common()
		
		# redirect to the URL passed back by that service call - this is the authentication page @ AAD
		# the redirect_uri brings us right back here (above) but this time with the 'code' query parameter
		return redirect(oauth_obj.url)
	