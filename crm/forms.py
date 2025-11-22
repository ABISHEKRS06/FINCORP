from django import forms
from .models import LoanProduct, LoanApplication, ApplicationDocument

class LoanProductForm(forms.ModelForm):
    class Meta:
        model = LoanProduct
        fields = ['name', 'interest_rate', 'processing_fee', 'min_amount', 'max_amount', 'eligibility_criteria', 'description']

class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = ['name', 'phone', 'email', 'loan_type', 'employment_type', 'amount', 'assigned_to', 'status', 'document_status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class ApplicationDocumentForm(forms.ModelForm):
    class Meta:
        model = ApplicationDocument
        fields = ['application', 'title', 'file', 'status']

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()
