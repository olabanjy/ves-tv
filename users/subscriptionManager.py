import requests
from datetime import timedelta, date, datetime
import hashlib
import json
import xmltodict
import untangle


url = "http://152.32.141.26:6991/SubscribeManageService/services/SubscribeManage"
spID = "2340110011662"
password = 123456
timeStamp = datetime.now()
operCode = "NG"
userType = 0
subInfo = None
productID = "23401220000028735"  # change this product ID later
channelID = 1


spPassword_hash_object = hashlib.md5((f"{spID}{password}{timeStamp}").encode())
spPassword = spPassword_hash_object.hexdigest()


def subscribeManager(msisdn):
    userID = msisdn.replace("0", "234", 1)
    print(userID)
    args = {
        "spPassword": spPassword,
        "timeStamp": timeStamp,
        "productID": productID,
        "userID": userID,
        "operCode": operCode,
    }

    body = """<?xml version=\"1.0\" encoding=\"utf-8\"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
            xmlns:loc="http://www.csapi.org/schema/parlayx/subscribe/manage/v1_0/local">
                <soapenv:Header>
                    <tns:RequestSOAPHeader xmlns:tns="http://www.huawei.com.cn/schema/common/v2_1">
                        <tns:spId>2340110011662</tns:spId>
                        <tns:spPassword>{spPassword}</tns:spPassword>
                        <tns:timeStamp>{timeStamp}</tns:timeStamp>
                    </tns:RequestSOAPHeader>
                </soapenv:Header>
                <soapenv:Body>
                    <loc:subscribeProductRequest>
                        <loc:subscribeProductReq>
                            <userID>
                            <ID>{userID}</ID>
                            <type>0</type>
                            </userID>
                            <subInfo>
                                <productID>{productID}</productID>
                                <operCode>{operCode}</operCode> 
                                <isAutoExtend>0</isAutoExtend>
                                <channelID>1</channelID>
                            </subInfo>
                        </loc:subscribeProductReq>
                    </loc:subscribeProductRequest>
                </soapenv:Body>
            </soapenv:Envelope>""".format(
        **args
    )
    headers = {
        "content-type": "text/xml; charset=utf-8",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Accept": "/",
    }

    response = requests.request("POST", url, data=body, headers=headers)

    dict_data = xmltodict.parse(response.content)
    print(dict_data)

    return dict_data["S:Envelope"]["S:Body"]["ns3:subscribeProductResponse"][
        "ns3:subscribeProductRsp"
    ]
