from django.contrib import admin
from . models import User, Loan, Payment, CreditScore,  Transaction, Referral, Penalty, LoanOffer
# Register your models here.

admin.site.register(User)
admin.site.register(Loan)
admin.site.register(Payment)
admin.site.register(CreditScore)
admin.site.register(Transaction)
admin.site.register(Referral)
admin.site.register(Penalty)
admin.site.register(LoanOffer)