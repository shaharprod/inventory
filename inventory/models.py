from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum, Count, F
import uuid

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    LOCATION_TYPE_CHOICES = [
        ('warehouse', 'מחסן'),
        ('store', 'חנות'),
        ('office', 'משרד'),
        ('factory', 'מפעל'),
        ('other', 'אחר'),
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name="שם מיקום")
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPE_CHOICES, default='warehouse', verbose_name="סוג מיקום")
    description = models.TextField(blank=True, verbose_name="תיאור")
    address = models.TextField(blank=True, verbose_name="כתובת")
    city = models.CharField(max_length=100, blank=True, verbose_name="עיר")
    postal_code = models.CharField(max_length=10, blank=True, verbose_name="מיקוד")
    phone = models.CharField(max_length=20, blank=True, verbose_name="טלפון")
    email = models.EmailField(blank=True, null=True, verbose_name="אימייל")
    manager_name = models.CharField(max_length=100, blank=True, verbose_name="שם מנהל")
    capacity = models.PositiveIntegerField(default=0, verbose_name="קיבולת (יחידות)")
    is_active = models.BooleanField(default=True, verbose_name="פעיל")
    is_main_warehouse = models.BooleanField(default=False, verbose_name="מחסן ראשי")
    is_main_store = models.BooleanField(default=False, verbose_name="חנות ראשית")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "מיקום"
        verbose_name_plural = "מיקומים"

    def __str__(self):
        return f"{self.name} ({self.get_location_type_display()})"

    @property
    def full_address(self):
        """כתובת מלאה"""
        parts = [self.address, self.city, self.postal_code]
        return ', '.join(filter(None, parts))

    @property
    def current_capacity_used(self):
        """קיבולת נוכחית בשימוש"""
        return Product.objects.filter(location=self).aggregate(
            total=Sum('quantity')
        )['total'] or 0

    @property
    def capacity_percentage(self):
        """אחוז קיבולת בשימוש"""
        if self.capacity == 0:
            return 0
        return (self.current_capacity_used / self.capacity) * 100

class Product(models.Model):
    UNIT_CHOICES = [
        ('pcs', 'יחידות'),
        ('kg', 'קילוגרם'),
        ('g', 'גרם'),
        ('l', 'ליטר'),
        ('ml', 'מיליליטר'),
        ('m', 'מטר'),
        ('cm', 'סנטימטר'),
        ('box', 'קופסה'),
        ('pack', 'חבילה'),
    ]

    STATUS_CHOICES = [
        ('active', 'פעיל'),
        ('inactive', 'לא פעיל'),
        ('discontinued', 'הופסק'),
    ]

    # מידע בסיסי
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    # מלאי
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    min_quantity = models.IntegerField(default=5, validators=[MinValueValidator(0)])
    max_quantity = models.IntegerField(default=1000, validators=[MinValueValidator(0)])
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='pcs')

    # מחירים
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    margin_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # ברקוד וזיהוי
    barcode = models.CharField(max_length=50, blank=True, unique=True)
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    product_image = models.ImageField(upload_to='products/', blank=True, null=True)

    # סטטוס ותאריכים
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # תכונות נוספות
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    dimensions = models.CharField(max_length=100, blank=True)  # LxWxH
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['barcode']),
            models.Index(fields=['category']),
            models.Index(fields=['supplier']),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def is_low_stock(self):
        return self.quantity <= self.min_quantity

    @property
    def is_out_of_stock(self):
        return self.quantity <= 0

    @property
    def is_overstocked(self):
        return self.quantity >= self.max_quantity

    @property
    def stock_value(self):
        return self.quantity * self.cost_price

    @property
    def potential_value(self):
        return self.quantity * self.selling_price

    def save(self, *args, **kwargs):
        # חישוב אחוז רווח אוטומטי
        if self.cost_price > 0 and self.selling_price > 0:
            self.margin_percentage = ((self.selling_price - self.cost_price) / self.cost_price) * 100
        super().save(*args, **kwargs)

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('in', 'כניסה'),
        ('out', 'יציאה'),
        ('adjustment', 'תיקון'),
        ('transfer', 'העברה'),
        ('return', 'החזרה'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    previous_quantity = models.IntegerField()
    new_quantity = models.IntegerField()
    reason = models.CharField(max_length=200, blank=True)
    reference = models.CharField(max_length=100, blank=True)  # מספר הזמנה, חשבונית וכו'
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.get_movement_type_display()} ({self.quantity})"

class Alert(models.Model):
    ALERT_TYPES = [
        ('low_stock', 'מלאי נמוך'),
        ('out_of_stock', 'אזל מהמלאי'),
        ('overstock', 'מלאי עודף'),
        ('expiry', 'תאריך תפוגה'),
        ('reorder', 'הזמנה מחדש'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'נמוכה'),
        ('medium', 'בינונית'),
        ('high', 'גבוהה'),
        ('critical', 'קריטית'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.get_alert_type_display()}"

# מודל לקוחות
class Customer(models.Model):
    CUSTOMER_TYPE_CHOICES = [
        ('individual', 'פרטי'),
        ('business', 'עסקי'),
        ('wholesale', 'סיטונאי'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'נמוכה'),
        ('medium', 'בינונית'),
        ('high', 'גבוהה'),
        ('vip', 'VIP'),
    ]

    # פרטים בסיסיים
    name = models.CharField(max_length=200, verbose_name="שם לקוח")
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default='individual', verbose_name="סוג לקוח")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name="עדיפות")

    # פרטי קשר
    email = models.EmailField(blank=True, null=True, verbose_name="אימייל")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="טלפון")
    mobile = models.CharField(max_length=20, blank=True, null=True, verbose_name="נייד")
    website = models.URLField(blank=True, null=True, verbose_name="אתר אינטרנט")

    # כתובות
    address = models.TextField(blank=True, null=True, verbose_name="כתובת")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="עיר")
    postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="מיקוד")
    country = models.CharField(max_length=100, default='ישראל', verbose_name="מדינה")

    # פרטי זיהוי
    tax_id = models.CharField(max_length=20, blank=True, null=True, verbose_name="ח.פ/ת.ז")
    id_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="ת.ז")

    # פרטי CRM
    customer_code = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="קוד לקוח")
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="מגבלת אשראי")
    payment_terms = models.CharField(max_length=100, default='30 ימים', verbose_name="תנאי תשלום")
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="אחוז הנחה")

    # סטטיסטיקות
    total_purchases = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="סה\"כ רכישות")
    last_purchase_date = models.DateTimeField(blank=True, null=True, verbose_name="רכישה אחרונה")
    total_orders = models.PositiveIntegerField(default=0, verbose_name="סה\"כ הזמנות")

    # סטטוס
    is_active = models.BooleanField(default=True, verbose_name="פעיל")
    is_vip = models.BooleanField(default=False, verbose_name="לקוח VIP")
    notes = models.TextField(blank=True, null=True, verbose_name="הערות")

    # מערכת
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="נוצר על ידי")

    class Meta:
        ordering = ['name']
        verbose_name = "לקוח"
        verbose_name_plural = "לקוחות"

    def __str__(self):
        return f"{self.name} ({self.customer_code or 'ללא קוד'})"

    def save(self, *args, **kwargs):
        if not self.customer_code:
            self.customer_code = f"CUST-{Customer.objects.count() + 1:06d}"
        super().save(*args, **kwargs)

    @property
    def full_address(self):
        """כתובת מלאה"""
        parts = [self.address, self.city, self.postal_code, self.country]
        return ', '.join(filter(None, parts))

    @property
    def contact_info(self):
        """פרטי קשר מלאים"""
        contacts = []
        if self.phone:
            contacts.append(f"טל: {self.phone}")
        if self.mobile:
            contacts.append(f"נייד: {self.mobile}")
        if self.email:
            contacts.append(f"אימייל: {self.email}")
        return ' | '.join(contacts)

# מודל מכירות
class Sale(models.Model):
    STATUS_CHOICES = [
        ('draft', 'טיוטה'),
        ('confirmed', 'מאושר'),
        ('completed', 'הושלם'),
        ('cancelled', 'בוטל'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'ממתין לתשלום'),
        ('partial', 'תשלום חלקי'),
        ('paid', 'שולם'),
        ('refunded', 'הוחזר'),
    ]

    invoice_number = models.CharField(max_length=50, unique=True, verbose_name="מספר חשבונית")
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="לקוח")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="סטטוס")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name="סטטוס תשלום")

    # מחירים
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="סכום לפני מע\"מ")
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=17, verbose_name="אחוז מע\"מ")
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="סכום מע\"מ")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="סכום כולל")

    # מידע נוסף
    notes = models.TextField(blank=True, null=True, verbose_name="הערות")
    sale_date = models.DateTimeField(default=timezone.now, verbose_name="תאריך מכירה")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="נוצר על ידי")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "מכירה"
        verbose_name_plural = "מכירות"

    def __str__(self):
        return f"חשבונית #{self.invoice_number}"

    def save(self, *args, **kwargs):
        # חישוב אוטומטי של מע"מ וסכום כולל
        self.tax_amount = self.subtotal * (self.tax_rate / 100)
        self.total_amount = self.subtotal + self.tax_amount
        super().save(*args, **kwargs)

# מודל פריטי חשבונית
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items', verbose_name="מכירה")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="מוצר")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="כמות")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="מחיר יחידה")
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="אחוז הנחה")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="סכום הנחה")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="סכום כולל")

    class Meta:
        verbose_name = "פריט חשבונית"
        verbose_name_plural = "פריטי חשבונית"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        # חישוב אוטומטי של הנחה וסכום כולל
        self.discount_amount = (self.quantity * self.unit_price) * (self.discount_percent / 100)
        self.total_price = (self.quantity * self.unit_price) - self.discount_amount
        super().save(*args, **kwargs)

# מודל ניהול מלאי בין חנות למחסן
class InventoryTransfer(models.Model):
    TRANSFER_TYPE_CHOICES = [
        ('warehouse_to_store', 'מחסן לחנות'),
        ('store_to_warehouse', 'חנות למחסן'),
        ('store_to_store', 'חנות לחנות'),
        ('warehouse_to_warehouse', 'מחסן למחסן'),
    ]

    STATUS_CHOICES = [
        ('pending', 'ממתין'),
        ('in_transit', 'בדרך'),
        ('completed', 'הושלם'),
        ('cancelled', 'בוטל'),
    ]

    transfer_number = models.CharField(max_length=50, unique=True, verbose_name="מספר העברה")
    transfer_type = models.CharField(max_length=30, choices=TRANSFER_TYPE_CHOICES, verbose_name="סוג העברה")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="סטטוס")

    # מיקומים
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='transfers_from', verbose_name="ממיקום")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='transfers_to', verbose_name="למיקום")

    # מידע נוסף
    notes = models.TextField(blank=True, null=True, verbose_name="הערות")
    transfer_date = models.DateTimeField(default=timezone.now, verbose_name="תאריך העברה")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="נוצר על ידי")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "העברת מלאי"
        verbose_name_plural = "העברות מלאי"

    def __str__(self):
        return f"העברה #{self.transfer_number}"

# מודל פריטי העברה
class TransferItem(models.Model):
    transfer = models.ForeignKey(InventoryTransfer, on_delete=models.CASCADE, related_name='items', verbose_name="העברה")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="מוצר")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="כמות")
    notes = models.TextField(blank=True, null=True, verbose_name="הערות")

    class Meta:
        verbose_name = "פריט העברה"
        verbose_name_plural = "פריטי העברה"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

# מודל היסטוריית מכירות ללקוח
class CustomerSaleHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sale_history', verbose_name="לקוח")
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name="מכירה")
    sale_date = models.DateTimeField(verbose_name="תאריך מכירה")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="סכום כולל")
    payment_status = models.CharField(max_length=20, choices=Sale.PAYMENT_STATUS_CHOICES, verbose_name="סטטוס תשלום")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sale_date']
        verbose_name = "היסטוריית מכירות"
        verbose_name_plural = "היסטוריית מכירות"

    def __str__(self):
        return f"{self.customer.name} - {self.sale.invoice_number}"

# מודל הערות ותקשורת עם לקוחות
class CustomerNote(models.Model):
    NOTE_TYPE_CHOICES = [
        ('general', 'כללי'),
        ('call', 'שיחה'),
        ('email', 'אימייל'),
        ('meeting', 'פגישה'),
        ('complaint', 'תלונה'),
        ('compliment', 'מחמאה'),
        ('follow_up', 'מעקב'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_notes', verbose_name="לקוח")
    note_type = models.CharField(max_length=20, choices=NOTE_TYPE_CHOICES, default='general', verbose_name="סוג הערה")
    title = models.CharField(max_length=200, verbose_name="כותרת")
    content = models.TextField(verbose_name="תוכן")
    is_important = models.BooleanField(default=False, verbose_name="חשוב")
    follow_up_date = models.DateTimeField(blank=True, null=True, verbose_name="תאריך מעקב")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="נוצר על ידי")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "הערת לקוח"
        verbose_name_plural = "הערות לקוחות"

    def __str__(self):
        return f"{self.customer.name} - {self.title}"

# מודל התראות לקוחות
class CustomerAlert(models.Model):
    ALERT_TYPE_CHOICES = [
        ('birthday', 'יום הולדת'),
        ('anniversary', 'יום השנה'),
        ('follow_up', 'מעקב נדרש'),
        ('payment_overdue', 'תשלום באיחור'),
        ('credit_limit', 'מגבלת אשראי'),
        ('inactive', 'לקוח לא פעיל'),
        ('high_value', 'רכישה גבוהה'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_alerts', verbose_name="לקוח")
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES, verbose_name="סוג התראה")
    title = models.CharField(max_length=200, verbose_name="כותרת")
    message = models.TextField(verbose_name="הודעה")
    is_read = models.BooleanField(default=False, verbose_name="נקרא")
    is_resolved = models.BooleanField(default=False, verbose_name="נפתר")
    alert_date = models.DateTimeField(default=timezone.now, verbose_name="תאריך התראה")
    resolved_at = models.DateTimeField(blank=True, null=True, verbose_name="תאריך פתרון")
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="נפתר על ידי")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "התראת לקוח"
        verbose_name_plural = "התראות לקוחות"

    def __str__(self):
        return f"{self.customer.name} - {self.title}"

# מודל תבניות חשבוניות
class InvoiceTemplate(models.Model):
    name = models.CharField(max_length=100, verbose_name="שם תבנית")
    is_default = models.BooleanField(default=False, verbose_name="תבנית ברירת מחדל")
    header_text = models.TextField(blank=True, null=True, verbose_name="טקסט כותרת")
    footer_text = models.TextField(blank=True, null=True, verbose_name="טקסט כותרת תחתונה")
    company_name = models.CharField(max_length=200, verbose_name="שם החברה")
    company_address = models.TextField(verbose_name="כתובת החברה")
    company_phone = models.CharField(max_length=20, verbose_name="טלפון החברה")
    company_email = models.EmailField(verbose_name="אימייל החברה")
    company_tax_id = models.CharField(max_length=20, verbose_name="ח.פ החברה")
    logo = models.ImageField(upload_to='invoice_logos/', blank=True, null=True, verbose_name="לוגו")
    is_active = models.BooleanField(default=True, verbose_name="פעיל")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "תבנית חשבונית"
        verbose_name_plural = "תבניות חשבוניות"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_default:
            # ביטול ברירת מחדל מכל התבניות האחרות
            InvoiceTemplate.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

# מודל התראות מיקום
class LocationAlert(models.Model):
    ALERT_TYPE_CHOICES = [
        ('low_stock', 'מלאי נמוך'),
        ('out_of_stock', 'אזל מהמלאי'),
        ('overstock', 'מלאי עודף'),
        ('capacity_full', 'קיבולת מלאה'),
        ('capacity_almost_full', 'קיבולת כמעט מלאה'),
        ('expired_products', 'מוצרים פגי תוקף'),
        ('near_expiry', 'מוצרים קרובים לפג תוקף'),
        ('maintenance_required', 'נדרש תחזוקה'),
        ('security_breach', 'הפרת אבטחה'),
        ('temperature_issue', 'בעיית טמפרטורה'),
        ('other', 'אחר'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'נמוכה'),
        ('medium', 'בינונית'),
        ('high', 'גבוהה'),
        ('critical', 'קריטית'),
    ]

    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location_alerts', verbose_name="מיקום")
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPE_CHOICES, verbose_name="סוג התראה")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name="עדיפות")
    title = models.CharField(max_length=200, verbose_name="כותרת")
    message = models.TextField(verbose_name="הודעה")
    is_read = models.BooleanField(default=False, verbose_name="נקרא")
    is_resolved = models.BooleanField(default=False, verbose_name="נפתר")
    alert_date = models.DateTimeField(default=timezone.now, verbose_name="תאריך התראה")
    resolved_at = models.DateTimeField(blank=True, null=True, verbose_name="תאריך פתרון")
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="נפתר על ידי")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "התראת מיקום"
        verbose_name_plural = "התראות מיקום"

    def __str__(self):
        return f"{self.location.name} - {self.title}"
