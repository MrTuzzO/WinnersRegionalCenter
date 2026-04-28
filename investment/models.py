from django.db import models
from django.conf import settings
from project.models import Project

INVESTMENNT_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
]

INVESTMENT_STRATEGY_CHOICES = [
    ("immigration", "Immigration"),
    ("profit", "Profit"),
    ("both", "Both"),
]

class Investment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='investments')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='investments')

    # Personal Info
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    nationality = models.CharField(max_length=50)
    current_country_of_residence = models.CharField(max_length=50)

    # Investment Details
    source_of_funds = models.CharField(max_length=255)
    investment_amount = models.DecimalField(max_digits=15, decimal_places=2)
    investment_strategy = models.CharField(max_length=20, choices=INVESTMENT_STRATEGY_CHOICES)
    status = models.CharField(max_length=20, choices=INVESTMENNT_STATUS_CHOICES, default="pending")

    # documents
    passport_copy = models.FileField(upload_to='investments/passport_copies/')
    proof_of_address = models.FileField(upload_to='investments/proof_of_address/')
    proof_of_funds = models.FileField(upload_to='investments/proof_of_funds/')
    bank_statements = models.FileField(upload_to='investments/bank_statements/')
    upload_agreement = models.FileField(upload_to='investments/agreements/')
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} invested ${self.amount} in {self.project.name}"