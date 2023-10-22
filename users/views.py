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
from .subscriptionManager_old import subscribeManager
from .subscriptionManager import mtnSubscribe, mtnUnSubscribe
import json
import xmltodict


def subscribe(request):
    if "Msisdn" in request.headers:
        msisdn = request.headers["Msisdn"]
        # get user msisdn

        sub = mtnSubscribe(msisdn)

        if sub != False:
            print("Subscribtion Successfull")
            return redirect("core:awaiting_response")
        else:
            print("Subscribtion UnSuccessfull")
            return redirect("core:onboarding")
    else:
        return redirect("core:onboarding")
        # return redirect("users:awaiting_response")


def cancelSubscribtion(request):
    if "Msisdn" in request.headers:
        msisdn = request.headers["Msisdn"]
        # get user msisdn

        sub = mtnUnSubscribe(msisdn)

        if sub != False:
            print("Un-Subscribtion Successfull")
            return redirect("core:home")
        else:
            print("Subscribtion UnSuccessfull")
            return redirect("core:home")
    else:
        return redirect("users:onboarding")


@login_required
def after_signup(request):
    # get user msisdn
    msisdn = request.user.profile.phone
    sub = mtnSubscribe(msisdn)
    print(sub)
    # check subscription status
    ###########

    return redirect("core:awaiting_response")


# DATA SYNC
@require_POST
@csrf_exempt
def data_sync(request):
    print("Receiving from HML datasync")

    the_data = json.loads(request.body)
    print(the_data)

    try:
        new_sync = WebhookBackup.objects.create(req_body=f"{request.body}")
    except:
        pass
    try:
        if the_data["telco"] == "MTN":
            not_type = the_data[
                "type"
            ]  # UNSUBSCRIPTION_NOTIFICATION, SYNC_NOTIFICATION
            msisdn = the_data["details"]["phone"]
            # "%Y-%m-%dT%H:%M:%S.%fZ",

            prod_type = the_data["product"]["type"]
            # sub_type = the_data["product"]["subscription_type"]
            print("prod_type", prod_type)

            if msisdn.startswith("0") and len(msisdn) == 11:
                msisdn = msisdn.replace("0", "234", 1)

            # fetch user
            theUser, created = UserProfile.objects.get_or_create(phone=msisdn)
            userSub, created = UserSubscribtion.objects.get_or_create(user=theUser)
            if not_type == "SYNC_NOTIFICATION":
                start_date = the_data["details"]["date"]
                start_datetime = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
                end_date = the_data["details"]["expiry"]
                end_datetime = datetime.strptime(end_date, "%Y-%m-%d %H:%M")

                userSub.sub_active = True
                userSub.starts_date = start_datetime
                userSub.ends_date = end_datetime
                userSub.save()

                theUser.sub_status = "active"
                theUser.save()
                return HttpResponse(200)

            elif not_type == "UNSUBSCRIPTION_NOTIFICATION":
                print("this is a unsubscribtion request")
                userSub.sub_active = False
                userSub.save()

                theUser.sub_status = "inactive"
                theUser.save()

                print("done with unsubscribtion")
                return HttpResponse(200)

            elif not_type == "RENEWAL_NOTIFICATION":
                """
                b'{"type":"RENEWAL_NOTIFICATION","telco":"MTN","action":"NONE","shortcode":null,"product":{"id":70,"name":"Magic Box Daily","identity":"PD-16541987951000","type":"SUBSCRIPTION","subscription_type":"ONETIME_AND_RECURRING","status":"LIVE"},"details":{"phone":"2347047344879","amount":5000,"channel":"system-renewal","date":"2023-01-07 08:58","expiry":"2023-01-08 08:58","auto_renewal":true,"telco_status_code":"0","telco_ref":"upstream_paid_2617724eebdbc3e8"}}'
                """
                start_date = the_data["details"]["date"]
                start_datetime = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
                end_date = the_data["details"]["expiry"]
                end_datetime = datetime.strptime(end_date, "%Y-%m-%d %H:%M")

                userSub.sub_active = True

                userSub.starts_date = start_datetime
                userSub.ends_date = end_datetime

                try:
                    userSub.first_sub = False
                    userSub.renewal_sub = True
                    if the_data["details"]["auto_renewal"] == True:
                        userSub.auto_renewal = True
                except:
                    pass
                userSub.save()

                theUser.sub_status = "active"
                theUser.save()
                return HttpResponse(200)
            else:
                return HttpResponse(200)
        else:
            return HttpResponse(200)
    except Exception as e:
        print(e)
        return HttpResponse(200)


@require_POST
@csrf_exempt
def campaign_notification(request):
    try:
        the_data = json.loads(request.body)
        print(the_data)

        try:
            new_sync = CampaignNotificationBackup.objects.create(
                req_body=f"{request.body}"
            )
        except:
            pass
    except Exception as e:
        print("error", e)
        pass

    return HttpResponse(200)


#### Vendor Onboarding
