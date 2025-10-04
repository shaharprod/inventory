from django.urls import path
from . import views

urlpatterns = [
    # דשבורד
    path('', views.dashboard, name='dashboard'),

    # מוצרים
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('products/<int:pk>/movement/', views.stock_movement, name='stock_movement'),
    path('products/<int:pk>/distribute/', views.distribute_stock, name='distribute_stock'),

    # קטגוריות
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:pk>/delete/', views.delete_category, name='delete_category'),

    # ספקים
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.add_supplier, name='add_supplier'),
    path('suppliers/<int:pk>/edit/', views.edit_supplier, name='edit_supplier'),
    path('suppliers/<int:pk>/delete/', views.delete_supplier, name='delete_supplier'),

    # התראות ודוחות
    path('alerts/', views.alerts, name='alerts'),
    path('reports/', views.reports, name='reports'),

    # עדכון מרובה
    path('bulk-update/', views.bulk_update, name='bulk_update'),

    # API
    path('generate-barcode/', views.generate_barcode, name='generate_barcode'),

    # ייצוא דוחות
    path('export/products-csv/', views.export_products_csv, name='export_products_csv'),
    path('export/low-stock-csv/', views.export_low_stock_csv, name='export_low_stock_csv'),
    path('export/movements-csv/', views.export_movements_csv, name='export_movements_csv'),
    path('export/full-report-csv/', views.export_full_report_csv, name='export_full_report_csv'),
    path('export/reports-json/', views.export_reports_json, name='export_reports_json'),

    # CRM
    path('crm/', views.crm_dashboard, name='crm_dashboard'),
    path('crm/customers/', views.customer_list, name='customer_list'),
    path('crm/customers/add/', views.add_customer, name='add_customer'),
    path('crm/customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('crm/customers/<int:pk>/edit/', views.edit_customer, name='edit_customer'),
    path('crm/customers/<int:pk>/delete/', views.delete_customer, name='delete_customer'),
    path('crm/customers/<int:customer_pk>/note/', views.add_customer_note, name='add_customer_note'),
    path('crm/customers/<int:customer_pk>/alert/', views.add_customer_alert, name='add_customer_alert'),
    path('crm/reports/', views.customer_reports, name='customer_reports'),

    # מכירות
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/add/', views.add_sale, name='add_sale'),
    path('sales/<int:pk>/', views.sale_detail, name='sale_detail'),
    path('sales/<int:pk>/edit/', views.edit_sale, name='edit_sale'),
    path('sales/<int:pk>/delete/', views.delete_sale, name='delete_sale'),
    path('sales/<int:sale_pk>/invoice/', views.generate_invoice, name='generate_invoice'),

    # API
    path('api/products/barcode/', views.search_product_by_barcode, name='api_product_barcode'),

    # תבניות חשבוניות
    path('invoice-templates/', views.invoice_templates, name='invoice_templates'),
    path('invoice-templates/add/', views.add_invoice_template, name='add_invoice_template'),

    # העברות מלאי
    path('transfers/', views.transfer_list, name='transfer_list'),
    path('transfers/add/', views.add_transfer, name='add_transfer'),
    path('transfers/<int:pk>/', views.transfer_detail, name='transfer_detail'),
    path('transfers/<int:pk>/complete/', views.complete_transfer, name='complete_transfer'),

    # מיקומים
    path('locations/', views.location_list, name='location_list'),
    path('locations/add/', views.add_location, name='add_location'),
    path('locations/<int:pk>/', views.location_detail, name='location_detail'),
    path('locations/<int:pk>/edit/', views.edit_location, name='edit_location'),
    path('locations/<int:pk>/delete/', views.delete_location, name='delete_location'),
    
    # גיבוי ושחזור
    path('backup/create/', views.backup_database, name='backup_database'),
    path('backup/list/', views.list_backups, name='list_backups'),
    path('backup/restore/', views.restore_database, name='restore_database'),
    path('backup/download/<str:filename>/', views.download_backup, name='download_backup'),
    path('backup/delete/<str:filename>/', views.delete_backup, name='delete_backup'),
]
