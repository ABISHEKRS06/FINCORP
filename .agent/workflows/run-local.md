---
description: How to run the FinCore CRM application locally
---

# Running FinCore CRM Locally

Follow these steps to run the FinCore CRM application on your local development server:

## Prerequisites
Ensure you have Python 3.8+ and pip installed on your system.

## Steps

1. **Navigate to the project directory**
   ```
   cd c:\Users\Abishek R.S\.gemini\antigravity\scratch\sales_crm
   ```

2. **Install dependencies** (if not already installed)
   ```
   pip install django
   ```

3. **Apply database migrations**
   // turbo
   ```
   python manage.py migrate
   ```

4. **Create a superuser** (if you haven't already)
   ```
   python manage.py createsuperuser
   ```
   Follow the prompts to set username, email, and password.

5. **Run the development server**
   // turbo
   ```
   python manage.py runserver
   ```

6. **Access the application**
   Open your web browser and navigate to:
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Default URLs
- **Dashboard**: http://127.0.0.1:8000/
- **Applications**: http://127.0.0.1:8000/applications/
- **Types of Loan**: http://127.0.0.1:8000/loan-products/
- **Documents**: http://127.0.0.1:8000/documents/
- **Bankers**: http://127.0.0.1:8000/employees/
- **Reports**: http://127.0.0.1:8000/reports/employees/
- **Settings**: http://127.0.0.1:8000/settings/

## Stopping the Server
Press `Ctrl+C` in the terminal to stop the development server.

## Troubleshooting
- If you see migration errors, run: `python manage.py makemigrations` then `python manage.py migrate`
- If port 8000 is already in use, specify a different port: `python manage.py runserver 8080`
- For static files issues, run: `python manage.py collectstatic`
