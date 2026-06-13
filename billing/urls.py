from django.urls import path
from . import views
from django.urls import include

app_name = 'billing'

urlpatterns = [

    path(
        'generate/',
        views.generate_bill,
        name='generate_bill'
    ),

    path(
        'bills/',
        views.bill_list,
        name='bill_list'
    ),

    path(
        'bill/<int:bill_id>/',
        views.bill_detail,
        name='bill_detail'
    ),

    path(
        'payment/<int:bill_id>/',
        views.make_payment,
        name='payment'
    ),

    path(
        'receipt/<int:payment_id>/',
        views.receipt,
        name='receipt'
    ),

    path(
        'payments/',
        views.payment_history,
        name='payment_history'
    ),

    path(
        'revenue/',
        views.revenue_report,
        name='revenue_report'
    ),
]