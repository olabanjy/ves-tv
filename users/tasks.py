from .subscriptionManager import HML


def reconcile_subscription(msisdn, telco):
    try:
        client = HML()
        checkSub = client.checkPhoneStatus(msisdn, telco)
        if checkSub != False:
            if checkSub["data"]["active_subscription"] > 0:
                return True
            return False
            # {
            # "status": true,
            # "status_code": 0,
            # "message": "Report",
            # "data": {
            #     "phone": "2349166345251",
            #     "active_subscription": 1,
            #     "active_products": [
            #     {
            #         "id": 2,
            #         "name": "MTN FC WEEKLY"
            #     }
            #     ],
            #     "total_subscriptions_count": 7
            # }
            # }
        return False

    except Exception as ex:
        print(ex)
        raise
