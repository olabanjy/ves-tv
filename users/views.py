from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
)
from django.views.decorators.http import require_POST

from django.shortcuts import redirect

from django.views.decorators.csrf import csrf_exempt


import random, string

from datetime import datetime

from .models import *

from .subscriptionManager import HML
import json

from . import choices


import requests

import string
import random


def subscribe(request):
    # fetch msisdn
    # if mtn, use secureD redirect
    # if airtel, call endpoint
    client = HML()
    if "Msisdn" in request.headers:
        msisdn = request.headers["Msisdn"]
        # get user msisdn

        checkNetwork = client.checkNetwork(msisdn)
        if checkNetwork == "AIRTEL":
            sub = client.subscribe(msisdn, choices.Telco.AIRTEL.value)
            if sub != False:
                print("Subscribtion Successfull")
                return redirect("core:awaiting_response")
            return redirect("core:onboarding")
        # elif checkNetwork == "MTN":
        else:
            # send to secureD for redirection
            N = 7
            res = "".join(random.choices(string.ascii_lowercase + string.digits, k=N))

            redirect_url = f"http://ng-app.com/CloudIntegrated/VESTV-24-No-23410220000022939-web?trxId={res}"

            return redirect(redirect_url)

    return redirect("core:onboarding")


def cancelSubscribtion(request):
    if "Msisdn" in request.headers:
        msisdn = request.headers["Msisdn"]
        # get user msisdn
        client = HML()

        checkNetwork = client.checkNetwork(msisdn)
        if checkNetwork == "AIRTEL":
            unSub = client.unSubscribe(msisdn, choices.Telco.AIRTEL.value)
        # elif checkNetwork == "MTN":
        else:
            unSub = client.unSubscribe(msisdn, choices.Telco.MTN.value)

        if unSub != False:
            print("Un-Subscribtion Successfull")
            return redirect("core:home")
        else:
            print("Subscribtion UnSuccessfull")
            return redirect("core:home")
    else:
        return redirect("users:onboarding")


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
            try:
                new_sync.telco = "MTN"
                new_sync.save()
            except:
                pass
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
            theUser.telco = "MTN"
            theUser.save()
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

                try:
                    # check campaign tracker is msisdn is there
                    find_promo_msisdn = CampaignTracker.objects.filter(
                        msisdn=msisdn
                    ).first()
                    postbackUrl = f"https://postback.level23.nl/?currency=USD&handler=11349&hash=63857b26c564dd6b79e5a2fb1bb209e8&tracker={find_promo_msisdn.click_id}"
                    send_postback = requests.get(postbackUrl)
                    find_promo_msisdn.converted = True
                    find_promo_msisdn.save()
                    print(send_postback)
                except:
                    pass
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
        elif the_data["telco"] == "AIRTEL":
            try:
                new_sync.telco = "AIRTEL"
                new_sync.save()
            except:
                pass
            # handle access
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
