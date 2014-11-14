from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, redirect
from hello.oauth import oauth_code

def index(request):
	template = loader.get_template('hello/step1.html')
	if request.method == 'GET':
		aad_code = request.GET.get('code','')
		context = {'url': '', 'status_code':'', 'history':'', 'aad_code':aad_code}
		if aad_code != '':
			oauth_obj = oauth_code()
			resp = oauth_obj.get_subscriptions(aad_code)
			context['subscriptions'] = resp.text
			context['requestheaders'] = resp.request.headers
		return render(request, 'hello/step1.html', context)
	elif request.method == 'POST':
		oauth_obj = oauth_code()
		oauth_obj.do_common()
		context = {'url': oauth_obj.url, 'status_code':oauth_obj.status_code, 'history':oauth_obj.history, 'aad_code':''}
		return redirect(oauth_obj.url)
	