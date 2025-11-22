import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sales_crm.settings')
django.setup()

from crm.models import Employee, Lead, Sale

def verify():
    print("Verifying CRM Logic...")
    
    # 1. Create Employee
    emp, created = Employee.objects.get_or_create(email="john@example.com", defaults={'name': "John Doe", 'commission_percentage': 10.0})
    if not created:
        print(f"Using existing Employee: {emp}")
    else:
        print(f"Created Employee: {emp}")
    
    # 2. Create Lead
    lead = Lead.objects.create(title="Big Corp Deal", assigned_to=emp, value=1000.00, status="New")
    print(f"Created Lead: {lead}")
    
    # 3. Convert to Won
    lead.status = 'Won'
    lead.save()
    
    # Check if Sale created
    try:
        sale = Sale.objects.get(lead=lead)
        print(f"Sale created: {sale}")
        print(f"Commission Earned: {sale.commission_earned}")
        
        expected_commission = 1000.00 * 0.10
        if float(sale.commission_earned) == expected_commission:
            print("SUCCESS: Commission calculation correct!")
        else:
            print(f"FAILURE: Commission mismatch. Expected {expected_commission}, got {sale.commission_earned}")
            
    except Sale.DoesNotExist:
        print("FAILURE: Sale not created automatically.")

    # 4. Check Dashboard logic (simple count)
    print(f"Total Sales Count: {Sale.objects.count()}")

if __name__ == '__main__':
    verify()
