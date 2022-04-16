from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import oauthlib
#from sqlalchemy import true
from server.forms import LoginForm, AccountRegisterForm
from server.models import Account, Action
from server import views
from server import logger
from django.contrib.auth import logout as django_logout
from authlib.integrations.django_client import OAuth
from django.shortcuts import redirect, render, redirect
import json

oauth = OAuth()
oauth.register(
    "auth0",
    client_id='8byXEQ7JTK9DFLXZliFOvVrGNfBCtu2U',
    client_secret='R5qeVOP_5EvXMDUmQZ65wcZg88JqM0ft6clVSmRXgY2M6zjidxdhkj_l_60d2TxL',
    client_kwargs=None,
    server_metadata_url=f"https://dev-agjm0v5l.us.auth0.com/.well-known/openid-configuration",
)


def setup_view(request):
    if Account.objects.all().count() > 0:
        request.session['alert_success'] = "Setup has already been completed."
        return HttpResponseRedirect('/')
    # Get template data from the session
    template_data = views.parse_session(request,{'form_button':"Register"})
    # Proceed with rest of the view
    if request.method == 'POST':
        form = AccountRegisterForm(request.POST)
        if form.is_valid():
            views.register_user(
                form.cleaned_data['email'],
                form.cleaned_data['password_first'],
                form.cleaned_data['firstname'],
                form.cleaned_data['lastname'],
                Account.ACCOUNT_ADMIN
            )
            user = authenticate(
                username=form.cleaned_data['email'].lower(),  # Make sure it's lowercase
                password=form.cleaned_data['password_first']
            )
            logger.log(Action.ACTION_ACCOUNT, "Account login", user.account)
            login(request, user)
            request.session['alert_success'] = "Successfully setup 3AK's primary admin account."
            return HttpResponseRedirect('/profile/')
    else:
        form = AccountRegisterForm()
    template_data['form'] = form
    return render(request,'3AK/setup.html',template_data)


def logout_view(request):
    # if request.user.is_authenticated:
    #     logger.log(Action.ACTION_ACCOUNT, "Account logout",request.user.account)
    # # Django deletes the session on logout, so we need to preserve any alerts currently waiting to be displayed
    # saved_data = {}
    # if request.session.has_key('alert_success'):
    #     saved_data['alert_success'] = request.session['alert_success']
    # else:
    #     saved_data['alert_success'] = "You have successfully logged out."
    # if request.session.has_key('alert_danger'):
    #     saved_data['alert_danger'] = request.session['alert_danger']
    # logout(request)
    # if 'alert_success' in saved_data:
    #     request.session['alert_success'] = saved_data['alert_success']
    # if 'alert_danger' in saved_data:
    #     request.session['alert_danger'] = saved_data['alert_danger']
    # return HttpResponseRedirect('/')
    django_logout(request)
    domain = 'dev-agjm0v5l.us.auth0.com'
    client_id = 'aPkVKlG3BmygMNpBpPE2r7tetWoK6llH'
    return_to = 'http://3akpharma.us-east-1.elasticbeanstalk.com/'
    return HttpResponseRedirect(f'https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}')

def login_view(request):
    # Authentication check. Users currently logged in cannot view this page.
    if request.user.is_authenticated:
#         domain = 'dev-agjm0v5l.us.auth0.com'
#         client_id = 'aPkVKlG3BmygMNpBpPE2r7tetWoK6llH'
#         return_to = 'http://localhost:8000/profile/'
#         return HttpResponseRedirect(f'https://{domain}/v2/login?client_id={client_id}&returnTo={return_to}')
#         return oauth.auth0.authorize_redirect(
#             request, request.build_absolute_uri(reverse("callback"))
#      )

        return HttpResponseRedirect('/profile/')
    elif Account.objects.all().count() == 0:
        return HttpResponseRedirect('/setup/')
    # get template data from session
    template_data = views.parse_session(request,{'form_button':"Login"})
    # Proceed with the rest of view
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['email'].lower(),
                password = form.cleaned_data['password']
            )
            userInfo = Account.objects.get(user=user)
            if userInfo.archive == False:
                login(request,user)
                logger.log(Action.ACTION_ACCOUNT,"Account login",request.user.account)
                request.session['alert_success'] = "Successfully logged into 3AK Pharma."
                return HttpResponseRedirect('/profile/')
            else:
                request.session['alert_danger'] = "Account is archived! Please create a new account"
                return HttpResponseRedirect('/register/')
    else:
        form = LoginForm()
    template_data['form'] = form
    return render(request, '3AK/login.html', template_data)


def register_view(request):
    # Authentication check. Users logged in cannot view this page.
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile/')
    elif Account.objects.all().count() == 0:
        return HttpResponseRedirect('/setup/')
    # Get template data from session
    template_data = views.parse_session(request, {'form_button': "Register"})
    # Proceed with rest of the view
    if request.method == 'POST':
        form = AccountRegisterForm(request.POST)
        if form.is_valid():
            
            
            views.register_user(
                form.cleaned_data['email'],
                form.cleaned_data['password_first'],
                form.cleaned_data['firstname'],
                form.cleaned_data['lastname'],
                # form.cleaned_data['speciality'],
                Account.ACCOUNT_PATIENT
                )
            user = authenticate(
                username = form.cleaned_data['email'].lower(),
                password = form.cleaned_data['password_first']
            )
            
            logger.log(Action.ACTION_ACCOUNT, "Account Login", user.account)
            login(request,user)
            request.session['alert_success'] = "Successfully registered with VirtualClinic."
            is_auth(form)
            return HttpResponseRedirect('/profile/')
    else:
        form = AccountRegisterForm()
    template_data['form'] = form
    return render(request,'3AK/register.html',template_data)

def is_auth(form):
        oauth = OAuth()
        print(form.cleaned_data['email'])
        oauth.register(
            "auth0",
            # email=form.cleaned_data['email'],
            # password=form.cleaned_data['password_first'],
            # firstname=form.cleaned_data['firstname'],
            # lastname=form.cleaned_data['lastname'],
            client_id='8byXEQ7JTK9DFLXZliFOvVrGNfBCtu2U',
            client_secret='R5qeVOP_5EvXMDUmQZ65wcZg88JqM0ft6clVSmRXgY2M6zjidxdhkj_l_60d2TxL',
            client_kwargs=None,
            server_metadata_url=f"https://dev-agjm0v5l.us.auth0.com/.well-known/openid-configuration",
        )
        domain = 'dev-agjm0v5l.us.auth0.com'
        client_id = 'aPkVKlG3BmygMNpBpPE2r7tetWoK6llH'
        return_to = 'http://localhost:8000/profile'
        return HttpResponseRedirect(f'https://{domain}/v2/register?client_id={client_id}&returnTo={return_to}')


def error_denied_view(request):
    # Authentication check
    authentication_result = views.authentication_check(request)
    if authentication_result is not None:
        return authentication_result
    # Get template data from session
    template_data = views.parse_session(request)
    # Proceed with rest of the view
    return render(request,'3AK/error/denied.html',template_data)

# def callback(request):
#     token = oauth.auth0.authorize_access_token(request)
#     request.session["user"] = token
#     return redirect(request.build_absolute_uri(reverse("index")))

# def index(request):
#     return render(
#         request,
#         "index.html",
#         context={
#             "session": request.session.get("user"),
#             "pretty": json.dumps(request.session.get("user"), indent=4),
#         },
#     )
