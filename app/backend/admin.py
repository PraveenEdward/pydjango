from django.contrib import admin
from .models import (
    Settings,
    Category,
    Product,
    Invoice,
    InvoiceItem,
    StockHistory
)


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = (
        'shop_name',
        'mobile',
        'invoice_prefix',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'category_name',
        'created_at'
    )
    search_fields = ('category_name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product_name',
        'category',
        'barcode',
        'purchase_price',
        'selling_price',
        'stock',
        'minimum_stock',
    )

    search_fields = (
        'product_name',
        'barcode'
    )

    list_filter = (
        'category',
    )


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_no',
        'customer_name',
        'payment_method',
        'total_qty',
        'grand_total',
        'created_at',
    )

    readonly_fields = (
        'invoice_no',
        'total_qty',
        'total_amount',
        'grand_total',
    )

    inlines = [InvoiceItemInline]


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = (
        'invoice',
        'product',
        'quantity',
        'price',
        'subtotal',
    )


@admin.register(StockHistory)
class StockHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'action',
        'previous_stock',
        'quantity',
        'current_stock',
        'created_at'
    )

    readonly_fields = (
        'product',
        'action',
        'previous_stock',
        'quantity',
        'current_stock',
        'created_at'
    )