from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class LoanApplication(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Follow-up', 'Follow-up'),
        ('Verified', 'Verified'),
        ('Converted', 'Converted'),
        ('Rejected', 'Rejected'),
    ]

    LOAN_TYPE_CHOICES = [
        ('Personal', 'Personal Loan'),
        ('Home', 'Home Loan'),
        ('Car', 'Car Loan'),
        ('Education', 'Education Loan'),
        ('Business', 'Business Loan'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('Salaried', 'Salaried'),
        ('Self-employed', 'Self-employed'),
    ]

    DOCUMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Submitted', 'Submitted'),
        ('Verified', 'Verified'),
        ('Rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=200, verbose_name="Applicant Name")
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    loan_type = models.CharField(max_length=50, choices=LOAN_TYPE_CHOICES, default='Personal')
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPE_CHOICES, default='Salaried')
    
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    document_status = models.CharField(max_length=20, choices=DOCUMENT_STATUS_CHOICES, default='Pending')
    
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Loan Amount Required")
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.loan_type}"

class ApplicationDocument(models.Model):
    application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=100, help_text="e.g., ID Proof, Income Proof")
    file = models.FileField(upload_to='application_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=LoanApplication.DOCUMENT_STATUS_CHOICES, default='Submitted')

    def __str__(self):
        return f"{self.title} for {self.application.name}"

class LoanProduct(models.Model):
    name = models.CharField(max_length=200)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Interest Rate %", default=10.0)
    processing_fee = models.DecimalField(max_digits=5, decimal_places=2, help_text="Processing Fee %", default=1.0)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2, default=10000)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2, default=1000000)
    eligibility_criteria = models.TextField(blank=True, help_text="Eligibility rules")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

from decimal import Decimal

class Disbursement(models.Model):
    application = models.OneToOneField(LoanApplication, on_delete=models.CASCADE, related_name='disbursement')
    banker = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='disbursements')
    product = models.ForeignKey(LoanProduct, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loan Disbursed for {self.application.name}"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=LoanApplication)
def create_disbursement_on_conversion(sender, instance, created, **kwargs):
    if instance.status == 'Converted':
        # Check if disbursement already exists
        if not hasattr(instance, 'disbursement'):
            Disbursement.objects.create(
                application=instance,
                banker=instance.assigned_to,
                amount=instance.amount
            )
