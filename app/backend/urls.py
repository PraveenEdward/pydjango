from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    path('category/', views.CategoryListView.as_view(), name='category_list'),

    path('category/add/', views.CategoryCreateView.as_view(), name='category_add'),

    path('category/update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),

    path('category/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),

    path('product/', views.ProductListView.as_view(), name='product_list'),

    path('product/add/', views.ProductCreateView.as_view(), name='product_add'),

    path('product/update/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update'),

    path('product/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),

    path('invoice/', views.InvoiceListView.as_view(), name='invoice_list'),

    path('invoice/add/', views.create_invoice, name='invoice_create'),

    path('invoice/update/<int:pk>/', views.update_invoice, name='invoice_update'),

    path('invoice/delete/<int:pk>/', views.delete_invoice, name='invoice_delete'),

    path('stock-history/', views.StockHistoryListView.as_view(), name='stock_history'),

    path('barcode/<str:barcode>/', views.get_product_by_barcode, name='barcode_product'),

    path('invoice/pdf/<int:pk>/', views.invoice_pdf, name='invoice_pdf'),

    path('settings/', views.SettingsListView.as_view(), name='settings_list'),

    path('settings/add/', views.SettingsCreateView.as_view(), name='settings_add'),

    path('settings/update/<int:pk>/', views.SettingsUpdateView.as_view(), name='settings_update'),

    path('settings/delete/<int:pk>/', views.SettingsDeleteView.as_view(), name='settings_delete'),

    # Sales Report
    path(
        'reports/sales/',
        views.sales_report,
        name='sales_report'
    ),

    # Product Sales Report
    path(
        'reports/product-sales/',
        views.product_sales_report,
        name='product_sales_report'
    ),

    # Stock Report
    path(
        'reports/stock/',
        views.stock_report,
        name='stock_report'
    ),

    # Profit Report
    path(
        'reports/profit/',
        views.profit_report,
        name='profit_report'
    ),

    # Customer Report
    path(
        'reports/customers/',
        views.customer_report,
        name='customer_report'
    ),

    path(
        'reports/revenue/',
        views.revenue_report,
        name='revenue_report'
    ),

]