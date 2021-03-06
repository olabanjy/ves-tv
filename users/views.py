from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseForbidden,
    HttpResponseServerError,
    JsonResponse,
)
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives, send_mail, EmailMessage
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils.encoding import force_bytes
from django.utils.timezone import make_aware
from paystackapi.paystack import Paystack
from django.db.models import Sum
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.timezone import make_aware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import time, re, random, string, math
from decimal import Decimal
from datetime import timedelta, date, datetime, time
from dateutil.relativedelta import relativedelta
from .models import *
from .subscriptionManager import subscribeManager
import json
import xmltodict


@login_required
def after_signup(request):
    # get user msisdn
    msisdn = request.user.profile.phone
    sub = subscribeManager(msisdn)
    print(sub)
    print(sub["result"])
    # check subscription status
    ###########

    return redirect("users:awaiting_response")


@login_required
def awaiting_response(request):
    template = "users/awaiting_response.html"
    return render(request, template)


@login_required
def after_login(request):
    msisdn = request.user.username
    # check sub status
    sub_qs = Subscribtion.objects.filter(user=request.user.profile, sub_active=True)
    if sub_qs.exists():
        return redirect("core:home")
    else:
        return redirect("users:inactive_account")


def onboarding(request):

    template = "users/subscribe_page.html"

    context = {"msisdn": request.user.profile.phone}

    return render(request, template, context)


def inactive_account(request):

    template = "users/inactive_account.html"

    context = {}
    return render(request, template, context)


# DATA SYNC
@require_POST
@csrf_exempt
def data_sync(request):
    print("Receiving from AGT datasync")
    dict_data = xmltodict.parse(request.body)
    print(dict_data)

    the_req_body = f"{request.body}"

    try:
        new_sync = WebhookBackup.objects.create(req_body=the_req_body)
    except:
        pass

    userID = dict_data["soapenv:Envelope"]["soapenv:Body"]["ns2:syncOrderRelation"][
        "ns2:userID"
    ]["ID"]
    userIDType = dict_data["soapenv:Envelope"]["soapenv:Body"]["ns2:syncOrderRelation"][
        "ns2:userID"
    ]["type"]

    productID = dict_data["soapenv:Envelope"]["soapenv:Body"]["ns2:syncOrderRelation"][
        "ns2:productID"
    ]
    updateType = dict_data["soapenv:Envelope"]["soapenv:Body"]["ns2:syncOrderRelation"][
        "ns2:updateType"
    ]
    updateTime = dict_data["soapenv:Envelope"]["soapenv:Body"]["ns2:syncOrderRelation"][
        "ns2:updateTime"
    ]
    updateDesc = dict_data["soapenv:Envelope"]["soapenv:Body"]["ns2:syncOrderRelation"][
        "ns2:updateDesc"
    ]
    effectiveTime = dict_data["soapenv:Envelope"]["soapenv:Body"][
        "ns2:syncOrderRelation"
    ]["ns2:effectiveTime"]
    expiryTime = dict_data["soapenv:Envelope"]["soapenv:Body"]["ns2:syncOrderRelation"][
        "ns2:expiryTime"
    ]
    print(userID)
    print(userIDType)
    print(productID)
    print(updateType)
    print(updateDesc)

    theUpdateTime = datetime.strptime(str(updateTime), "%Y%m%d%H%M%S")
    theEffectiveTime = datetime.strptime(str(effectiveTime), "%Y%m%d%H%M%S")
    theExpiryTime = datetime.strptime(str(expiryTime), "%Y%m%d%H%M%S")
    theUserPhoneNumber = str(userID).replace("234", "0", 1)

    print(theUpdateTime)
    print(theEffectiveTime)
    print(theExpiryTime)

    the_user = User.objects.get(username=theUserPhoneNumber)
    the_user_profile = Profile.objects.get(user=the_user)

    the_user_sub, created = Subscribtion.objects.get_or_create(user=the_user_profile)
    """
    Update Type
    1. Add
    2. Delete
    3. Update
    """
    if updateType == "1":
        the_user_sub.sub_active = True
        the_user_sub.starts_date = make_aware(theEffectiveTime)
        the_user_sub.ends_date = make_aware(theExpiryTime)

    elif updateType == "2":
        the_user_sub.sub_active = False

    elif updateType == "3":
        the_user_sub.sub_active = True
        the_user_sub.starts_date = make_aware(theEffectiveTime)
        the_user_sub.ends_date = make_aware(theExpiryTime)

    the_user_sub.save()

    return HttpResponse(200)

    # response_body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    #                 xmlns:loc="http://www.csapi.org/schema/parlayx/data/sync/v1_0/local">
    #                     <soapenv:Header/>
    #                     <soapenv:Body>
    #                         <loc:syncOrderRelationResponse>
    #                             <loc:result>0</loc:result>
    #                             <loc:resultDescription>OK</loc:resultDescription>
    #                         </loc:syncOrderRelationResponse>
    #                     </soapenv:Body>
    #                 </soapenv:Envelope>"""

    # return response_body
