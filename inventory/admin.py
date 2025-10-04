from django.contrib import admin
from .models import (
    Product, Category, Supplier, Location, StockMovement, Alert,
    Customer, Sale, SaleItem, InventoryTransfer, TransferItem,
    CustomerSaleHistory, CustomerNote, CustomerAlert, InvoiceTemplate,
    LocationAlert, ProductLocationStock, CompanySettings, InvoiceAuditLog, InvoiceArchive
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'created_at']
    list_filter = ['parent', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'email', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'contact_person', 'email']
    ordering = ['name']

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'location_type', 'city', 'manager_name',
        'capacity', 'current_capacity_used', 'is_active', 'created_at'
    ]
    list_filter = [
        'location_type', 'is_active', 'is_main_warehouse',
        'is_main_store', 'created_at'
    ]
    search_fields = [
        'name', 'description', 'address', 'city',
        'manager_name', 'phone', 'email'
    ]
    readonly_fields = [
        'current_capacity_used', 'capacity_percentage',
        'created_at', 'updated_at'
    ]
    fieldsets = (
        ('פרטים בסיסיים', {
            'fields': ('name', 'location_type', 'description')
        }),
        ('כתובת', {
            'fields': ('address', 'city', 'postal_code')
        }),
        ('פרטי קשר', {
            'fields': ('phone', 'email', 'manager_name')
        }),
        ('קיבולת', {
            'fields': ('capacity', 'current_capacity_used', 'capacity_percentage')
        }),
        ('סטטוס', {
            'fields': ('is_active', 'is_main_warehouse', 'is_main_store')
        }),
        ('מערכת', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'sku', 'category', 'supplier', 'quantity',
        'min_quantity', 'cost_price', 'selling_price', 'status', 'created_at'
    ]
    list_filter = [
        'category', 'supplier', 'location', 'status', 'unit',
        'created_at', 'updated_at'
    ]
    search_fields = ['name', 'sku', 'barcode', 'description']
    readonly_fields = ['created_at', 'updated_at', 'margin_percentage']
    fieldsets = (
        ('מידע בסיסי', {
            'fields': ('name', 'sku', 'description', 'category', 'supplier', 'location')
        }),
        ('מלאי', {
            'fields': ('quantity', 'min_quantity', 'max_quantity', 'unit')
        }),
        ('מחירים', {
            'fields': ('cost_price', 'selling_price', 'margin_percentage')
        }),
        ('זיהוי', {
            'fields': ('barcode', 'barcode_image', 'product_image')
        }),
        ('פרטים נוספים', {
            'fields': ('weight', 'dimensions', 'notes', 'status')
        }),
        ('מערכת', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['name']

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = [
        'product', 'movement_type', 'quantity', 'previous_quantity',
        'new_quantity', 'user', 'created_at'
    ]
    list_filter = ['movement_type', 'created_at', 'user']
    search_fields = ['product__name', 'reason', 'reference']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = [
        'product', 'alert_type', 'priority', 'is_read',
        'is_resolved', 'created_at'
    ]
    list_filter = ['alert_type', 'priority', 'is_read', 'is_resolved', 'created_at']
    search_fields = ['product__name', 'message']
    readonly_fields = ['created_at', 'resolved_at']
    ordering = ['-created_at']

# ניהול לקוחות
class CustomerNoteInline(admin.TabularInline):
    model = CustomerNote
    extra = 1
    fields = ['note_type', 'title', 'content', 'is_important', 'follow_up_date']

class CustomerAlertInline(admin.TabularInline):
    model = CustomerAlert
    extra = 0
    fields = ['alert_type', 'title', 'is_read', 'is_resolved']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'customer_code', 'customer_type', 'priority',
        'email', 'phone', 'total_purchases', 'is_active', 'created_at'
    ]
    list_filter = [
        'customer_type', 'priority', 'is_active', 'is_vip',
        'created_at', 'last_purchase_date'
    ]
    search_fields = [
        'name', 'customer_code', 'email', 'phone', 'mobile',
        'tax_id', 'id_number', 'city'
    ]
    readonly_fields = [
        'customer_code', 'total_purchases', 'total_orders',
        'last_purchase_date', 'created_at', 'updated_at'
    ]
    inlines = [CustomerNoteInline, CustomerAlertInline]
    fieldsets = (
        ('פרטים בסיסיים', {
            'fields': ('name', 'customer_code', 'customer_type', 'priority')
        }),
        ('פרטי קשר', {
            'fields': ('email', 'phone', 'mobile', 'website')
        }),
        ('כתובת', {
            'fields': ('address', 'city', 'postal_code', 'country')
        }),
        ('פרטי זיהוי', {
            'fields': ('tax_id', 'id_number')
        }),
        ('פרטי CRM', {
            'fields': ('credit_limit', 'payment_terms', 'discount_percent')
        }),
        ('סטטיסטיקות', {
            'fields': ('total_purchases', 'total_orders', 'last_purchase_date'),
            'classes': ('collapse',)
        }),
        ('סטטוס', {
            'fields': ('is_active', 'is_vip', 'notes')
        }),
        ('מערכת', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['name']

# ניהול מכירות
class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    fields = ['product', 'quantity', 'unit_price', 'discount_percent', 'total_price']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'customer', 'status', 'payment_status', 'total_amount', 'sale_date']
    list_filter = ['status', 'payment_status', 'sale_date', 'created_at']
    search_fields = ['invoice_number', 'customer__name']
    inlines = [SaleItemInline]
    readonly_fields = ['created_at', 'updated_at', 'tax_amount', 'total_amount']
    fieldsets = (
        ('מידע בסיסי', {
            'fields': ('invoice_number', 'customer', 'status', 'payment_status')
        }),
        ('מחירים', {
            'fields': ('subtotal', 'tax_rate', 'tax_amount', 'total_amount')
        }),
        ('מידע נוסף', {
            'fields': ('notes', 'sale_date', 'created_by')
        }),
        ('מערכת', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['-created_at']

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ['sale', 'product', 'quantity', 'unit_price', 'total_price']
    list_filter = ['sale__status', 'sale__sale_date']
    search_fields = ['sale__invoice_number', 'product__name']

# ניהול העברות מלאי
class TransferItemInline(admin.TabularInline):
    model = TransferItem
    extra = 1
    fields = ['product', 'quantity', 'notes']

@admin.register(InventoryTransfer)
class InventoryTransferAdmin(admin.ModelAdmin):
    list_display = ['transfer_number', 'transfer_type', 'from_location', 'to_location', 'status', 'transfer_date']
    list_filter = ['transfer_type', 'status', 'transfer_date', 'created_at']
    search_fields = ['transfer_number', 'from_location__name', 'to_location__name']
    inlines = [TransferItemInline]
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('מידע בסיסי', {
            'fields': ('transfer_number', 'transfer_type', 'status')
        }),
        ('מיקומים', {
            'fields': ('from_location', 'to_location')
        }),
        ('מידע נוסף', {
            'fields': ('notes', 'transfer_date', 'created_by')
        }),
        ('מערכת', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['-created_at']

@admin.register(TransferItem)
class TransferItemAdmin(admin.ModelAdmin):
    list_display = ['transfer', 'product', 'quantity']
    list_filter = ['transfer__status', 'transfer__transfer_type']
    search_fields = ['transfer__transfer_number', 'product__name']

# ניהול CRM
@admin.register(CustomerSaleHistory)
class CustomerSaleHistoryAdmin(admin.ModelAdmin):
    list_display = ['customer', 'sale', 'sale_date', 'total_amount', 'payment_status']
    list_filter = ['payment_status', 'sale_date', 'created_at']
    search_fields = ['customer__name', 'sale__invoice_number']
    readonly_fields = ['created_at']
    ordering = ['-sale_date']

@admin.register(CustomerNote)
class CustomerNoteAdmin(admin.ModelAdmin):
    list_display = ['customer', 'note_type', 'title', 'is_important', 'created_by', 'created_at']
    list_filter = ['note_type', 'is_important', 'created_at']
    search_fields = ['customer__name', 'title', 'content']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

@admin.register(CustomerAlert)
class CustomerAlertAdmin(admin.ModelAdmin):
    list_display = ['customer', 'alert_type', 'title', 'is_read', 'is_resolved', 'alert_date']
    list_filter = ['alert_type', 'is_read', 'is_resolved', 'alert_date']
    search_fields = ['customer__name', 'title', 'message']
    readonly_fields = ['created_at', 'resolved_at']
    ordering = ['-created_at']

@admin.register(InvoiceTemplate)
class InvoiceTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_default', 'company_name', 'is_active', 'created_at']
    list_filter = ['is_default', 'is_active', 'created_at']
    search_fields = ['name', 'company_name']
    readonly_fields = ['created_at']
    ordering = ['name']

# ניהול התראות מיקום
@admin.register(LocationAlert)
class LocationAlertAdmin(admin.ModelAdmin):
    list_display = [
        'location', 'alert_type', 'priority', 'title',
        'is_read', 'is_resolved', 'alert_date'
    ]
    list_filter = [
        'alert_type', 'priority', 'is_read', 'is_resolved',
        'location__location_type', 'alert_date'
    ]
    search_fields = [
        'location__name', 'title', 'message'
    ]
    readonly_fields = ['created_at', 'resolved_at']
    ordering = ['-created_at']

# ניהול מלאי לפי מיקום
@admin.register(ProductLocationStock)
class ProductLocationStockAdmin(admin.ModelAdmin):
    list_display = [
        'product', 'location', 'quantity', 'min_quantity',
        'is_low_stock', 'is_out_of_stock', 'last_sold', 'updated_at'
    ]
    list_filter = [
        'location__location_type', 'location__name',
        'last_sold', 'last_restocked'
    ]
    search_fields = [
        'product__name', 'product__sku', 'location__name'
    ]
    readonly_fields = ['updated_at', 'created_at']
    ordering = ['product__name', 'location__name']

    def is_low_stock(self, obj):
        return obj.is_low_stock
    is_low_stock.boolean = True
    is_low_stock.short_description = 'מלאי נמוך'

    def is_out_of_stock(self, obj):
        return obj.is_out_of_stock
    is_out_of_stock.boolean = True
    is_out_of_stock.short_description = 'אזל מלאי'


# ============ ניהול דרישות חוקיות ============

@admin.register(CompanySettings)
class CompanySettingsAdmin(admin.ModelAdmin):
    list_display = [
        'company_name', 'business_number', 'phone', 'email',
        'default_tax_rate', 'is_active', 'updated_at'
    ]
    fieldsets = (
        ('פרטי החברה', {
            'fields': ('company_name', 'business_number', 'tax_id')
        }),
        ('כתובת ופרטי קשר', {
            'fields': ('address', 'city', 'postal_code', 'phone', 'email', 'website')
        }),
        ('הגדרות חשבוניות', {
            'fields': (
                'invoice_prefix', 'current_invoice_number',
                'tax_authority_allocation_number', 'default_tax_rate'
            )
        }),
        ('אבטחה וחתימה', {
            'fields': ('digital_signature_key', 'signature_certificate'),
            'classes': ('collapse',)
        }),
        ('ארכוב', {
            'fields': ('archive_years',)
        }),
        ('מערכת', {
            'fields': ('is_active', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

    def has_add_permission(self, request):
        # אפשר רק רשומה אחת
        return not CompanySettings.objects.exists()


@admin.register(InvoiceAuditLog)
class InvoiceAuditLogAdmin(admin.ModelAdmin):
    list_display = [
        'sale', 'action', 'performed_by', 'performed_at',
        'ip_address', 'formatted_notes'
    ]
    list_filter = ['action', 'performed_at', 'performed_by']
    search_fields = [
        'sale__invoice_number', 'performed_by__username',
        'ip_address', 'notes'
    ]
    readonly_fields = [
        'sale', 'action', 'performed_by', 'performed_at',
        'ip_address', 'user_agent', 'old_values', 'new_values', 'notes'
    ]
    ordering = ['-performed_at']
    date_hierarchy = 'performed_at'

    def has_add_permission(self, request):
        # לא ניתן להוסיף ידנית - רק דרך המערכת
        return False

    def has_change_permission(self, request, obj=None):
        # לא ניתן לערוך - לוג קבוע
        return False

    def has_delete_permission(self, request, obj=None):
        # לא ניתן למחוק - לוג קבוע
        return False

    def formatted_notes(self, obj):
        return obj.notes[:50] + '...' if len(obj.notes) > 50 else obj.notes
    formatted_notes.short_description = 'הערות'


@admin.register(InvoiceArchive)
class InvoiceArchiveAdmin(admin.ModelAdmin):
    list_display = [
        'sale', 'archived_at', 'delete_after',
        'is_encrypted', 'signature_valid'
    ]
    list_filter = ['is_encrypted', 'archived_at', 'delete_after']
    search_fields = ['sale__invoice_number']
    readonly_fields = [
        'sale', 'invoice_data', 'invoice_html', 'digital_signature',
        'signature_timestamp', 'qr_code_data', 'archived_at', 'delete_after'
    ]
    ordering = ['-archived_at']
    date_hierarchy = 'archived_at'

    def has_add_permission(self, request):
        # לא ניתן להוסיף ידנית - רק דרך המערכת
        return False

    def has_change_permission(self, request, obj=None):
        # לא ניתן לערוך - ארכיון קבוע
        return False

    def has_delete_permission(self, request, obj=None):
        # לא ניתן למחוק - ארכיון חוקי
        return False

    def signature_valid(self, obj):
        return obj.verify_signature()
    signature_valid.boolean = True
    signature_valid.short_description = 'חתימה תקינה'
