azure-python-authenticate
=========================

Open source authentication sample for Microsoft Azure via Python/Django
To run this sample to best effect, you'll need two subscriptions, each with a different associated directory.  Otherwise, how would it be a demo of a multi-tenant app?  I'll refer to the two tenants (directories) as TenantA and TenantB.

To set up your environment to run this sample:
1. Create a web app inside your Azure AD tenant.  (TenantA)
  * Capture the client id of that app.  
  * If you don't have a record of the client key, create a new one and record it. 
  * In the section at the bottom of the page "Windows Azure Service Management API", in the Delegated Permissions dropdown, check the box.
  * Add "http://localhost:8000/aadrest/step2/" to the list of acceptable Reply URL's.
  * Toggle to "yes" - Application is Multi-Tenant
  * Save the page.

2. Your dev box should have this directory structure after cloning the repo:

        azure-python-authenticate
        |_djangoSite
            |_djangoSite
            |_aadrest
                |_migrations
                |_Templates
                    |_aadrest
		  
3. Edit djangoSite\djangoSite\settings.py
  1. client_id
  2. client_key
  3. redirect_uri - can usually be left alone, but if you change the port, make sure you edit Reply URL in the app definition page (above).

To run the sample:

1.  Start up the python dev web server environment.  Docs on this are here:
	https://docs.djangoproject.com/en/dev/intro/tutorial01/ 
	
	Open a command prompt and navigate to: azure-python-authenticate\djangoSite.
	Enter the command: python manage.py runserver
	
2.  Open a web browser.  Navigate to: http://localhost:8000/aadrest

3.  When you click the button on the first page, it will redirect you to the AAD login page.  Enter credentials from your AAD tenant.  For example: user@tenantb.onmicrosoft.com.   (aka an organizational ID) (NOTE: TenantB user)

4.	(FYI) As part of the process, Azure AD will present a permission request - asking if it's ok that the app from TenantA be listed in the apps list of TenantB.  Click OK.

5.  After authenticating, the app will display certain progress information as you click through the buttons on the pages.

If you've been critically thinking as you go through this, you have noticed that everything is taking place in the context of a single AAD tenancy.  Since the purpose of the sample is to demonstrate a multi-tenant solution, maybe this strikes you as a little bit bogus.  It is.  

A planned next step is to test the technique with >=2 tenants.  Shortly thereafter, test the technique with a live ID rather than an organizational ID.