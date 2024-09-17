from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not phone_number:
            raise ValueError('Users must have a phone number')

        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, phone_number, password, **extra_fields)

# Custom User Model
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    national_id = models.CharField(unique=True, max_length=20)
    is_verified = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    credit_score = models.IntegerField(default=0)
    employment_status = models.CharField(max_length=50, choices=[('Employed', 'Employed'), ('Self-Employed', 'Self-Employed')], null=True, blank=True)
    income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    loan_eligibility_status = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name



from django.db import models
from django.utils import timezone

class LoanType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Loan(models.Model):
    LOAN_STATUS_CHOICES = [
        ('Approved', 'Approved'),
        ('Disbursed', 'Disbursed'),
        ('Repayed', 'Repayed'),
        ('Defaulted', 'Defaulted'),
    ]
    
    borrower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='loans')
    loan_type = models.ForeignKey('LoanType', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    loan_term = models.PositiveIntegerField(help_text="Term in months")
    status = models.CharField(max_length=20, choices=LOAN_STATUS_CHOICES, default='Approved')
    disbursed_date = models.DateField(null=True, blank=True)
    repayment_date = models.DateField(null=True, blank=True)
    total_repayment_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    penalty_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remaining_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Loan {self.id} - {self.borrower.email}'

    def calculate_total_repayment(self):
        # Logic to calculate total repayment amount including interest
        pass

    def calculate_remaining_balance(self):
        # Logic to calculate remaining balance
        pass



from django.db import models
from django.utils import timezone

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Bank Transfer', 'Bank Transfer'),
        ('Mobile Money', 'Mobile Money'),
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
    ]

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)
    transaction_id = models.CharField(max_length=50, unique=True)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Completed')
    notes = models.TextField(null=True, blank=True)
    
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='payments')
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Payment {self.transaction_id} - {self.amount}'

    def get_payment_details(self):
        return f'Amount: {self.amount}, Date: {self.payment_date}, Method: {self.method}, Status: {self.status}'




class CreditScore(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='credit_score_record')
    score = models.IntegerField()
    score_date = models.DateField(default=timezone.now)
    adjustment_reason = models.CharField(max_length=255, null=True, blank=True)
    adjustment_date = models.DateField(null=True, blank=True)
    adjustment_amount = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Credit Score for {self.user.email} - Score: {self.score}'

    def adjust_score(self, amount, reason):
        self.score += amount
        self.adjustment_amount = amount
        self.adjustment_reason = reason
        self.adjustment_date = timezone.now().date()
        self.save()

    def get_score_history(self):
        return f'Score: {self.score}, Last Updated: {self.score_date}, Adjustment: {self.adjustment_amount}, Reason: {self.adjustment_reason}'



from django.db import models
from django.utils import timezone

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('Loan Disbursement', 'Loan Disbursement'),
        ('Payment', 'Payment'),
        ('Adjustment', 'Adjustment'),
        ('Refund', 'Refund'),
        ('Fee', 'Fee'),
    ]
    
    TRANSACTION_STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
    ]
    
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_date = models.DateField(default=timezone.now)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES, default='Completed')
    reference_number = models.CharField(max_length=50, unique=True)
    
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE, null=True, blank=True, related_name='transactions')
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, null=True, blank=True, related_name='transactions')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='transactions')
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Transaction {self.reference_number} - {self.transaction_type} - {self.amount}'

    def get_transaction_details(self):
        return f'Type: {self.transaction_type}, Amount: {self.amount}, Date: {self.transaction_date}, Status: {self.status}'



class Referral(models.Model):
    REFERRAL_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    referrer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='referrals_made')
    referred = models.ForeignKey('User', on_delete=models.CASCADE, related_name='referrals_received')
    referral_code = models.CharField(max_length=50, unique=True)
    referral_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=REFERRAL_STATUS_CHOICES, default='Pending')
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reward_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Referral by {self.referrer.email} for {self.referred.email} - Status: {self.status}'

    def grant_reward(self, amount):
        self.reward_amount = amount
        self.reward_date = timezone.now().date()
        self.status = 'Approved'
        self.save()

    def get_referral_details(self):
        return f'Referrer: {self.referrer.email}, Referred: {self.referred.email}, Status: {self.status}, Reward: {self.reward_amount}'




class Penalty(models.Model):
    PENALTY_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Applied', 'Applied'),
        ('Waived', 'Waived'),
    ]
    
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE, related_name='penalties')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='penalties')
    penalty_amount = models.DecimalField(max_digits=10, decimal_places=2)
    penalty_date = models.DateField(default=timezone.now)
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=PENALTY_STATUS_CHOICES, default='Pending')
    notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Penalty of {self.penalty_amount} for Loan ID {self.loan.id} - Status: {self.status}'

    def apply_penalty(self):
        self.status = 'Applied'
        self.save()

    def waive_penalty(self):
        self.status = 'Waived'
        self.save()

    def get_penalty_details(self):
        return f'Loan ID: {self.loan.id}, User: {self.user.email}, Amount: {self.penalty_amount}, Date: {self.penalty_date}, Status: {self.status}, Reason: {self.reason}'


from django.db import models
from django.utils import timezone

class LoanOffer(models.Model):
    LOAN_OFFER_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Accepted', 'Accepted'),
        ('Expired', 'Expired'),
        ('Rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='loan_offers')
    offer_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_length = models.IntegerField()  # Term length in months
    offer_date = models.DateField(default=timezone.now)
    expiration_date = models.DateField()
    status = models.CharField(max_length=20, choices=LOAN_OFFER_STATUS_CHOICES, default='Active')
    conditions = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Offer of {self.offer_amount} for User ID {self.user.id} - Status: {self.status}'

    def is_expired(self):
        return timezone.now().date() > self.expiration_date

    def accept_offer(self):
        if not self.is_expired():
            self.status = 'Accepted'
            self.save()
        else:
            raise ValueError("Cannot accept an expired offer.")

    def reject_offer(self):
        self.status = 'Rejected'
        self.save()

    def get_offer_details(self):
        return f'User ID: {self.user.id}, Amount: {self.offer_amount}, Interest Rate: {self.interest_rate}%, Term: {self.term_length} months, Status: {self.status}, Conditions: {self.conditions}'
