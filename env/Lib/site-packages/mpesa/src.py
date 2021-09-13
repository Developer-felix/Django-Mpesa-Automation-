import requests
from requests.auth import HTTPBasicAuth

#Generates access token
def access_token():
    consumer_key = "YOUR_APP_CONSUMER_KEY"
    consumer_secret = "YOUR_APP_CONSUMER_SECRET"

    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    print(r.text)
    
#B2C payment Request
def b_to_c():
    access_token = "Access-Token"
    api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
    headers = { "Authorization": "Bearer %s" % access_token }
    request = {
        "InitiatorName": "",
        "SecurityCredential":"",
        "CommandID": "",
        "Amount": "",
        "PartyA": "",
        "PartyB": "",
        "Remarks": "",
        "QueueTimeOutURL": "https://your_timeout_url",
        "ResultURL": "https://your_result_url",
        "Occasion": ""
               }
    response = requests.post(api_url, json = request, headers=headers)
    print (response.text)

#B2B Payment Request
def b_to_b():
    access_token = "Access-Token"
    api_url = "https://sandbox.safaricom.co.ke/mpesa/b2b/v1/paymentrequest"
    headers = { "Authorization": "Bearer %s" % access_token }
    request = {
        "Initiator": "",
        "SecurityCredential": "",
        "CommandID": "",
        "SenderIdentifierType": "",
        "RecieverIdentifierType": "",
        "Amount": "",
        "PartyA": "",
        "PartyB": "",
        "AccountReference": "",
        "Remarks": "",
        "QueueTimeOutURL": "https://your_timeout_url",
        "ResultURL": "https://your_result_url"
    }

    response = requests.post(api_url, json = request, headers=headers)
    print (response.text)

"""#C2B registering URLs
def c_b_register():
    access_token = "GJs9H5cZeFEkQUXtAWd9Urc4ccMk"
    api_url = "http://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "ShortCode": "601406",
        "ResponseType": "Completed",
        "ConfirmationURL": "https://hookb.in/vgLlPBrO",
        "ValidationURL": "https://hookb.in/vgLlPBrO"
    }

    response = requests.post(api_url, json = request, headers=headers)
    print (response.text)"""

#C2B transaction simulation
def c_b_simulate():
    access_token = "Access-Token"
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "ShortCode":"",
        "CommandID":"CustomerPayBillOnline or CustomeBuyGoodsOnline",
        "Amount":"",
        "Msisdn":"",
        "BillRefNumber":""
    }
    response = requests.post(api_url, json = request, headers=headers)
    print (response.text)

#finds the current account bal for a particular account
def account_bal():
    access_token = "Access-Token"
    api_url = "https://sandbox.safaricom.co.ke/mpesa/accountbalance/v1/query"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "Initiator":"",
        "SecurityCredential":"",
        "CommandID":"AccountBalance",
        "PartyA":"shortcode",
        "IdentifierType":"4",
        "Remarks":"Remarks",
        "QueueTimeOutURL":"https://ip_address:port/timeout_url",
        "ResultURL":"https://ip_address:port/result_url"
        }
    response = requests.post(api_url, json = request, headers=headers)
    print (response.text)

#reverses a transaction
def reversal():
    access_token = "Access-Token"
    api_url = "https://sandbox.safaricom.co.ke/mpesa/reversal/v1/request"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "Initiator":"",
        "SecurityCredential":"",
        "CommandID":"TransactionReversal",
        "TransactionID":"",
        "Amount":"",
        "ReceiverParty":"",
        "RecieverIdentifierType":"4",
        "ResultURL":"https://ip_address:port/result_url",
        "QueueTimeOutURL":"https://ip_address:port/timeout_url",
        "Remarks":"",
        "Occasion":""
    }
    response = requests.post(api_url, json = request, headers=headers)
    print (response.text)

#lipa na mpesa query
def LNMQ():
    access_token = "Access-Token"
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = { 
        "BusinessShortCode": "" ,
        "Password": "",
        "Timestamp": "",
        "CheckoutRequestID": ""
    }
    response = requests.post(api_url, json = request, headers=headers)
    print (response.text)

#lipa na mpesa payment
def LNMP():
    access_token = "Access-Token"
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = { "Authorization": "Bearer %s" % access_token }
    request = {
        "BusinessShortCode": "",
        "Password": "",
        "Timestamp": "",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": "1",
        "PartyA": "",
        "PartyB": "",
        "PhoneNumber": "",
        "CallBackURL": "https://ip_address:port/callback",
        "AccountReference": "",
        "TransactionDesc": ""
    }
    response = requests.post(api_url, json = request, headers=headers)

    print (response.text)

#gets the status of a certain transaction
def status():
    access_token = "qgmZz0TOQvm4w6oCYRVdmmq8qSZD"
    api_url = "https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query"
    headers = { "Authorization": "Bearer %s" % access_token }
    request = {
       "Initiator":"testapi406",
       "SecurityCredential":"",
       "CommandID":"TransactionStatusQuery",
       "TransactionID":" ",
       "PartyA":" ",
       "IdentifierType":"1",
       "ResultURL":"https://ip_address:port/result_url",
       "QueueTimeOutURL":"https://ip_address:port/timeout_url",
       "Remarks":" ",
       "Occasion":" "
    }
    response = requests.post(api_url, json = request, headers=headers)
    print (response.text)


