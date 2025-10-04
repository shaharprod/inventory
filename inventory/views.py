from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count, F, Case, When
from django.db import models
from django.core.paginator import Paginator
from django.utils import timezone
from django.db import transaction
from .models import (
    Product, Category, Supplier, Location, StockMovement, Alert,
    Customer, Sale, SaleItem, InventoryTransfer, TransferItem,
    CustomerSaleHistory, CustomerNote, CustomerAlert, InvoiceTemplate,
    LocationAlert, ProductLocationStock
)
from .forms import (
    ProductForm, CategoryForm, SupplierForm, LocationForm,
    StockMovementForm, AlertForm, ProductSearchForm, BulkUpdateForm,
    CustomerForm, SaleForm, SaleItemForm, InventoryTransferForm, TransferItemForm,
    SaleItemFormSet, TransferItemFormSet, CustomerNoteForm, CustomerAlertForm,
    InvoiceTemplateForm, CustomerSearchForm
)
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
import csv
import json
from datetime import timedelta
import json
from datetime import datetime, timedelta

def dashboard(request):
    """דשבורד ראשי עם סטטיסטיקות"""
    # סטטיסטיקות כלליות (מכל המיקומים)
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(quantity__lte=F('min_quantity')).count()
    out_of_stock_products = Product.objects.filter(quantity=0).count()
    total_stock_value = Product.objects.aggregate(
        total=Sum(F('quantity') * F('cost_price'))
    )['total'] or 0

    # סטטיסטיקות מחסן (מתוך ProductLocationStock)
    warehouse_locations = Location.objects.filter(location_type='warehouse', is_active=True)
    warehouse_stock = ProductLocationStock.objects.filter(location__in=warehouse_locations)
    warehouse_total = warehouse_stock.values('product').distinct().count()
    warehouse_quantity = warehouse_stock.aggregate(total=Sum('quantity'))['total'] or 0
    warehouse_low_stock = warehouse_stock.filter(quantity__lte=F('min_quantity')).count()
    warehouse_out_of_stock = warehouse_stock.filter(quantity=0).count()
    warehouse_value = warehouse_stock.aggregate(
        total=Sum(F('quantity') * F('product__cost_price'))
    )['total'] or 0

    # סטטיסטיקות חנות (מתוך ProductLocationStock)
    store_locations = Location.objects.filter(location_type='store', is_active=True)
    store_stock = ProductLocationStock.objects.filter(location__in=store_locations)
    store_total = store_stock.values('product').distinct().count()
    store_quantity = store_stock.aggregate(total=Sum('quantity'))['total'] or 0
    store_low_stock = store_stock.filter(quantity__lte=F('min_quantity')).count()
    store_out_of_stock = store_stock.filter(quantity=0).count()
    store_value = store_stock.aggregate(
        total=Sum(F('quantity') * F('product__cost_price'))
    )['total'] or 0

    # התראות
    alerts = Alert.objects.filter(is_resolved=False).order_by('-created_at')[:10]

    # התראות מיקום
    location_alerts = LocationAlert.objects.filter(is_resolved=False).order_by('-created_at')[:10]

    # מוצרים עם מלאי נמוך במחסן
    warehouse_low_stock_items = warehouse_stock.filter(quantity__lte=F('min_quantity')).select_related('product').order_by('quantity')[:5]

    # מוצרים עם מלאי נמוך בחנות
    store_low_stock_items = store_stock.filter(quantity__lte=F('min_quantity')).select_related('product').order_by('quantity')[:5]

    # תנועות מלאי אחרונות
    recent_movements = StockMovement.objects.select_related('product').order_by('-created_at')[:10]

    # סטטיסטיקות לפי קטגוריה
    category_stats = Product.objects.values('category__name').annotate(
        count=Count('id'),
        total_value=Sum(F('quantity') * F('cost_price'))
    ).order_by('-count')[:5]

    # סטטיסטיקות לפי מיקום
    location_stats = Product.objects.values('location__name', 'location__location_type').annotate(
        count=Count('id'),
        total_quantity=Sum('quantity'),
        total_value=Sum(F('quantity') * F('cost_price'))
    ).order_by('-total_value')[:10]

    # לקוחות אחרונים
    recent_customers = Customer.objects.order_by('-created_at')[:5]

    # מכירות אחרונות
    recent_sales = Sale.objects.select_related('customer').order_by('-created_at')[:5]

    context = {
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'out_of_stock_products': out_of_stock_products,
        'total_stock_value': total_stock_value,

        # מחסן
        'warehouse_total': warehouse_total,
        'warehouse_quantity': warehouse_quantity,
        'warehouse_low_stock': warehouse_low_stock,
        'warehouse_out_of_stock': warehouse_out_of_stock,
        'warehouse_value': warehouse_value,
        'warehouse_low_stock_items': warehouse_low_stock_items,

        # חנות
        'store_total': store_total,
        'store_quantity': store_quantity,
        'store_low_stock': store_low_stock,
        'store_out_of_stock': store_out_of_stock,
        'store_value': store_value,
        'store_low_stock_items': store_low_stock_items,

        'alerts': alerts,
        'location_alerts': location_alerts,
        'recent_movements': recent_movements,
        'category_stats': category_stats,
        'location_stats': location_stats,
        'recent_customers': recent_customers,
        'recent_sales': recent_sales,
    }
    return render(request, 'inventory/dashboard.html', context)

def product_list(request):
    """רשימת מוצרים עם חיפוש וסינון"""
    search_form = ProductSearchForm(request.GET)
    products = Product.objects.select_related('category', 'supplier', 'location').prefetch_related('location_stocks__location')

    # בדיקה אם מסננים לפי מיקום ספציפי
    location_filter = request.GET.get('location', None)

    # חישוב מלאי לפי מיקום
    products = products.annotate(
        warehouse_stock=Sum(
            Case(
                When(location_stocks__location__location_type='warehouse', then=F('location_stocks__quantity')),
                default=0,
                output_field=models.IntegerField()
            )
        ),
        store_stock=Sum(
            Case(
                When(location_stocks__location__location_type='store', then=F('location_stocks__quantity')),
                default=0,
                output_field=models.IntegerField()
            )
        )
    )

    # סינון לפי מיקום אם נדרש
    if location_filter == 'warehouse':
        # הצג רק מוצרים שיש להם מלאי במחסן
        products = products.filter(location_stocks__location__location_type='warehouse', location_stocks__quantity__gt=0).distinct()
    elif location_filter == 'store':
        # הצג רק מוצרים שיש להם מלאי בחנות
        products = products.filter(location_stocks__location__location_type='store', location_stocks__quantity__gt=0).distinct()

    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        category = search_form.cleaned_data.get('category')
        supplier = search_form.cleaned_data.get('supplier')
        status = search_form.cleaned_data.get('status')
        low_stock = search_form.cleaned_data.get('low_stock')
        out_of_stock = search_form.cleaned_data.get('out_of_stock')

        if search:
            products = products.filter(
                Q(name__icontains=search) |
                Q(sku__icontains=search) |
                Q(barcode__icontains=search) |
                Q(description__icontains=search)
            )

        if category:
            products = products.filter(category=category)

        if supplier:
            products = products.filter(supplier=supplier)

        if status:
            products = products.filter(status=status)

        if low_stock:
            products = products.filter(quantity__lte=F('min_quantity'))

        if out_of_stock:
            products = products.filter(quantity=0)

    # מיון
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'quantity':
        products = products.order_by('quantity')
    elif sort_by == 'value':
        products = products.order_by(F('quantity') * F('cost_price'))
    elif sort_by == 'updated':
        products = products.order_by('-updated_at')
    else:
        products = products.order_by('name')

    # עמודים
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'products': products,
        'search_form': search_form,
        'sort_by': sort_by,
        'location_filter': location_filter,  # העברת סוג התצוגה לטמפלייט
    }
    return render(request, 'inventory/product_list.html', context)

def add_product(request):
    """הוספת מוצר חדש"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    product = form.save(commit=False)
                    # הגדרת ערכי ברירת מחדל לשדות חובה
                    if not product.sku:
                        product.sku = f"SKU-{Product.objects.count() + 1:06d}"
                    if not product.status:
                        product.status = 'active'
                    if not product.unit:
                        product.unit = 'pcs'
                    if not product.cost_price:
                        product.cost_price = 0
                    if not product.selling_price:
                        product.selling_price = 0
                    if not product.min_quantity:
                        product.min_quantity = 0
                    if not product.max_quantity:
                        product.max_quantity = 1000

                    # חישוב אחוז רווח
                    if product.cost_price and product.selling_price and product.cost_price > 0:
                        product.margin_percentage = ((product.selling_price - product.cost_price) / product.cost_price) * 100

                    # הכמות הכוללת תתאפס (תעודכן אוטומטית מ-ProductLocationStock)
                    product.quantity = 0

                    if request.user.is_authenticated:
                        product.created_by = request.user

                    product.save()

                    messages.success(request, f'✅ המוצר "{product.name}" נוסף בהצלחה!')
                    messages.info(request, 'כדי להוסיף מלאי, לך לדף המוצר ולחץ על "חלק מלאי" או "פרטי מוצר".')
                    return redirect('product_detail', pk=product.pk)
            except Exception as e:
                messages.error(request, f'❌ שגיאה בשמירת המוצר: {str(e)}')
        else:
            messages.error(request, '❌ יש שגיאות בטופס. אנא בדוק את הנתונים.')
            # הצגת שגיאות ספציפיות
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProductForm()
    return render(request, 'inventory/add_product.html', {'form': form})

# @login_required
def product_detail(request, pk):
    """פרטי מוצר"""
    product = get_object_or_404(Product, pk=pk)
    movements = StockMovement.objects.filter(product=product).order_by('-created_at')[:20]
    alerts = Alert.objects.filter(product=product, is_resolved=False)

    context = {
        'product': product,
        'movements': movements,
        'alerts': alerts,
    }
    return render(request, 'inventory/product_detail.html', context)

# @login_required
def edit_product(request, pk):
    """עריכת מוצר"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            try:
                with transaction.atomic():
                    product = form.save(commit=False)

                    # חישוב אחוז רווח מחדש
                    if product.cost_price and product.selling_price and product.cost_price > 0:
                        product.margin_percentage = ((product.selling_price - product.cost_price) / product.cost_price) * 100

                    product.save()

                    messages.success(request, f'✅ המוצר "{product.name}" עודכן בהצלחה!')
                    return redirect('product_detail', pk=product.pk)
            except Exception as e:
                messages.error(request, f'❌ שגיאה בעדכון המוצר: {str(e)}')
        else:
            messages.error(request, '❌ יש שגיאות בטופס. אנא בדוק את הנתונים.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/edit_product.html', {'form': form, 'product': product})

def delete_product(request, pk):
    """מחיקת מוצר"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_name = product.name
        try:
            # בדיקה אם יש מכירות קשורות
            sales_count = SaleItem.objects.filter(product=product).count()
            if sales_count > 0:
                messages.error(request, f'לא ניתן למחוק את המוצר "{product_name}" כי יש לו {sales_count} מכירות קשורות. שנה את הסטטוס ל"הופסק" במקום.')
                return redirect('product_detail', pk=pk)

            # בדיקה אם יש תנועות מלאי
            movements_count = StockMovement.objects.filter(product=product).count()

            # מחיקת המוצר (ימחק גם ProductLocationStock אוטומטית בגלל CASCADE)
            product.delete()
            messages.success(request, f'המוצר "{product_name}" נמחק בהצלחה!')
            return redirect('product_list')
        except Exception as e:
            messages.error(request, f'שגיאה במחיקת המוצר: {str(e)}')
            return redirect('product_detail', pk=pk)

    # בדיקה אם יש רשומות קשורות
    sales_count = SaleItem.objects.filter(product=product).count()
    movements_count = StockMovement.objects.filter(product=product).count()
    location_stocks = ProductLocationStock.objects.filter(product=product).count()

    return render(request, 'inventory/delete_product.html', {
        'product': product,
        'sales_count': sales_count,
        'movements_count': movements_count,
        'location_stocks': location_stocks,
        'can_delete': sales_count == 0
    })

# @login_required
def stock_movement(request, pk):
    """תנועת מלאי"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = StockMovementForm(request.POST, product=product)
        if form.is_valid():
            with transaction.atomic():
                movement = form.save(commit=False)
                movement.product = product
                # movement.user = request.user  # זמנית ללא משתמש
                movement.previous_quantity = product.quantity

                # עדכון כמות המלאי
                if movement.movement_type == 'in':
                    product.quantity += movement.quantity
                elif movement.movement_type == 'out':
                    if product.quantity >= movement.quantity:
                        product.quantity -= movement.quantity
                    else:
                        messages.error(request, 'אין מספיק מלאי!')
                        return render(request, 'inventory/stock_movement.html', {'form': form, 'product': product})
                elif movement.movement_type == 'adjustment':
                    product.quantity = movement.quantity

                movement.new_quantity = product.quantity
                product.save()
                movement.save()

                # יצירת התראות
                create_stock_alerts(product)

                messages.success(request, 'תנועת המלאי בוצעה בהצלחה!')
                return redirect('product_detail', pk=product.pk)
    else:
        form = StockMovementForm(product=product)
    return render(request, 'inventory/stock_movement.html', {'form': form, 'product': product})

def distribute_stock(request, pk):
    """חלוקת מלאי בין מחסן וחנות"""
    product = get_object_or_404(Product, pk=pk)

    # קבלת מחסן וחנות ראשיים
    warehouse = Location.objects.filter(location_type='warehouse', is_active=True).first()
    store = Location.objects.filter(location_type='store', is_active=True).first()

    if not warehouse or not store:
        messages.error(request, 'חסר מחסן או חנות במערכת! אנא הוסף מיקומים תחילה.')
        return redirect('product_detail', pk=pk)

    # קבלת מלאי נוכחי
    warehouse_stock, _ = ProductLocationStock.objects.get_or_create(
        product=product,
        location=warehouse,
        defaults={'quantity': 0}
    )
    store_stock, _ = ProductLocationStock.objects.get_or_create(
        product=product,
        location=store,
        defaults={'quantity': 0}
    )

    if request.method == 'POST':
        try:
            warehouse_qty = int(request.POST.get('warehouse_quantity', 0))
            store_qty = int(request.POST.get('store_quantity', 0))

            if warehouse_qty < 0 or store_qty < 0:
                messages.error(request, 'כמויות חייבות להיות חיוביות!')
                return redirect('distribute_stock', pk=pk)

            total = warehouse_qty + store_qty

            with transaction.atomic():
                # עדכון מלאי לפי מיקום
                warehouse_stock.quantity = warehouse_qty
                warehouse_stock.save()  # יסנכרן אוטומטית את product.quantity

                store_stock.quantity = store_qty
                store_stock.save()  # יסנכרן אוטומטית את product.quantity

                # המלאי הכללי מתעדכן אוטומטית דרך ProductLocationStock.save()
                # product.quantity = מחסן + חנות (אוטומטי)

                # רענון המוצר מהDB לקבלת הערך המעודכן
                product.refresh_from_db()

                messages.success(request, f'המלאי חולק בהצלחה! מחסן: {warehouse_qty}, חנות: {store_qty}, סה"כ: {product.quantity}')
                return redirect('product_detail', pk=pk)

        except ValueError:
            messages.error(request, 'ערכים לא תקינים!')
            return redirect('distribute_stock', pk=pk)

    context = {
        'product': product,
        'warehouse': warehouse,
        'store': store,
        'warehouse_stock': warehouse_stock,
        'store_stock': store_stock,
        'total_quantity': product.quantity,
    }
    return render(request, 'inventory/distribute_stock.html', context)

def sync_product_quantity_from_locations(product):
    """
    סנכרון המלאי הכללי של מוצר מסכום כל המיקומים
    הכמות הכללית = מלאי מחסן + מלאי חנות + כל מיקום אחר
    """
    from django.db.models import Sum
    total = ProductLocationStock.objects.filter(
        product=product
    ).aggregate(total=Sum('quantity'))['total'] or 0

    product.quantity = total
    product.save()
    return total

def create_stock_alerts(product):
    """יצירת התראות מלאי"""
    if product.quantity <= 0:
        Alert.objects.create(
            product=product,
            alert_type='out_of_stock',
            priority='critical',
            message=f'המוצר {product.name} אזל מהמלאי!'
        )
    elif product.quantity <= product.min_quantity:
        Alert.objects.create(
            product=product,
            alert_type='low_stock',
            priority='high',
            message=f'המוצר {product.name} במלאי נמוך ({product.quantity} יחידות)'
        )
    elif product.quantity >= product.max_quantity:
        Alert.objects.create(
            product=product,
            alert_type='overstock',
            priority='medium',
            message=f'המוצר {product.name} במלאי עודף ({product.quantity} יחידות)'
        )

# @login_required
def bulk_update(request):
    """עדכון מרובה"""
    try:
        products = Product.objects.all()[:50]  # הגבלה ל-50 מוצרים לתצוגה
    except Exception as e:
        products = []
        print(f"Error fetching products: {e}")

    if request.method == 'POST':
        form = BulkUpdateForm(request.POST)
        product_ids = request.POST.getlist('product_ids')

        if form.is_valid() and product_ids:
            action = form.cleaned_data['action']
            value = form.cleaned_data['value']
            reason = form.cleaned_data['reason']

            products_to_update = Product.objects.filter(id__in=product_ids)
            updated_count = 0

            try:
                with transaction.atomic():
                    for product in products_to_update:
                        old_quantity = product.quantity

                        if action == 'add':
                            product.quantity += int(value or 0)
                        elif action == 'subtract':
                            product.quantity = max(0, product.quantity - int(value or 0))
                        elif action == 'set':
                            product.quantity = int(value or 0)
                        elif action == 'update_price':
                            product.selling_price = value or product.selling_price
                        elif action == 'change_status':
                            product.status = form.cleaned_data['new_status']
                        elif action == 'change_category':
                            product.category = form.cleaned_data['new_category']

                        product.save()

                        # יצירת תנועת מלאי
                        if action in ['add', 'subtract', 'set']:
                            StockMovement.objects.create(
                                product=product,
                                movement_type='adjustment',
                                quantity=product.quantity - old_quantity,
                                previous_quantity=old_quantity,
                                new_quantity=product.quantity,
                                reason=f'עדכון מרובה: {reason}',
                                # user=request.user  # זמנית ללא משתמש
                            )

                        updated_count += 1

                messages.success(request, f'{updated_count} מוצרים עודכנו בהצלחה!')
                return redirect('product_list')

            except Exception as e:
                messages.error(request, f'שגיאה בעדכון: {str(e)}')
        else:
            if not product_ids:
                messages.error(request, 'אנא בחר לפחות מוצר אחד')
            else:
                messages.error(request, 'יש שגיאות בטופס')
    else:
        form = BulkUpdateForm()

    return render(request, 'inventory/bulk_update.html', {'form': form, 'products': products})

# @login_required
def alerts(request):
    """ניהול התראות"""
    alerts = Alert.objects.filter(is_resolved=False).order_by('-created_at')

    if request.method == 'POST':
        alert_id = request.POST.get('alert_id')
        action = request.POST.get('action')

        if alert_id and action:
            alert = get_object_or_404(Alert, id=alert_id)
            if action == 'mark_read':
                alert.is_read = True
                alert.save()
            elif action == 'resolve':
                alert.is_resolved = True
                alert.resolved_at = timezone.now()
                # alert.resolved_by = request.user  # זמנית ללא משתמש
                alert.save()

    return render(request, 'inventory/alerts.html', {'alerts': alerts})

# @login_required
def reports(request):
    """דוחות ואנליטיקה"""
    # סטטיסטיקות כלליות
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(quantity__lte=F('min_quantity')).count()
    out_of_stock_products = Product.objects.filter(quantity=0).count()
    total_stock_value = Product.objects.aggregate(
        total=Sum(F('quantity') * F('cost_price'))
    )['total'] or 0

    # דוח מלאי נמוך
    low_stock = Product.objects.filter(quantity__lte=F('min_quantity')).order_by('quantity')

    # דוח ערך מלאי
    stock_value = Product.objects.aggregate(
        total_cost=Sum(F('quantity') * F('cost_price')),
        total_selling=Sum(F('quantity') * F('selling_price'))
    )

    # דוח תנועות מלאי
    movements_today = StockMovement.objects.filter(
        created_at__date=timezone.now().date()
    ).count()

    movements_week = StockMovement.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=7)
    ).count()

    # דוח לפי קטגוריה
    category_report = Product.objects.values('category__name').annotate(
        count=Count('id'),
        total_quantity=Sum('quantity'),
        total_value=Sum(F('quantity') * F('cost_price'))
    ).order_by('-total_value')

    # דוח ספקים
    supplier_stats = Product.objects.values('supplier__name').annotate(
        count=Count('id'),
        total_value=Sum(F('quantity') * F('cost_price'))
    ).order_by('-count')[:10]

    # דוח מוצרים עם הרווח הגבוה ביותר
    high_margin_products = Product.objects.filter(
        margin_percentage__gt=0
    ).order_by('-margin_percentage')[:10]

    # דוח תנועות לפי סוג
    movement_stats = StockMovement.objects.values('movement_type').annotate(
        count=Count('id'),
        total_quantity=Sum('quantity')
    ).order_by('-count')

    # דוח התראות
    active_alerts = Alert.objects.filter(is_resolved=False).count()
    critical_alerts = Alert.objects.filter(is_resolved=False, priority='critical').count()

    context = {
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'out_of_stock_products': out_of_stock_products,
        'total_stock_value': total_stock_value,
        'low_stock': low_stock,
        'stock_value': stock_value,
        'movements_today': movements_today,
        'movements_week': movements_week,
        'category_report': category_report,
        'supplier_stats': supplier_stats,
        'high_margin_products': high_margin_products,
        'movement_stats': movement_stats,
        'active_alerts': active_alerts,
        'critical_alerts': critical_alerts,
    }
    return render(request, 'inventory/reports.html', context)

def generate_barcode(request):
    """יצירת ברקוד אוטומטי"""
    if request.method == 'POST':
        barcode_text = request.POST.get('barcode_text', '')
        if barcode_text:
            try:
                # יצירת ברקוד EAN13
                ean = barcode.get('ean13', barcode_text, writer=ImageWriter())
                buffer = BytesIO()
                ean.write(buffer)
                buffer.seek(0)

                # המרה ל-base64
                barcode_data = base64.b64encode(buffer.getvalue()).decode()

                return JsonResponse({
                    'success': True,
                    'barcode_data': f'data:image/png;base64,{barcode_data}',
                    'barcode_text': barcode_text
                })
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'No barcode text provided'})

# ניהול קטגוריות
# @login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'inventory/category_list.html', {'categories': categories})

# @login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'הקטגוריה נוספה בהצלחה!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'inventory/add_category.html', {'form': form})

# ניהול ספקים
# @login_required
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/supplier_list.html', {'suppliers': suppliers})

# @login_required
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'הספק נוסף בהצלחה!')
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'inventory/add_supplier.html', {'form': form})

def edit_category(request, pk):
    """עריכת קטגוריה"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'הקטגוריה עודכנה בהצלחה!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'inventory/edit_category.html', {'form': form, 'category': category})

def delete_category(request, pk):
    """מחיקת קטגוריה"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'הקטגוריה "{category_name}" נמחקה בהצלחה!')
        return redirect('category_list')
    return render(request, 'inventory/delete_category.html', {'category': category})

def edit_supplier(request, pk):
    """עריכת ספק"""
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'הספק עודכן בהצלחה!')
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'inventory/edit_supplier.html', {'form': form, 'supplier': supplier})

def delete_supplier(request, pk):
    """מחיקת ספק"""
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier_name = supplier.name
        supplier.delete()
        messages.success(request, f'הספק "{supplier_name}" נמחק בהצלחה!')
        return redirect('supplier_list')
    return render(request, 'inventory/delete_supplier.html', {'supplier': supplier})

# פונקציות ייצוא דוחות
def export_products_csv(request):
    """ייצוא רשימת מוצרים ל-CSV"""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    # הוספת BOM ל-UTF-8 לתמיכה ב-Excel
    response.write('\ufeff')

    writer = csv.writer(response)
    writer.writerow([
        'שם מוצר', 'SKU', 'תיאור', 'קטגוריה', 'ספק', 'מיקום',
        'כמות', 'כמות מינימלית', 'כמות מקסימלית', 'יחידה',
        'מחיר עלות', 'מחיר מכירה', 'אחוז רווח', 'ברקוד',
        'סטטוס', 'משקל', 'מידות', 'הערות', 'תאריך יצירה'
    ])

    products = Product.objects.select_related('category', 'supplier').prefetch_related('location_stocks__location').all()
    for product in products:
        # מיקומי המוצר (מתוך ProductLocationStock)
        locations_str = ', '.join([
            f"{pls.location.name}: {pls.quantity}"
            for pls in product.location_stocks.all()
        ]) if product.location_stocks.exists() else 'אין מיקום'

        # הכנת SKU וברקוד כטקסט (למניעת המרה למספר ב-Excel)
        sku_text = f"'{product.sku}" if product.sku else ''
        barcode_text = f"'{product.barcode}" if product.barcode else ''

        writer.writerow([
            product.name,
            sku_text,  # SKU עם גרש בהתחלה
            product.description or '',
            product.category.name if product.category else '',
            product.supplier.name if product.supplier else '',
            locations_str,
            product.quantity,
            product.min_quantity,
            product.max_quantity,
            product.get_unit_display(),
            product.cost_price or 0,
            product.selling_price or 0,
            product.margin_percentage or 0,
            barcode_text,  # ברקוד עם גרש בהתחלה
            product.get_status_display(),
            product.weight or '',
            product.dimensions or '',
            product.notes or '',
            product.created_at.strftime('%d/%m/%Y %H:%M') if product.created_at else ''
        ])

    return response

def export_low_stock_csv(request):
    """ייצוא מוצרים במלאי נמוך ל-CSV"""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="low_stock_products.csv"'

    response.write('\ufeff')
    writer = csv.writer(response)
    writer.writerow([
        'שם מוצר', 'SKU', 'כמות נוכחית', 'כמות מינימלית', 'סטטוס',
        'קטגוריה', 'ספק', 'מחיר עלות', 'ערך מלאי'
    ])

    low_stock_products = Product.objects.filter(quantity__lte=F('min_quantity')).select_related('category', 'supplier')
    for product in low_stock_products:
        # הכנת SKU כטקסט
        sku_text = f"'{product.sku}" if product.sku else ''

        writer.writerow([
            product.name,
            sku_text,  # SKU עם גרש בהתחלה
            product.quantity,
            product.min_quantity,
            'אזל מהמלאי' if product.quantity == 0 else 'מלאי נמוך',
            product.category.name if product.category else '',
            product.supplier.name if product.supplier else '',
            product.cost_price or 0,
            product.stock_value or 0
        ])

    return response

def export_movements_csv(request):
    """ייצוא תנועות מלאי ל-CSV"""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="stock_movements.csv"'

    response.write('\ufeff')
    writer = csv.writer(response)
    writer.writerow([
        'מוצר', 'SKU', 'סוג תנועה', 'כמות', 'כמות קודמת', 'כמות חדשה',
        'סיבה', 'התייחסות', 'תאריך'
    ])

    movements = StockMovement.objects.select_related('product').order_by('-created_at')
    for movement in movements:
        # הכנת SKU כטקסט
        sku_text = f"'{movement.product.sku}" if movement.product.sku else ''

        writer.writerow([
            movement.product.name,
            sku_text,  # SKU עם גרש בהתחלה
            movement.get_movement_type_display(),
            movement.quantity,
            movement.previous_quantity,
            movement.new_quantity,
            movement.reason or '',
            movement.reference or '',
            movement.created_at.strftime('%d/%m/%Y %H:%M')
        ])

    return response

def export_full_report_csv(request):
    """ייצוא דוח מלא ל-CSV"""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="full_report.csv"'
    response.write('\ufeff')  # BOM for UTF-8

    writer = csv.writer(response)

    # כותרת הדוח
    writer.writerow(['דוח מלאי מלא', timezone.now().strftime('%d/%m/%Y %H:%M')])
    writer.writerow([])  # שורה ריקה

    # סטטיסטיקות כלליות
    writer.writerow(['=== סטטיסטיקות כלליות ==='])
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(quantity__lte=F('min_quantity')).count()
    out_of_stock_products = Product.objects.filter(quantity=0).count()
    total_stock_value = Product.objects.aggregate(
        total=Sum(F('quantity') * F('cost_price'))
    )['total'] or 0

    writer.writerow(['סה"כ מוצרים', total_products])
    writer.writerow(['מוצרים במלאי נמוך', low_stock_products])
    writer.writerow(['מוצרים שאזלו', out_of_stock_products])
    writer.writerow(['ערך מלאי כולל', f'₪{total_stock_value:,.2f}'])
    writer.writerow([])  # שורה ריקה

    # דוח לפי קטגוריות
    writer.writerow(['=== דוח לפי קטגוריות ==='])
    writer.writerow(['קטגוריה', 'כמות מוצרים', 'כמות יחידות', 'ערך מלאי'])
    for item in Product.objects.values('category__name').annotate(
        count=Count('id'),
        total_quantity=Sum('quantity'),
        total_value=Sum(F('quantity') * F('cost_price'))
    ).order_by('-total_value'):
        writer.writerow([
            item['category__name'] or 'ללא קטגוריה',
            item['count'],
            item['total_quantity'] or 0,
            f"₪{(item['total_value'] or 0):,.2f}"
        ])
    writer.writerow([])  # שורה ריקה

    # דוח ספקים
    writer.writerow(['=== דוח ספקים ==='])
    writer.writerow(['ספק', 'כמות מוצרים', 'כמות יחידות', 'ערך מלאי'])
    for item in Product.objects.values('supplier__name').annotate(
        count=Count('id'),
        total_quantity=Sum('quantity'),
        total_value=Sum(F('quantity') * F('cost_price'))
    ).order_by('-count'):
        writer.writerow([
            item['supplier__name'] or 'ללא ספק',
            item['count'],
            item['total_quantity'] or 0,
            f"₪{(item['total_value'] or 0):,.2f}"
        ])
    writer.writerow([])  # שורה ריקה

    # דוח מוצרים רווחיים
    writer.writerow(['=== מוצרים רווחיים ==='])
    writer.writerow(['מוצר', 'SKU', 'כמות', 'מחיר עלות', 'מחיר מכירה', 'אחוז רווח'])
    high_margin = Product.objects.filter(margin_percentage__gt=0).order_by('-margin_percentage')[:20]
    for product in high_margin:
        sku_text = f"'{product.sku}" if product.sku else ''
        writer.writerow([
            product.name,
            sku_text,
            product.quantity,
            f'₪{product.cost_price or 0}',
            f'₪{product.selling_price or 0}',
            f'{product.margin_percentage:.1f}%'
        ])
    writer.writerow([])  # שורה ריקה

    # דוח מלאי נמוך
    writer.writerow(['=== מוצרים במלאי נמוך ==='])
    writer.writerow(['מוצר', 'SKU', 'כמות נוכחית', 'כמות מינימלית', 'סטטוס'])
    low_stock = Product.objects.filter(quantity__lte=F('min_quantity')).order_by('quantity')
    for product in low_stock:
        sku_text = f"'{product.sku}" if product.sku else ''
        writer.writerow([
            product.name,
            sku_text,
            product.quantity,
            product.min_quantity,
            'אזל מהמלאי' if product.quantity == 0 else 'מלאי נמוך'
        ])
    writer.writerow([])  # שורה ריקה

    # דוח תנועות מלאי
    writer.writerow(['=== תנועות מלאי (7 ימים אחרונים) ==='])
    writer.writerow(['תאריך', 'מוצר', 'סוג תנועה', 'כמות', 'כמות קודמת', 'כמות חדשה'])
    recent_movements = StockMovement.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=7)
    ).select_related('product').order_by('-created_at')[:50]
    for movement in recent_movements:
        writer.writerow([
            movement.created_at.strftime('%d/%m/%Y %H:%M'),
            movement.product.name,
            movement.get_movement_type_display(),
            movement.quantity,
            movement.previous_quantity,
            movement.new_quantity
        ])

    return response

def export_reports_json(request):
    """ייצוא דוחות ל-JSON"""
    # סטטיסטיקות כלליות
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(quantity__lte=F('min_quantity')).count()
    out_of_stock_products = Product.objects.filter(quantity=0).count()
    total_stock_value = Product.objects.aggregate(
        total=Sum(F('quantity') * F('cost_price'))
    )['total'] or 0

    # דוח לפי קטגוריות
    category_report = []
    for item in Product.objects.values('category__name').annotate(
        count=Count('id'),
        total_value=Sum(F('quantity') * F('cost_price'))
    ).order_by('-total_value'):
        category_report.append({
            'category_name': item['category__name'],
            'count': item['count'],
            'total_value': float(item['total_value'] or 0)
        })

    # דוח ספקים
    supplier_report = []
    for item in Product.objects.values('supplier__name').annotate(
        count=Count('id'),
        total_value=Sum(F('quantity') * F('cost_price'))
    ).order_by('-count'):
        supplier_report.append({
            'supplier_name': item['supplier__name'],
            'count': item['count'],
            'total_value': float(item['total_value'] or 0)
        })

    data = {
        'export_date': timezone.now().strftime('%d/%m/%Y %H:%M'),
        'summary': {
            'total_products': total_products,
            'low_stock_products': low_stock_products,
            'out_of_stock_products': out_of_stock_products,
            'total_stock_value': float(total_stock_value)
        },
        'category_report': category_report,
        'supplier_report': supplier_report
    }

    response = HttpResponse(
        json.dumps(data, ensure_ascii=False, indent=2),
        content_type='application/json; charset=utf-8'
    )
    response['Content-Disposition'] = 'attachment; filename="inventory_report.json"'
    return response

# Views למכירות
def customer_list(request):
    """רשימת לקוחות"""
    customers = Customer.objects.all()
    return render(request, 'inventory/customer_list.html', {'customers': customers})

def add_customer(request):
    """הוספת לקוח חדש"""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            try:
                customer = form.save(commit=False)
                # רק אם המשתמש מחובר, נשמור אותו
                if request.user.is_authenticated:
                    customer.created_by = request.user
                customer.save()
                messages.success(request, 'הלקוח נוסף בהצלחה!')
                return redirect('customer_list')
            except Exception as e:
                messages.error(request, f'שגיאה בשמירת הלקוח: {str(e)}')
        else:
            messages.error(request, 'יש שגיאות בטופס. אנא בדוק את הנתונים.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomerForm()
    return render(request, 'inventory/add_customer.html', {'form': form})

def sale_list(request):
    """רשימת מכירות"""
    sales = Sale.objects.select_related('customer').all()
    return render(request, 'inventory/sale_list.html', {'sales': sales})

def add_sale(request):
    """הוספת מכירה חדשה עם אפשרות להוסיף לקוח מהר"""
    if request.method == 'POST':
        # בדיקה אם מוסיפים לקוח חדש במהירות
        if 'add_quick_customer' in request.POST:
            customer_name = request.POST.get('quick_customer_name', '').strip()
            customer_phone = request.POST.get('quick_customer_phone', '').strip()
            customer_email = request.POST.get('quick_customer_email', '').strip()

            if customer_name:
                # יצירת לקוח חדש
                customer = Customer.objects.create(
                    name=customer_name,
                    phone=customer_phone if customer_phone else None,
                    email=customer_email if customer_email else None,
                    customer_type='individual',
                    created_by=request.user if request.user.is_authenticated else None
                )
                messages.success(request, f'הלקוח "{customer_name}" נוסף בהצלחה!')

                # החזרת הטופס עם הלקוח החדש נבחר
                form = SaleForm(initial={'customer': customer.id})
                formset = SaleItemFormSet()
                return render(request, 'inventory/add_sale.html', {
                    'form': form,
                    'formset': formset,
                    'new_customer_id': customer.id
                })
            else:
                messages.error(request, 'נא להזין שם לקוח!')
                form = SaleForm()
                formset = SaleItemFormSet()
                return render(request, 'inventory/add_sale.html', {'form': form, 'formset': formset})

        # טיפול במכירה רגילה
        form = SaleForm(request.POST)
        formset = SaleItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            # בדיקת מלאי לפני שמירה
            location = form.cleaned_data.get('location')
            insufficient_stock = []

            for item_form in formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE', False):
                    product = item_form.cleaned_data.get('product')
                    quantity = item_form.cleaned_data.get('quantity', 0)

                    if product and quantity > 0 and location:
                        # בדיקת מלאי במיקום
                        location_stock = ProductLocationStock.objects.filter(
                            product=product,
                            location=location
                        ).first()

                        available_qty = location_stock.quantity if location_stock else 0

                        if available_qty < quantity:
                            location_name = location.get_location_type_display()
                            insufficient_stock.append({
                                'product': product.name,
                                'requested': quantity,
                                'available': available_qty,
                                'location': location_name
                            })

            # אם יש מוצרים שאין להם מלאי מספיק
            if insufficient_stock:
                for item in insufficient_stock:
                    if item['available'] == 0:
                        messages.error(
                            request,
                            f'❌ {item["product"]}: אין במלאי של {item["location"]}! המלאי אזל.'
                        )
                    else:
                        messages.error(
                            request,
                            f'❌ {item["product"]}: אין מלאי מספיק ב{item["location"]}! '
                            f'מבוקש: {item["requested"]}, זמין: {item["available"]}'
                        )
                messages.warning(request, '⚠️ לא ניתן להשלים את המכירה. אנא תקן את הכמויות או העבר מלאי מהמחסן.')

            else:
                # אם יש מלאי מספיק, המשך לשמירה
                with transaction.atomic():
                    sale = form.save(commit=False)
                    if request.user.is_authenticated:
                        sale.created_by = request.user
                    # מספר החשבונית ייווצר אוטומטית ב-save
                    sale.save()

                    # שמירת פריטי החשבונית
                    formset.instance = sale
                    sale_items = formset.save()

                    # עדכון סכום כולל
                    # total_price כבר כולל מע"מ, צריך להפריד אותו
                    total_with_vat = sum(item.total_price for item in sale.items.all())
                    # חישוב subtotal (לפני מע"מ) מתוך total (כולל מע"מ)
                    sale.subtotal = total_with_vat / (1 + sale.tax_rate / 100)
                    sale.save()

                    # עדכון מלאי - במיקום הספציפי
                    # המלאי הכללי יתעדכן אוטומטית ב-ProductLocationStock.save()
                    from .models import ProductLocationStock
                    from django.utils import timezone

                    for item in sale_items:
                        product = item.product

                        # אם יש מיקום למכירה, עדכן מלאי במיקום
                        if sale.location:
                            # מצא או צור רשומת מלאי למיקום זה
                            location_stock, created = ProductLocationStock.objects.get_or_create(
                                product=product,
                                location=sale.location,
                                defaults={'quantity': 0}
                            )

                            # עדכן מלאי במיקום (הסנכרון אוטומטי)
                            location_stock.quantity -= item.quantity
                            location_stock.last_sold = timezone.now()
                            location_stock.save()  # זה יסנכרן אוטומטית את product.quantity

                    messages.success(request, f'✅ המכירה נוצרה בהצלחה! מספר חשבונית: {sale.invoice_number}')
                    return redirect('sale_detail', pk=sale.pk)
        else:
            messages.error(request, 'אנא תקן את השגיאות בטופס.')
    else:
        # קבע חנות ראשית כברירת מחדל
        default_store = Location.objects.filter(
            location_type='store',
            is_main_store=True
        ).first()

        if not default_store:
            # אם אין חנות ראשית, קח את החנות הראשונה
            default_store = Location.objects.filter(location_type='store').first()

        form = SaleForm(initial={'location': default_store.id if default_store else None})
        formset = SaleItemFormSet()

    # הכן נתוני מוצרים ולקוחות עבור JavaScript
    import json
    products_data = {}
    for product in Product.objects.filter(quantity__gt=0):
        products_data[str(product.id)] = {
            'name': product.name,
            'price': float(product.selling_price or product.price or 0),
            'quantity': product.quantity
        }

    customers_data = {}
    for customer in Customer.objects.all():
        customers_data[str(customer.id)] = {
            'name': customer.name,
            'discount': float(customer.discount_percent or 0)
        }

    context = {
        'form': form,
        'formset': formset,
        'customers': Customer.objects.all().order_by('name'),
        'products': Product.objects.filter(quantity__gt=0).order_by('name'),
        'locations': Location.objects.filter(is_active=True).order_by('location_type', 'name'),
        'products_json': json.dumps(products_data),
        'customers_json': json.dumps(customers_data),
    }
    return render(request, 'inventory/add_sale.html', context)

def sale_detail(request, pk):
    """פרטי מכירה"""
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'inventory/sale_detail.html', {'sale': sale})

def edit_sale(request, pk):
    """עריכת מכירה"""
    sale = get_object_or_404(Sale, pk=pk)

    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        formset = SaleItemFormSet(request.POST, instance=sale)

        if form.is_valid() and formset.is_valid():
            # בדיקת מלאי לפני שמירה
            location = form.cleaned_data.get('location')
            insufficient_stock = []

            # החזר מלאי זמנית למבנה נתונים
            temp_stock = {}
            for item in sale.items.all():
                product = item.product
                if location:
                    location_stock = ProductLocationStock.objects.filter(
                        product=product,
                        location=location
                    ).first()
                    if location_stock:
                        temp_stock[product.id] = location_stock.quantity + item.quantity

            # בדיקת מלאי חדש
            for item_form in formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE', False):
                    product = item_form.cleaned_data.get('product')
                    quantity = item_form.cleaned_data.get('quantity', 0)

                    if product and quantity > 0 and location:
                        # בדיקת מלאי במיקום (כולל המלאי שהוחזר זמנית)
                        available_qty = temp_stock.get(product.id, 0)

                        if available_qty < quantity:
                            location_name = location.get_location_type_display()
                            insufficient_stock.append({
                                'product': product.name,
                                'requested': quantity,
                                'available': available_qty,
                                'location': location_name
                            })

            # אם יש מוצרים שאין להם מלאי מספיק
            if insufficient_stock:
                for item in insufficient_stock:
                    if item['available'] == 0:
                        messages.error(
                            request,
                            f'❌ {item["product"]}: אין במלאי של {item["location"]}! המלאי אזל.'
                        )
                    else:
                        messages.error(
                            request,
                            f'❌ {item["product"]}: אין מלאי מספיק ב{item["location"]}! '
                            f'מבוקש: {item["requested"]}, זמין: {item["available"]}'
                        )
                messages.warning(request, '⚠️ לא ניתן לעדכן את המכירה. אנא תקן את הכמויות או העבר מלאי מהמחסן.')

            else:
                # אם יש מלאי מספיק, המשך לשמירה
                with transaction.atomic():
                    # החזר מלאי ישן לפני עדכון
                    for item in sale.items.all():
                        product = item.product
                        if sale.location:
                            location_stock = ProductLocationStock.objects.filter(
                                product=product,
                                location=sale.location
                            ).first()
                            if location_stock:
                                location_stock.quantity += item.quantity
                                location_stock.save()  # זה יסנכרן אוטומטית את product.quantity

                    # עדכן מכירה
                    sale = form.save()
                    formset.instance = sale
                    sale_items = formset.save()

                    # עדכן סכום
                    # total_price כבר כולל מע"מ, צריך להפריד אותו
                    total_with_vat = sum(item.total_price for item in sale.items.all())
                    sale.subtotal = total_with_vat / (1 + sale.tax_rate / 100)
                    sale.save()

                    # הורד מלאי חדש
                    from django.utils import timezone
                    for item in sale_items:
                        product = item.product
                        if sale.location:
                            location_stock, created = ProductLocationStock.objects.get_or_create(
                                product=product,
                                location=sale.location,
                                defaults={'quantity': 0}
                            )
                            location_stock.quantity -= item.quantity
                            location_stock.last_sold = timezone.now()
                            location_stock.save()  # זה יסנכרן אוטומטית את product.quantity

                    messages.success(request, '✅ המכירה עודכנה בהצלחה!')
                    return redirect('sale_detail', pk=sale.pk)
    else:
        form = SaleForm(instance=sale)
        formset = SaleItemFormSet(instance=sale)

    context = {
        'form': form,
        'formset': formset,
        'sale': sale,
        'is_edit': True,
    }
    return render(request, 'inventory/add_sale.html', context)

def delete_sale(request, pk):
    """מחיקת מכירה"""
    sale = get_object_or_404(Sale, pk=pk)

    if request.method == 'POST':
        with transaction.atomic():
            # החזר מלאי (הסנכרון אוטומטי)
            for item in sale.items.all():
                product = item.product
                if sale.location:
                    location_stock = ProductLocationStock.objects.filter(
                        product=product,
                        location=sale.location
                    ).first()
                    if location_stock:
                        location_stock.quantity += item.quantity
                        location_stock.save()  # זה יסנכרן אוטומטית את product.quantity

            invoice_num = sale.invoice_number
            sale.delete()
            messages.success(request, f'✅ חשבונית {invoice_num} נמחקה והמלאי הוחזר בהצלחה')
            return redirect('sale_list')

    return render(request, 'inventory/delete_sale.html', {'sale': sale})

def search_product_by_barcode(request):
    """API endpoint לחיפוש מוצר לפי ברקוד"""
    barcode = request.GET.get('barcode', '').strip()

    if not barcode:
        return JsonResponse({'error': 'ברקוד לא סופק'}, status=400)

    try:
        product = Product.objects.get(barcode=barcode, status='active')

        data = {
            'success': True,
            'product': {
                'id': product.id,
                'name': product.name,
                'sku': product.sku or '',
                'barcode': product.barcode,
                'price': float(product.selling_price or product.price or 0),
                'quantity': product.quantity,
                'unit': product.get_unit_display(),
                'category': product.category.name if product.category else '',
            }
        }
        return JsonResponse(data)

    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'מוצר לא נמצא',
            'message': f'לא נמצא מוצר עם ברקוד {barcode}'
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'שגיאה בחיפוש',
            'message': str(e)
        }, status=500)

# Views להעברות מלאי
def transfer_list(request):
    """רשימת העברות מלאי"""
    transfers = InventoryTransfer.objects.select_related('from_location', 'to_location').all()
    return render(request, 'inventory/transfer_list.html', {'transfers': transfers})

def add_transfer(request):
    """הוספת העברת מלאי חדשה"""
    if request.method == 'POST':
        form = InventoryTransferForm(request.POST)
        formset = TransferItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                transfer = form.save(commit=False)
                # יצירת מספר העברה אוטומטי
                if not transfer.transfer_number:
                    transfer.transfer_number = f"TRF-{InventoryTransfer.objects.count() + 1:06d}"
                transfer.save()

                # שמירת פריטי ההעברה
                formset.instance = transfer
                formset.save()

                # עדכון מלאי אוטומטי אם ההעברה הושלמה
                if transfer.status == 'completed':
                    update_inventory_from_transfer(transfer)

                messages.success(request, 'ההעברה נוספה בהצלחה!')
                return redirect('transfer_detail', pk=transfer.pk)
    else:
        form = InventoryTransferForm()
        formset = TransferItemFormSet()

    return render(request, 'inventory/add_transfer.html', {'form': form, 'formset': formset})

def transfer_detail(request, pk):
    """פרטי העברה"""
    transfer = get_object_or_404(InventoryTransfer, pk=pk)
    return render(request, 'inventory/transfer_detail.html', {'transfer': transfer})

# מיקומים
def location_list(request):
    """רשימת מיקומים"""
    locations = Location.objects.all()
    return render(request, 'inventory/location_list.html', {'locations': locations})

def add_location(request):
    """הוספת מיקום חדש"""
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            try:
                location = form.save(commit=False)
                location.created_by = request.user
                location.save()
                messages.success(request, 'המיקום נוסף בהצלחה!')
                return redirect('location_list')
            except Exception as e:
                messages.error(request, f'שגיאה בשמירת המיקום: {str(e)}')
        else:
            messages.error(request, 'יש שגיאות בטופס. אנא בדוק את הנתונים.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = LocationForm()
    return render(request, 'inventory/add_location.html', {'form': form})

def location_detail(request, pk):
    """פרטי מיקום"""
    location = get_object_or_404(Location, pk=pk)
    products = Product.objects.filter(location=location)
    alerts = LocationAlert.objects.filter(location=location, is_resolved=False)
    return render(request, 'inventory/location_detail.html', {
        'location': location,
        'products': products,
        'alerts': alerts
    })

def edit_location(request, pk):
    """עריכת מיקום"""
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'המיקום עודכן בהצלחה!')
                return redirect('location_detail', pk=pk)
            except Exception as e:
                messages.error(request, f'שגיאה בעדכון המיקום: {str(e)}')
        else:
            messages.error(request, 'יש שגיאות בטופס. אנא בדוק את הנתונים.')
    else:
        form = LocationForm(instance=location)
    return render(request, 'inventory/edit_location.html', {'form': form, 'location': location})

def delete_location(request, pk):
    """מחיקת מיקום"""
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        location_name = location.name
        location.delete()
        messages.success(request, f'המיקום "{location_name}" נמחק בהצלחה!')
        return redirect('location_list')
    return render(request, 'inventory/delete_location.html', {'location': location})

def complete_transfer(request, pk):
    """השלמת העברה ועדכון מלאי"""
    transfer = get_object_or_404(InventoryTransfer, pk=pk)

    if transfer.status != 'completed':
        with transaction.atomic():
            transfer.status = 'completed'
            transfer.save()

            # עדכון מלאי
            update_inventory_from_transfer(transfer)

            messages.success(request, 'ההעברה הושלמה והמלאי עודכן!')

    return redirect('transfer_detail', pk=transfer.pk)

def update_inventory_from_transfer(transfer):
    """עדכון מלאי אוטומטי מהעברה"""
    for item in transfer.items.all():
        # הפחתה מהמיקום המקור
        if item.product.location == transfer.from_location:
            item.product.quantity = max(0, item.product.quantity - item.quantity)
        else:
            # אם המוצר לא במיקום המקור, נחפש אותו
            try:
                product_in_source = Product.objects.get(
                    name=item.product.name,
                    location=transfer.from_location
                )
                product_in_source.quantity = max(0, product_in_source.quantity - item.quantity)
                product_in_source.save()
            except Product.DoesNotExist:
                pass

        # הוספה למיקום היעד
        if item.product.location == transfer.to_location:
            item.product.quantity += item.quantity
        else:
            # אם המוצר לא במיקום היעד, נחפש אותו או ניצור חדש
            try:
                product_in_dest = Product.objects.get(
                    name=item.product.name,
                    location=transfer.to_location
                )
                product_in_dest.quantity += item.quantity
                product_in_dest.save()
            except Product.DoesNotExist:
                # יצירת עותק של המוצר במיקום היעד
                new_product = Product.objects.create(
                    name=item.product.name,
                    description=item.product.description,
                    category=item.product.category,
                    supplier=item.product.supplier,
                    location=transfer.to_location,
                    quantity=item.quantity,
                    min_quantity=item.product.min_quantity,
                    max_quantity=item.product.max_quantity,
                    unit=item.product.unit,
                    cost_price=item.product.cost_price,
                    selling_price=item.product.selling_price,
                    barcode=item.product.barcode,
                    status=item.product.status,
                    weight=item.product.weight,
                    dimensions=item.product.dimensions,
                    notes=item.product.notes,
                )

        item.product.save()

        # יצירת תנועת מלאי
        StockMovement.objects.create(
            product=item.product,
            movement_type='transfer_out' if transfer.transfer_type.startswith('warehouse_to') else 'transfer_in',
            quantity=-item.quantity if transfer.transfer_type.startswith('warehouse_to') else item.quantity,
            reason=f'העברה #{transfer.transfer_number}',
        )

# Views ל-CRM
def crm_dashboard(request):
    """דשבורד CRM"""
    # סטטיסטיקות לקוחות
    total_customers = Customer.objects.count()
    active_customers = Customer.objects.filter(is_active=True).count()
    vip_customers = Customer.objects.filter(is_vip=True).count()

    # לקוחות לפי סוג
    customers_by_type = Customer.objects.values('customer_type').annotate(
        count=Count('id')
    ).order_by('-count')

    # לקוחות לפי עדיפות
    customers_by_priority = Customer.objects.values('priority').annotate(
        count=Count('id')
    ).order_by('-count')

    # לקוחות עם רכישות גבוהות
    top_customers = Customer.objects.filter(
        total_purchases__gt=0
    ).order_by('-total_purchases')[:10]

    # התראות לקוחות
    customer_alerts = CustomerAlert.objects.filter(
        is_resolved=False
    ).order_by('-created_at')[:10]

    # הערות אחרונות
    recent_notes = CustomerNote.objects.select_related(
        'customer', 'created_by'
    ).order_by('-created_at')[:10]

    # מכירות אחרונות
    recent_sales = Sale.objects.select_related('customer').order_by('-created_at')[:10]

    context = {
        'total_customers': total_customers,
        'active_customers': active_customers,
        'vip_customers': vip_customers,
        'customers_by_type': customers_by_type,
        'customers_by_priority': customers_by_priority,
        'top_customers': top_customers,
        'customer_alerts': customer_alerts,
        'recent_notes': recent_notes,
        'recent_sales': recent_sales,
    }
    return render(request, 'inventory/crm_dashboard.html', context)

def customer_detail(request, pk):
    """פרטי לקוח"""
    customer = get_object_or_404(Customer, pk=pk)

    # היסטוריית מכירות
    sale_history = CustomerSaleHistory.objects.filter(
        customer=customer
    ).order_by('-sale_date')[:20]

    # הערות לקוח
    notes = CustomerNote.objects.filter(
        customer=customer
    ).order_by('-created_at')[:10]

    # התראות לקוח
    alerts = CustomerAlert.objects.filter(
        customer=customer
    ).order_by('-created_at')[:10]

    # סטטיסטיקות
    total_sales = sale_history.count()
    total_amount = sale_history.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    context = {
        'customer': customer,
        'sale_history': sale_history,
        'notes': notes,
        'alerts': alerts,
        'total_sales': total_sales,
        'total_amount': total_amount,
    }
    return render(request, 'inventory/customer_detail.html', context)

def edit_customer(request, pk):
    """עריכת לקוח"""
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'הלקוח עודכן בהצלחה!')
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'inventory/edit_customer.html', {'form': form, 'customer': customer})

def delete_customer(request, pk):
    """מחיקת לקוח"""
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer_name = customer.name
        customer.delete()
        messages.success(request, f'הלקוח "{customer_name}" נמחק בהצלחה!')
        return redirect('customer_list')
    return render(request, 'inventory/delete_customer.html', {'customer': customer})

def add_customer_note(request, customer_pk):
    """הוספת הערה ללקוח"""
    customer = get_object_or_404(Customer, pk=customer_pk)

    if request.method == 'POST':
        form = CustomerNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.customer = customer
            note.created_by = request.user
            note.save()
            messages.success(request, 'ההערה נוספה בהצלחה!')
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerNoteForm()

    return render(request, 'inventory/add_customer_note.html', {
        'form': form, 'customer': customer
    })

def add_customer_alert(request, customer_pk):
    """הוספת התראה ללקוח"""
    customer = get_object_or_404(Customer, pk=customer_pk)

    if request.method == 'POST':
        form = CustomerAlertForm(request.POST)
        if form.is_valid():
            alert = form.save(commit=False)
            alert.customer = customer
            alert.save()
            messages.success(request, 'ההתראה נוספה בהצלחה!')
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerAlertForm()

    return render(request, 'inventory/add_customer_alert.html', {
        'form': form, 'customer': customer
    })

def generate_invoice(request, sale_pk):
    """הפקת חשבונית מס רשמית לפי חוקי המס בישראל"""
    sale = get_object_or_404(Sale, pk=sale_pk)

    # קבלת תבנית ברירת מחדל
    template = InvoiceTemplate.objects.filter(is_default=True).first()
    if not template:
        template = InvoiceTemplate.objects.first()

    context = {
        'sale': sale,
        'template': template,
    }
    return render(request, 'inventory/tax_invoice.html', context)

def invoice_templates(request):
    """ניהול תבניות חשבוניות"""
    templates = InvoiceTemplate.objects.all()
    return render(request, 'inventory/invoice_templates.html', {'templates': templates})

def add_invoice_template(request):
    """הוספת תבנית חשבונית"""
    if request.method == 'POST':
        form = InvoiceTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'התבנית נוספה בהצלחה!')
            return redirect('invoice_templates')
    else:
        form = InvoiceTemplateForm()

    return render(request, 'inventory/add_invoice_template.html', {'form': form})

def customer_reports(request):
    """דוחות לקוחות"""
    # סטטיסטיקות כלליות
    total_customers = Customer.objects.count()
    active_customers = Customer.objects.filter(is_active=True).count()
    vip_customers = Customer.objects.filter(is_vip=True).count()

    # לקוחות לפי סוג
    customers_by_type = Customer.objects.values('customer_type').annotate(
        count=Count('id')
    ).order_by('-count')

    # לקוחות לפי עיר
    customers_by_city = Customer.objects.values('city').annotate(
        count=Count('id')
    ).order_by('-count')[:20]

    # לקוחות עם הרכישות הגבוהות ביותר (על בסיס מכירות)
    top_customers = Customer.objects.annotate(
        purchase_count=Count('sale'),
        total_spent=Sum('sale__total_amount')
    ).filter(
        purchase_count__gt=0
    ).order_by('-total_spent')[:20]

    # לקוחות לא פעילים
    inactive_customers = Customer.objects.filter(
        is_active=False
    ).order_by('-created_at')

    # לקוחות ללא רכישות
    customers_without_purchases = Customer.objects.annotate(
        purchase_count=Count('sale')
    ).filter(
        purchase_count=0
    ).order_by('-created_at')

    # המרת נתונים ל-JSON עבור הגרפים
    import json
    customers_by_type_json = json.dumps(list(customers_by_type))
    customers_by_city_json = json.dumps(list(customers_by_city))

    context = {
        'total_customers': total_customers,
        'active_customers': active_customers,
        'vip_customers': vip_customers,
        'customers_by_type': customers_by_type_json,
        'customers_by_city': customers_by_city_json,
        'top_customers': top_customers,
        'inactive_customers': inactive_customers,
        'customers_without_purchases': customers_without_purchases,
    }
    return render(request, 'inventory/customer_reports.html', context)
