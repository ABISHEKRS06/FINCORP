from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/edit/', views.employee_update, name='employee_update'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    path('applications/', views.application_list, name='application_list'),
    path('applications/add/', views.application_create, name='application_create'),
    path('applications/import/', views.import_leads, name='import_applications'), # Keeping import_leads view name but changing url name
    path('applications/<int:pk>/edit/', views.application_update, name='application_update'),
    path('loan-products/', views.loan_product_list, name='loan_product_list'),
    path('loan-products/add/', views.loan_product_create, name='loan_product_create'),
    path('documents/', views.documents, name='documents'),
    path('settings/', views.settings, name='settings'),
    path('reports/employees/', views.employee_sales_report, name='employee_report'),
    path('setup-admin/', views.setup_admin, name='setup_admin'),
]
