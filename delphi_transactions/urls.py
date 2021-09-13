from django.conf.urls import url

from .views import (accounts,read_smart_contracts,send_transactions)

app_name = "delphi_transactions"
urlpatterns = [
    url(r'^accounts/$', accounts, name="accounts"),
    url(r'^read_smart_contracts/$', read_smart_contracts, name="read_smart_contracts"),
    url(r'^send_transactions/$', send_transactions, name="send_transactions"),
]