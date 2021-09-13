from django.conf.urls import url

from .views import *

app_name = "payments"
urlpatterns = [
    url(r'^order_payment/$', order_payment, name="order_payment"),
    url(r'^payment_methods/$', payment_methods, name="payment_methods"),
    url(r'^lipa_na_mpesa_listener/$', lipa_na_mpesa_listener, name="lipa_na_mpesa_listener"),
    url(r'^consult_lipa_na_mpesa_listener/$', consult_lipa_na_mpesa_listener, name="consult_lipa_na_mpesa_listener"),
    url(r'^fetch_firebase/$', fetch_firebase, name="fetch_firebase"),
]
