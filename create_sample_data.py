from inventory.models import Category, Supplier, Location, Product

# יצירת קטגוריות
electronics = Category.objects.create(name='אלקטרוניקה', description='מוצרי אלקטרוניקה')
clothing = Category.objects.create(name='ביגוד', description='בגדים ואביזרים')
food = Category.objects.create(name='מזון', description='מוצרי מזון')

# יצירת ספקים
supplier1 = Supplier.objects.create(
    name='ספק אלקטרוניקה',
    contact_person='יוסי כהן',
    email='yossi@electronics.co.il',
    phone='03-1234567',
    address='רחוב התעשייה 1, תל אביב'
)

supplier2 = Supplier.objects.create(
    name='ספק ביגוד',
    contact_person='שרה לוי',
    email='sara@clothing.co.il',
    phone='04-9876543',
    address='רחוב האופנה 5, חיפה'
)

# יצירת מיקומים
location1 = Location.objects.create(
    name='מחסן ראשי',
    address='רחוב התעשייה 1, תל אביב'
)

location2 = Location.objects.create(
    name='מחסן משני',
    address='רחוב האופנה 5, חיפה'
)

# יצירת מוצרים לדוגמה
Product.objects.create(
    name='מחשב נייד',
    description='מחשב נייד 15 אינץ',
    category=electronics,
    supplier=supplier1,
    location=location1,
    quantity=10,
    min_quantity=5,
    max_quantity=50,
    cost_price=2000,
    selling_price=2500,
    barcode='1234567890123',
    status='active'
)

Product.objects.create(
    name='חולצת טי שירט',
    description='חולצת טי שירט כותנה',
    category=clothing,
    supplier=supplier2,
    location=location2,
    quantity=3,
    min_quantity=10,
    max_quantity=100,
    cost_price=20,
    selling_price=35,
    barcode='9876543210987',
    status='active'
)

Product.objects.create(
    name='סמארטפון',
    description='סמארטפון אנדרואיד',
    category=electronics,
    supplier=supplier1,
    location=location1,
    quantity=0,
    min_quantity=3,
    max_quantity=20,
    cost_price=800,
    selling_price=1000,
    barcode='5555555555555',
    status='active'
)

print('נתונים לדוגמה נוצרו בהצלחה!')
