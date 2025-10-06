from django import forms
from .models import (
    Product, Category, Supplier, Location, StockMovement, Alert,
    Customer, Sale, SaleItem, InventoryTransfer, TransferItem,
    CustomerSaleHistory, CustomerNote, CustomerAlert, InvoiceTemplate,
    SystemSettings
)
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'parent']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email', 'phone', 'address', 'is_active']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'description', 'address', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'category', 'supplier', 'location',
            'quantity', 'min_quantity', 'max_quantity', 'unit',
            'cost_price', 'selling_price', 'barcode', 'status',
            'weight', 'dimensions', 'notes', 'barcode_image', 'product_image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'dimensions': forms.TextInput(attrs={'placeholder': 'LxWxH (לדוגמה: 10x5x3)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # הוספת CSS classes
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['movement_type', 'quantity', 'reason', 'reference']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        if self.product:
            self.fields['quantity'].widget.attrs.update({
                'max': self.product.quantity if self.instance.movement_type == 'out' else 9999
            })

class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['alert_type', 'priority', 'message', 'is_resolved']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }

class ProductSearchForm(forms.Form):
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'חיפוש לפי שם, SKU או ברקוד...',
            'class': 'form-control'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="כל הקטגוריות",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.filter(is_active=True),
        required=False,
        empty_label="כל הספקים",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=[('', 'כל הסטטוסים')] + Product.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    low_stock = forms.BooleanField(
        required=False,
        label='מלאי נמוך בלבד',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    out_of_stock = forms.BooleanField(
        required=False,
        label='אזל מהמלאי',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class BulkUpdateForm(forms.Form):
    ACTION_CHOICES = [
        ('add', 'הוסף כמות'),
        ('subtract', 'הפחת כמות'),
        ('set', 'קבע כמות'),
        ('update_price', 'עדכן מחיר'),
        ('change_status', 'שנה סטטוס'),
        ('change_category', 'שנה קטגוריה'),
    ]

    action = forms.ChoiceField(choices=ACTION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    value = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    new_status = forms.ChoiceField(
        choices=[('', 'בחר סטטוס')] + Product.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    new_category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="בחר קטגוריה",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    reason = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'סיבת העדכון'})
    )

# Forms למכירות
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name', 'customer_type', 'priority', 'email', 'phone', 'mobile', 'website',
            'address', 'city', 'postal_code', 'country', 'tax_id', 'id_number',
            'credit_limit', 'payment_terms', 'discount_percent', 'is_active', 'is_vip', 'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_type': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'tax_id': forms.TextInput(attrs={'class': 'form-control'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control'}),
            'credit_limit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_terms': forms.TextInput(attrs={'class': 'form-control'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_vip': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'location', 'status', 'payment_status', 'payment_method', 'subtotal', 'tax_rate', 'notes', 'sale_date']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tax_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sale_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # הצג חנויות ומחסנים פעילים
        from .models import Location
        self.fields['location'].queryset = Location.objects.filter(
            is_active=True
        ).order_by('location_type', 'name')
        self.fields['location'].label = "מיקום מכירה"
        self.fields['location'].help_text = "בחר חנות או מחסן למכירה"

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'unit_price', 'discount_percent']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100', 'value': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # שינוי התווית של "בחר מוצר" ללא קווים
        self.fields['product'].empty_label = "בחר מוצר"
        self.fields['product'].required = False

# Forms להעברות מלאי
class InventoryTransferForm(forms.ModelForm):
    class Meta:
        model = InventoryTransfer
        fields = ['transfer_type', 'from_location', 'to_location', 'status', 'notes', 'transfer_date']
        widgets = {
            'transfer_type': forms.Select(attrs={'class': 'form-control'}),
            'from_location': forms.Select(attrs={'class': 'form-control'}),
            'to_location': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'transfer_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class TransferItemForm(forms.ModelForm):
    class Meta:
        model = TransferItem
        fields = ['product', 'quantity', 'notes']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

# Formset לפריטי מכירה
SaleItemFormSet = forms.inlineformset_factory(
    Sale, SaleItem,
    form=SaleItemForm,
    extra=1,           # רק שורה אחת ריקה
    can_delete=True,
    min_num=0,         # שונה מ-1 ל-0 - מינימום 0 שורות
    validate_min=False # ללא אימות מינימום
)

# Formset לפריטי העברה
TransferItemFormSet = forms.inlineformset_factory(
    InventoryTransfer, TransferItem,
    form=TransferItemForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)

# Forms ל-CRM
class CustomerNoteForm(forms.ModelForm):
    class Meta:
        model = CustomerNote
        fields = ['note_type', 'title', 'content', 'is_important', 'follow_up_date']
        widgets = {
            'note_type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'follow_up_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class CustomerAlertForm(forms.ModelForm):
    class Meta:
        model = CustomerAlert
        fields = ['alert_type', 'title', 'message', 'alert_date']
        widgets = {
            'alert_type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'alert_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class InvoiceTemplateForm(forms.ModelForm):
    class Meta:
        model = InvoiceTemplate
        fields = [
            'name', 'is_default', 'header_text', 'footer_text',
            'company_name', 'company_address', 'company_phone',
            'company_email', 'company_tax_id', 'logo', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'header_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'footer_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'company_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'company_tax_id': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Forms לחיפוש וסינון
class CustomerSearchForm(forms.Form):
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'חיפוש לפי שם, קוד, טלפון או אימייל...'
        })
    )
    customer_type = forms.ChoiceField(
        choices=[('', 'כל הסוגים')] + Customer.CUSTOMER_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    priority = forms.ChoiceField(
        choices=[('', 'כל העדיפויות')] + Customer.PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_active = forms.ChoiceField(
        choices=[('', 'כל הסטטוסים'), ('true', 'פעיל'), ('false', 'לא פעיל')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_vip = forms.ChoiceField(
        choices=[('', 'כל הלקוחות'), ('true', 'VIP בלבד')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

# Forms למיקומים
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = [
            'name', 'location_type', 'description', 'address', 'city', 'postal_code',
            'phone', 'email', 'manager_name', 'capacity', 'is_active',
            'is_main_warehouse', 'is_main_store'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'manager_name': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_main_warehouse': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_main_store': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SystemSettingsForm(forms.ModelForm):
    """טופס להגדרות מערכת"""
    class Meta:
        model = SystemSettings
        fields = [
            'email_enabled', 'email_host', 'email_port', 'email_use_tls', 'email_use_ssl',
            'email_host_user', 'email_host_password', 'default_from_email',
            'daily_report_enabled', 'daily_report_email', 'daily_report_time',
            'alert_email_enabled', 'alert_email_recipients',
            'low_stock_threshold', 'critical_stock_threshold',
            'enable_low_stock_alerts', 'enable_expiry_alerts', 'expiry_alert_days'
        ]
        widgets = {
            'email_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_host': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'smtp.gmail.com'}),
            'email_port': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '587'}),
            'email_use_tls': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_use_ssl': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_host_user': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your-email@gmail.com'}),
            'email_host_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'App Password'}),
            'default_from_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your-email@gmail.com'}),
            'daily_report_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'daily_report_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'reports@example.com'}),
            'daily_report_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'alert_email_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'alert_email_recipients': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'email1@example.com, email2@example.com'}),
            'low_stock_threshold': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': '10'}),
            'critical_stock_threshold': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': '5'}),
            'enable_low_stock_alerts': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enable_expiry_alerts': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'expiry_alert_days': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': '30'}),
        }
