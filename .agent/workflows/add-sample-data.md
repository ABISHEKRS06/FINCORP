---
description: How to add sample data to the FinCore CRM
---

# Adding Sample Data to FinCore CRM

This workflow helps you populate the database with sample data for testing and demonstration purposes.

## Steps

1. **Navigate to the project directory**
   ```
   cd c:\Users\Abishek R.S\.gemini\antigravity\scratch\sales_crm
   ```

2. **Open Django shell**
   ```
   python manage.py shell
   ```

3. **Create sample employees/bankers**
   ```python
   from crm.models import Employee
   
   Employee.objects.create(name="John Smith", email="john@fincore.com")
   Employee.objects.create(name="Sarah Johnson", email="sarah@fincore.com")
   Employee.objects.create(name="Michael Brown", email="michael@fincore.com")
   ```

4. **Create sample loan types**
   ```python
   from crm.models import LoanProduct
   
   LoanProduct.objects.create(
       name="Personal Loan",
       interest_rate=10.5,
       processing_fee=1.5,
       min_amount=10000,
       max_amount=500000,
       eligibility_criteria="Minimum salary: $30,000/year",
       description="Quick personal loans for your immediate needs"
   )
   
   LoanProduct.objects.create(
       name="Home Loan",
       interest_rate=8.5,
       processing_fee=1.0,
       min_amount=100000,
       max_amount=5000000,
       eligibility_criteria="Minimum salary: $50,000/year, Good credit score",
       description="Affordable home loans with flexible tenure"
   )
   
   LoanProduct.objects.create(
       name="Car Loan",
       interest_rate=9.0,
       processing_fee=1.2,
       min_amount=50000,
       max_amount=1000000,
       eligibility_criteria="Minimum salary: $35,000/year",
       description="Drive your dream car with our competitive rates"
   )
   ```

5. **Create sample loan applications**
   ```python
   from crm.models import LoanApplication, Employee
   
   banker = Employee.objects.first()
   
   LoanApplication.objects.create(
       name="Robert Wilson",
       phone="+1-555-0101",
       email="robert@example.com",
       loan_type="Personal",
       employment_type="Salaried",
       amount=50000,
       status="New",
       assigned_to=banker,
       notes="Looking for quick approval"
   )
   
   LoanApplication.objects.create(
       name="Emily Davis",
       phone="+1-555-0102",
       email="emily@example.com",
       loan_type="Home",
       employment_type="Salaried",
       amount=250000,
       status="Contacted",
       assigned_to=banker,
       notes="First-time home buyer"
   )
   
   LoanApplication.objects.create(
       name="James Martinez",
       phone="+1-555-0103",
       email="james@example.com",
       loan_type="Car",
       employment_type="Self-employed",
       amount=75000,
       status="Converted",
       assigned_to=banker,
       notes="Approved and disbursed"
   )
   ```

6. **Exit the shell**
   ```python
   exit()
   ```

7. **Verify the data**
   Run the development server and check the dashboard to see the sample data.

## Alternative: Using Django Admin

You can also add data through the Django admin interface:
1. Go to http://127.0.0.1:8000/admin/
2. Login with your superuser credentials
3. Add Employees, Loan Products, and Applications through the admin forms
