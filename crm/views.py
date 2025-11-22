from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count
from .models import Employee, LoanApplication, Disbursement, ApplicationDocument, LoanProduct
from django.contrib import messages
from .forms import LoanProductForm, LoanApplicationForm, ApplicationDocumentForm, CSVUploadForm
from django.utils import timezone

def dashboard(request):
    today = timezone.now().date()
    
    # Summary Cards
    total_applications_count = LoanApplication.objects.count()
    new_today_count = LoanApplication.objects.filter(created_at__date=today).count()
    converted_count = LoanApplication.objects.filter(status='Converted').count()
    pending_docs_count = LoanApplication.objects.filter(document_status='Pending').count()
    
    # Pipeline Stages
    pipeline_counts = {
        'New': LoanApplication.objects.filter(status='New').count(),
        'Contacted': LoanApplication.objects.filter(status='Contacted').count(),
        'Follow_up': LoanApplication.objects.filter(status='Follow-up').count(),
        'Verified': LoanApplication.objects.filter(status='Verified').count(),
        'Converted': converted_count,
        'Rejected': LoanApplication.objects.filter(status='Rejected').count(),
    }
    
    # Follow-Ups
    follow_ups = LoanApplication.objects.filter(status='Follow-up').order_by('-updated_at')[:5]
    
    # Application Table
    recent_applications = LoanApplication.objects.all().order_by('-created_at')[:10]
    
    # Employee Performance
    top_employees = Employee.objects.annotate(total_disbursed=Sum('disbursements__amount')).order_by('-total_disbursed')[:5]
    
    context = {
        'total_applications_count': total_applications_count,
        'new_today_count': new_today_count,
        'converted_count': converted_count,
        'pending_docs_count': pending_docs_count,
        'pipeline_counts': pipeline_counts,
        'follow_ups': follow_ups,
        'recent_applications': recent_applications,
        'top_employees': top_employees,
    }
    return render(request, 'crm/dashboard.html', context)

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'crm/employee_list.html', {'employees': employees})

def employee_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        Employee.objects.create(name=name, email=email)
        messages.success(request, 'Employee created successfully.')
        return redirect('employee_list')
    return render(request, 'crm/employee_form.html')

def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.name = request.POST.get('name')
        employee.email = request.POST.get('email')
        employee.save()
        messages.success(request, 'Employee updated successfully.')
        return redirect('employee_list')
    return render(request, 'crm/employee_form.html', {'employee': employee})

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    messages.success(request, 'Employee deleted successfully.')
    return redirect('employee_list')


def application_list(request):
    status = request.GET.get('status')
    if status:
        applications = LoanApplication.objects.filter(status=status).order_by('-created_at')
    else:
        applications = LoanApplication.objects.all().order_by('-created_at')
    return render(request, 'crm/application_list.html', {'applications': applications})

def application_create(request):
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()
            if application.status == 'Converted':
                messages.success(request, 'Application created and Disbursement recorded!')
            else:
                messages.success(request, 'Application created successfully.')
            return redirect('application_list')
    else:
        form = LoanApplicationForm()
    return render(request, 'crm/application_form.html', {'form': form})

def application_update(request, pk):
    application = get_object_or_404(LoanApplication, pk=pk)
    
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST, instance=application)
        if form.is_valid():
            old_status = LoanApplication.objects.get(pk=pk).status
            application = form.save(commit=False)
            new_status = application.status
            application.save()
            
            if old_status != 'Converted' and new_status == 'Converted':
                 messages.success(request, 'Application updated to Converted! Disbursement recorded.')
            else:
                 messages.success(request, 'Application updated successfully.')
            return redirect('application_list')
    else:
        form = LoanApplicationForm(instance=application)
        
    return render(request, 'crm/application_form.html', {'form': form, 'application': application})

# --- Documents View ---
def documents(request):
    documents = ApplicationDocument.objects.all().order_by('-uploaded_at')
    pending_docs = LoanApplication.objects.filter(document_status='Pending')
    
    if request.method == 'POST':
        form = ApplicationDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document uploaded successfully.')
            return redirect('documents')
    else:
        form = ApplicationDocumentForm()
        
    return render(request, 'crm/documents.html', {
        'documents': documents,
        'pending_docs': pending_docs,
        'form': form
    })

# --- Settings View ---
def settings(request):
    return render(request, 'crm/settings.html')

# --- Product Views ---

def loan_product_list(request):
    products = LoanProduct.objects.all()
    return render(request, 'crm/loan_product_list.html', {'products': products})

def loan_product_create(request):
    if request.method == 'POST':
        form = LoanProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loan Product added successfully.')
            return redirect('loan_product_list')
    else:
        form = LoanProductForm()
    return render(request, 'crm/loan_product_form.html', {'form': form})

# --- CSV Import ---
import csv
import io

def import_leads(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            count = 0
            for row in reader:
                try:
                    emp_email = row.get('assigned_to_email')
                    employee = Employee.objects.filter(email=emp_email).first()
                    if not employee:
                        employee = Employee.objects.first() # Fallback
                    
                    LoanApplication.objects.create(
                        name=row.get('name', 'Untitled Application'),
                        amount=row.get('amount', 0),
                        assigned_to=employee,
                        status='New',
                        email=row.get('email'),
                        phone=row.get('phone')
                    )
                    count += 1
                except Exception as e:
                    print(f"Error importing row: {e}")
            
            messages.success(request, f'{count} applications imported successfully.')
            return redirect('application_list')
    else:
        form = CSVUploadForm()
    return render(request, 'crm/import_applications.html', {'form': form})

# --- Reports ---
def employee_sales_report(request):
    employees = Employee.objects.annotate(
        total_sales_amount=Sum('disbursements__amount'),
        deals_closed=Count('disbursements')
    ).order_by('-total_sales_amount')
    return render(request, 'crm/employee_report.html', {'employees': employees})
