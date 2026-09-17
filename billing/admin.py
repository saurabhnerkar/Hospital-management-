from django.contrib import admin
from .models import Bill, Payment, BillingHistory

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_no', 'patient', 'doctor', 'total_amount', 'payment_status', 'bill_date')
    list_filter = ('payment_status', 'bill_date')
    search_fields = ('bill_no', 'patient__name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('receipt_no', 'bill', 'amount_paid', 'payment_mode', 'payment_date')
    list_filter = ('payment_mode', 'payment_date')
    search_fields = ('receipt_no', 'transaction_id')

@admin.register(BillingHistory)
class BillingHistoryAdmin(admin.ModelAdmin):
    list_display = ('action', 'bill', 'created_at')
    list_filter = ('created_at',)
