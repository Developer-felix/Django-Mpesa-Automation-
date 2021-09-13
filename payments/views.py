import json
import os
from datetime import datetime

import firebase_admin
from config import settings
from config.mpesa import lipa_na_mpesa_online
# from consultation.models import Consultation
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.http import HttpResponse
from firebase_admin import db
# from orders.models import Cart
# from orders.models import OrderCheckout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import MpesaPayments, Payments, PaymentMethods
from .serializer import PaymentMethodSerializer, OrderPaymentSerializer


@api_view(['POST', "GET"])
def payment_methods(request, version):
    if request.method == "POST":
        payment_serializer = PaymentMethodSerializer(data=request.data, context={"request": request})
        if payment_serializer.is_valid():
            payment_serializer.save(user_id=request.user.id)
        else:
            return Response({"success": False, "errors": payment_serializer.errors, "status_code": 1,
                             "status_message": "failed", "message": "Cannot add payment method",
                             "data": None}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": True, "errors": None, "status_code": 0,
                         "status_message": "success", "message": "Successfully created  payment method",
                         "data": None}, status=status.HTTP_200_OK)
    if request.method == "GET":
        payment_methods = PaymentMethods.objects.all()
        payment_method_serializer = PaymentMethodSerializer(payment_methods, context={"request": request}, many=True)
        return Response({
            "success": True,
            "errors": None,
            "status_code": 0,
            "status_message": "success",
            "message": "successfully retrieved payment method",
            'data': payment_method_serializer.data, })


@api_view(["POST", 'GET'])
def order_payment(request, version):
    if request.method == "POST":
        if request.data['payment_method'] == "MPESA":

            amount_to_pay = 0
            # get the total amount to be paid
            if "order_id" in request.data:
                try:
                    order = OrderCheckout.objects.get(id=request.data['order_id'])
                    # check if order is paid for
                    if order.is_paid:
                        return Response({"success": False,
                                         "errors": [{"Payment Error": "Order is already paid "}],
                                         "status_code": 1, "status_message": "failed",
                                         "message": "Cannot process payment request",
                                         "data": None}, status=status.HTTP_400_BAD_REQUEST)

                    if order.delivery_cost is not None:
                        amount_to_pay = float(order.total_cost) + float(order.delivery_cost)
                    else:
                        amount_to_pay = float(order.total_cost)

                    order_payment_request = lipa_na_mpesa_online(phone_number='254704494519', amount=1,
                                                                 account_reference=1234,
                                                                 transaction_description='order_payment',
                                                                 call_back_url="lipa_na_mpesa_listener")
                    payment_response = json.loads(order_payment_request)

                    if "ResponseCode" in payment_response and int(payment_response['ResponseCode']) == 0:
                        response_code = payment_response['ResponseCode']
                        merchant_request_id = payment_response['MerchantRequestID']
                        checkout_request_id = payment_response['CheckoutRequestID']
                        response_description = payment_response['ResponseDescription']
                        customer_message = payment_response['CustomerMessage']
                        # save mpesa transaction information
                        try:
                            mpesa_transaction = MpesaPayments.objects.create(
                                user_id=request.user.id,
                                amount=amount_to_pay,
                                order_id=request.data['order_id'],
                                response_code=response_code,
                                phone_no=request.data['phone_no'],
                                merchant_request_id=merchant_request_id,
                                checkout_request_id=checkout_request_id,
                                description=response_description
                            )
                        except:
                            return Response({"success": False,
                                             "errors": [{"Payment Error": "Cannot process payment Request"}],
                                             "status_code": 1, "status_message": "failed",
                                             "message": "Cannot process payment request",
                                             "data": None}, status=status.HTTP_400_BAD_REQUEST)

                        return Response({
                            "success": True,
                            "errors": None,
                            "status_code": 0,
                            "status_message": "success",
                            "message": "successfully sent a payment request ",
                            'data': None, })

                except:
                    return Response({"success": False,
                                     "errors": [{"Payment Error": "Cannot process payment Request"}],
                                     "status_code": 1, "status_message": "failed",
                                     "message": "Order is invalid",
                                     "data": None}, status=status.HTTP_400_BAD_REQUEST)

                # check if order has been fully paid

            return Response({"success": False, "errors": [{"Payment Error": "Cannot process payment Request"}],
                             "status_code": 1, "status_message": "failed", "message": "Cannot proccess payment request",
                             "data": None}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": False, "errors": [{"Payment Error": "Invalid Payment Method"}],
                         "status_code": 1, "status_message": "failed",
                         "message": "Cannot process payment request. Invalid payment method",
                         "data": None}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":

        nextPage = 1
        previousPage = 1
        page = request.GET.get('page', 1)
        if request.user is not None and not request.user.is_admin:
            order_payment = Payments.objects.filter(user_id=request.user.id)
        else:
            order_payment = Payments.objects.all()
        paginator = Paginator(order_payment, 20)
        try:
            orders_payment_data = paginator.page(page)
        except PageNotAnInteger:
            orders_payment_data = paginator.page(1)
        except EmptyPage:
            orders_payment_data = paginator.page(paginator.num_pages)

        serializer = OrderPaymentSerializer(orders_payment_data, context={"request": request}, many=True)
        if orders_payment_data.has_next():
            nextPage = orders_payment_data.next_page_number()
        if orders_payment_data.has_previous():
            previousPage = orders_payment_data.previous_page_number()

        return Response({
            "success": True,
            "errors": None,
            "status_code": 0,
            "status_message": "success",
            "message": "successfully retrieved order payment",
            'data': serializer.data, 'count': paginator.count, 'numpages': paginator.num_pages,
            'nextlink': '/api/' + version + '/order_payment/?page=' + str(nextPage),
            'prevlink': '/api/' + version + '/order_payment/?page=' + str(previousPage)})


@api_view(['POST', "GET"])
def lipa_na_mpesa_listener(request, version):
    try:
        f = open(settings.MEDIA_ROOT + f"/mpesa/orders/{datetime.now().strftime('%Y%m%d')}_stks.txt", 'a')
    except Exception as e:
        try:
            os.mkdir(os.path.join(settings.MEDIA_ROOT, 'mpesa/'))
        except Exception as e:
            os.mkdir(os.path.join(settings.MEDIA_ROOT, 'mpesa/orders/'))
        f = open(settings.MEDIA_ROOT + f"/mpesa/orders/{datetime.now().strftime('%Y%m%d')}_stks.txt", 'a')
    f.write(str(request.data) + "\n")
    merchant_request_id = request.data['Body']['stkCallback']['MerchantRequestID']
    checkout_request_id = request.data['Body']['stkCallback']['CheckoutRequestID']
    result_desc = request.data['Body']['stkCallback']['ResultDesc']

    # trace and update transaction
    try:
        mpesa_payment = MpesaPayments.objects.filter(
            merchant_request_id=merchant_request_id,
            checkout_request_id=checkout_request_id,
        ).last()

    except:
        mpesa_payment = None
    if "ResultCode" in request.data['Body']['stkCallback'] and int(
            request.data['Body']['stkCallback']['ResultCode']) == 0:

        result_code = request.data['Body']['stkCallback']['ResultCode']
        if "CallbackMetadata" in request.data['Body']['stkCallback']:
            amount = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
            mpesa_receipt_number = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
            transaction_date = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']
            phone_number = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][4]["Value"]
            # update  payment values
            mpesa_payment.mpesa_code = mpesa_receipt_number
            mpesa_payment.completed_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            mpesa_payment.save()

            with transaction.atomic():
                try:
                    payment = Payments.objects.filter(payment_reference_id=mpesa_payment.id)
                except:
                    payment = []

                #   record a payment
                try:
                    payment_method = PaymentMethods.objects.filter(name="MPESA").last().id
                except:
                    payment_method = None
                try:
                    if payment.count() == 0:
                        payment = Payments.objects.create(
                            user_id=mpesa_payment.user_id,
                            amount=amount,
                            payment_method_id=payment_method,
                            payment_receipt_no=mpesa_payment.mpesa_code,
                            payment_reference_id=mpesa_payment.id,
                            transaction_status="completed",
                            completed_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        )
                except:
                    payment = []

                # update order to paid
                order_check_out = OrderCheckout.objects.get(id=mpesa_payment.order_id)
                # update the payment status
                if order_check_out.delivery_cost is not None:
                    amount_to_pay = float(order_check_out.total_cost) + float(order_check_out.delivery_cost)
                else:
                    amount_to_pay = float(order_check_out.total_cost)
                if amount_to_pay >= float(amount):
                    order_check_out.is_paid = True
                else:
                    order_check_out.is_paid = False
                # return Response("Cart.objects.filter(order_check_out.cart_id).last().id")
                # todo update payments to correct on going live
                Cart.objects.filter(cart_id=order_check_out.cart_id).update(
                    is_paid=True,
                    is_checked_out=True,
                    order_complete=True,
                )
                order_check_out.is_paid = True
                order_check_out.receipt_no = mpesa_payment.mpesa_code
                order_check_out.save()

    else:
        mpesa_payment.description = f"{mpesa_payment.description} | {result_desc}"
        mpesa_payment.save()

    return HttpResponse(request.data)


@api_view(['POST', "GET"])
def consult_lipa_na_mpesa_listener(request, version):
    try:
        f = open(settings.MEDIA_ROOT + f"/mpesa/consultation/{datetime.now().strftime('%Y%m%d')}_stks.txt", 'a')
    except Exception as e:
        try:
            os.mkdir(os.path.join(settings.MEDIA_ROOT, 'mpesa/'))
        except:
            os.mkdir(os.path.join(settings.MEDIA_ROOT, 'mpesa/consultation/'))
        f = open(settings.MEDIA_ROOT + f"/mpesa/consultation/{datetime.now().strftime('%Y%m%d')}_stks.txt", 'a')
        # print(e)
    f.write(str(request.data) + "\n")
    merchant_request_id = request.data['Body']['stkCallback']['MerchantRequestID']
    checkout_request_id = request.data['Body']['stkCallback']['CheckoutRequestID']
    result_desc = request.data['Body']['stkCallback']['ResultDesc']

    # trace and update transaction
    # try:
    mpesa_payment = MpesaPayments.objects.filter(
            merchant_request_id=merchant_request_id,
            checkout_request_id=checkout_request_id,
        ).last()

    # except:
    #     mpesa_payment = None
    if "ResultCode" in request.data['Body']['stkCallback'] and int(
            request.data['Body']['stkCallback']['ResultCode']) == 0 :

        result_code = request.data['Body']['stkCallback']['ResultCode']
        if "CallbackMetadata" in request.data['Body']['stkCallback']:
            amount = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
            mpesa_receipt_number = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
            transaction_date = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']
            phone_number = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][3]["Value"]
            # update  payment values
            mpesa_payment.mpesa_code = mpesa_receipt_number
            mpesa_payment.completed_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            mpesa_payment.save()
            try:
                payment = Payments.objects.filter(payment_reference_id=mpesa_payment.id)
            except:
                payment = None
            #   record a payment
            try:
                payment_method = PaymentMethods.objects.filter(name="MPESA").last().id
            except:
                payment_method = None
            try:

                if payment is None or payment.count() == 0:
                    payment = Payments.objects.create(
                        user_id=mpesa_payment.user_id,
                        amount=amount,
                        payment_method_id=payment_method,
                        payment_receipt_no=mpesa_payment.mpesa_code,
                        payment_reference_id=mpesa_payment.id,
                        transaction_status="completed",
                        completed_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    )

            except:
                payment = None

            # update order to paid
            consultation_request = Consultation.objects.get(id=mpesa_payment.order_id)
            # update the payment status

            if consultation_request.amount >= float(amount):
                consultation_request.is_paid = True

            else:
                consultation_request.is_paid = False

            consultation_request.receipt_no = mpesa_payment.mpesa_code
            consultation_request.save()

            fetch_base_response = fetch_firebase(
                str(consultation_request.patient_id) + "_" + str(consultation_request.doctor_id))
            if fetch_base_response == 0:
                Response("Firebase Update")
            else:
                return Response("payment logged")


    elif mpesa_payment is not None:
        mpesa_payment.description = f"{mpesa_payment.description} | {result_desc}"
        mpesa_payment.save()
        return Response("payment error logged")

    else:
        return Response("No payment logged")
        return HttpResponse(request.data)


def fetch_firebase(doctor_id_patient_id):
    try:
        url = os.path.join(settings.BASE_DIR) + '/media/ponasasa-6ce7c-firebase-adminsdk-9g8wm-97a5e47ca2.json'
        cred_obj = firebase_admin.credentials.Certificate(url)
        default_app = firebase_admin.initialize_app(cred_obj, {
            'databaseURL': "https://ponasasa-6ce7c.firebaseio.com"
        })
        consultations = db.reference("/ponasasa/consultation")
        single_consult = consultations.child(doctor_id_patient_id)
        single_consult.update({'consultation_status': "ConsultationStatus.active"})
    except:
        return 1

    # for key, value in consultation.get().items():

    return 0
