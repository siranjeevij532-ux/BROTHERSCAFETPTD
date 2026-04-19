import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brothers_cafe.settings')
django.setup()

from decimal import Decimal
from restaurant.models import ShopSettings, Table, Category, MenuItem, Combo, ComboItem

print("Seeding Brothers Cafe...")

ShopSettings.objects.all().delete()
ShopSettings.objects.create(
    shop_name="Brothers Cafe", location="Tirupattur",
    address="Tirupattur, Tamil Nadu", phone="",
    gstin="", fssai_number="",
    default_discount_percent=Decimal("0"),
    default_parcel_charge=Decimal("0"),
)
print("  Shop Settings created")

Table.objects.all().delete()
for n in range(1, 6):
    Table.objects.create(number=n, name=f"Table {n}", capacity=4, is_active=True)
print("  5 Tables created")

Category.objects.all().delete()
MenuItem.objects.all().delete()

def cat(name, icon, order):
    return Category.objects.create(name=name, icon=icon, order=order, is_active=True)

def item(c, name, price, t='veg', o=0):
    return MenuItem.objects.create(
        category=c, name=name, price=Decimal(str(price)),
        item_type=t, is_available=True, order=o)

# HOT DRINKS
c = cat("Hot Drinks","☕",1)
item(c,"Coffee",25,'beverage',0); item(c,"Boost",30,'beverage',1)
item(c,"Horlicks",30,'beverage',2); item(c,"Chocolate Coffee",85,'beverage',3)

# COOL DRINKS
c = cat("Cool Drinks","🥤",2)
item(c,"Cold Coffee",85,'beverage',0); item(c,"Rose Milk",45,'beverage',1)
item(c,"Rose Milk with Ice Cream",65,'beverage',2)

# MILK SHAKES
c = cat("Milk Shakes","🥛",3)
shakes=[("Vanilla",80,110),("Strawberry",85,115),("Chocolate",95,125),
        ("Butterscotch",90,120),("Mango",90,120),("Pista",100,135),
        ("Oreo",105,135),("Kit-Kat",105,135),("Boost",100,130),
        ("Horlicks",100,130),("Brownie",120,160),("Dry Fruits",130,170)]
for i,(n,mini,reg) in enumerate(shakes):
    item(c,f"{n} Milkshake (Mini)",mini,'beverage',i*2)
    item(c,f"{n} Milkshake (Regular)",reg,'beverage',i*2+1)

# MOJITO
c = cat("Mojito","🍹",4)
mojitos=[("Virgin",60,90),("Strawberry",65,95),("Blue Curacao",75,105),("Green Apple",75,105)]
for i,(n,mini,reg) in enumerate(mojitos):
    item(c,f"{n} Mojito (Mini)",mini,'beverage',i*2)
    item(c,f"{n} Mojito (Regular)",reg,'beverage',i*2+1)

# ICE CREAM
c = cat("Ice Cream","🍨",5)
for i,(n,p) in enumerate([("Vanilla",60),("Strawberry",65),("Mango",70),
                           ("Chocolate",80),("Butterscotch",75),("Pista",85)]):
    item(c,f"{n} Ice Cream",p,'veg',i)

# SUNDAE
c = cat("Sundae","🍧",6)
for i,(n,p) in enumerate([("Fruit Sundae",165),("Cookies Monster Sundae",150),
                           ("Brownie Sundae",160),("Dry Fruit Sundae",170)]):
    item(c,n,p,'veg',i)

# FALOODA
c = cat("Falooda","🍓",7)
for i,(n,p) in enumerate([("Classic Falooda",120),("Dry Fruit Falooda",150),
                           ("Rayal Falooda",160),("Strawberry Falooda",145),("Mango Falooda",140)]):
    item(c,n,p,'veg',i)

# BROWNIE
c = cat("Brownie","🍫",8)
for i,(n,p) in enumerate([("Dark Choco Brownie",70),("Triple Choco Brownie",105),
                           ("Brownie with Ice Cream",100),("Sizzling Brownie Plate",120)]):
    item(c,n,p,'veg',i)

# WAFFLES
c = cat("Waffles","🧇",9)
for i,(n,p) in enumerate([("Milk Choco Waffle",80),("White Choco Waffle",85),
    ("Dark Choco Waffle",90),("Triple Choco Waffle",100),("White & Dark Waffle",90),
    ("Milk & White Waffle",85),("Dark & Milk Waffle",90),("Cookies & Cream Waffle",115),
    ("Kit-Kat Crunch Waffle",110),("Oreo Fantasy Waffle",110),("Naughty Nutella Waffle",120),
    ("Red Velvet Waffle",115),("Brownie Waffle White",110),("Brownie Waffle Dark",115),
    ("Cotton Candy Waffle",115),("Lotus Biscoff Waffle",135)]):
    item(c,n,p,'veg',i)

# BUN
c = cat("Bun","🍞",10)
for i,(n,p) in enumerate([("Bun Butter Jam",30),("Dark Choco Bun",45),("Milk Choco Bun",40),
    ("White Choco Bun",45),("Triple Choco Bun",55),("Cookies and Cream Bun",65),("Cotton Candy Bun",60)]):
    item(c,n,p,'veg',i)

# BREAD OMELETTE
c = cat("Bread Omelette","🍳",11)
item(c,"Bread Omelette",50,'veg',0); item(c,"Cheese Bread Omelette",70,'veg',1)
item(c,"Chicken Bread Omelette",95,'nonveg',2); item(c,"Cheese Chicken Bread Omelette",115,'nonveg',3)

# SANDWICH
c = cat("Sandwich","🥪",12)
for i,(n,p,t) in enumerate([
    ("Veg Sandwich",60,'veg'),("Veg Cheese Sandwich",80,'veg'),
    ("Sweet Corn Sandwich",75,'veg'),("Sweet Corn Cheese Sandwich",95,'veg'),
    ("Chocolate Sandwich",80,'veg'),("Mushroom Sandwich",100,'veg'),
    ("Mushroom Cheese Sandwich",120,'veg'),("Paneer Sandwich",110,'veg'),
    ("Paneer Cheese Sandwich",130,'veg'),("Egg Sandwich",70,'veg'),
    ("Egg Cheese Sandwich",90,'veg'),("Chicken Sandwich",95,'nonveg'),
    ("Chicken Cheese Sandwich",115,'nonveg')]):
    item(c,n,p,t,i)

# MAGGI
c = cat("Maggi","🍜",13)
for i,(n,p,t) in enumerate([
    ("Plain Maggi",45,'veg'),("Plain Maggi Cheese",65,'veg'),
    ("Veg Maggi",55,'veg'),("Veg Maggi Cheese",75,'veg'),
    ("Peri Peri Maggi",60,'veg'),("Peri Peri Maggi Cheese",80,'veg'),
    ("Szechwan Maggi",85,'veg'),("Szechwan Maggi Cheese",105,'veg'),
    ("Sweet Corn Maggi",65,'veg'),("Sweet Corn Maggi Cheese",85,'veg'),
    ("Mushroom Maggi",85,'veg'),("Mushroom Maggi Cheese",105,'veg'),
    ("Egg Maggi",65,'veg'),("Egg Maggi Cheese",85,'veg'),
    ("Chicken Maggi",95,'nonveg'),("Chicken Maggi Cheese",115,'nonveg')]):
    item(c,n,p,t,i)

# PIZZA
c = cat("Pizza","🍕",14)
for i,(n,p,t) in enumerate([
    ("Margherita Pizza",145,'veg'),("Veg Pizza",160,'veg'),
    ("Sweet Corn Pizza",175,'veg'),("Mushroom Pizza",190,'veg'),
    ("Paneer Pizza",215,'veg'),("Chilli Paneer Pizza",225,'veg'),
    ("Mixed Pizza",235,'veg'),("Fried Chicken Pizza",210,'nonveg'),
    ("Pepper Chicken Pizza",220,'nonveg'),("Peri Peri Chicken Pizza",220,'nonveg')]):
    item(c,n,p,t,i)

# BURGER
c = cat("Burger","🍔",15)
for i,(n,p,t) in enumerate([
    ("Mini Chicken Burger (4 pc)",120,'nonveg'),("Chicken Zinger Burger",135,'nonveg'),
    ("Cheese Chicken Zinger Burger",155,'nonveg'),("No Bun Chicken Burger",185,'nonveg'),
    ("Cheese No Bun Burger",205,'nonveg')]):
    item(c,n,p,t,i)

# FRENCH FRIES
c = cat("French Fries","🍟",16)
for i,(n,p,t) in enumerate([("French Fries",80,'veg'),("Masala French Fries",90,'veg'),
    ("Peri Peri French Fries",100,'veg'),("Chicken Loaded Fries",145,'nonveg')]):
    item(c,n,p,t,i)

# FRIED CHICKEN
c = cat("Fried Chicken","🍗",17)
for i,(n,p,t) in enumerate([
    ("Hot & Crispy Chicken (2 pc)",115,'nonveg'),("Hot & Crispy Peri Peri (2 pc)",155,'nonveg'),
    ("Crispy Chicken Strips (3 pc)",135,'nonveg'),("Crispy Strips Peri Peri (3 pc)",145,'nonveg'),
    ("Chicken Hot Wings (3 pc)",110,'nonveg'),("Chicken Hot Wings Peri Peri (3 pc)",120,'nonveg'),
    ("Chicken Leg (1 pc)",95,'nonveg'),("Chicken Leg Peri Peri (1 pc)",105,'nonveg'),
    ("Chicken Popcorn",120,'nonveg'),("Chicken Popcorn Peri Peri",130,'nonveg')]):
    item(c,n,p,t,i)

# WRAP
c = cat("Wrap","🌯",18)
item(c,"Paneer Wrap",135,'veg',0); item(c,"Chicken Wrap",130,'nonveg',1)

# LAYS CHICKEN
c = cat("Lays Chicken","🥔",19)
item(c,"Lays Chicken (Mini)",60,'nonveg',0); item(c,"Lays Chicken (Regular)",100,'nonveg',1)

# EXTRAS
c = cat("Extras","➕",20)
item(c,"Coco Cola",30,'veg',0); item(c,"Dips & Toppings",10,'veg',1)

print(f"  {Category.objects.count()} categories, {MenuItem.objects.count()} menu items created")

# ── COMBOS ────────────────────────────────────────────────────────────────────
Combo.objects.all().delete()

def get(name):
    return MenuItem.objects.filter(name__icontains=name).first()

# Combo 1: Chicken Zinger Burger + French Fries + Coco Cola = 220
combo1 = Combo.objects.create(name="Combo 1 - Zinger Meal", price=Decimal("220"),
    description="Chicken Zinger Burger + French Fries + Coco Cola", icon="🍔", is_active=True, order=1)
for mi,qty in [(get("Chicken Zinger Burger"),1),(get("French Fries"),1),(get("Coco Cola"),1)]:
    if mi: ComboItem.objects.create(combo=combo1, menu_item=mi, quantity=qty)

# Combo 2: Chicken Pizza + French Fries + Coco Cola = 300
combo2 = Combo.objects.create(name="Combo 2 - Pizza Meal", price=Decimal("300"),
    description="Chicken Pizza + French Fries + Coco Cola", icon="🍕", is_active=True, order=2)
for mi,qty in [(get("Fried Chicken Pizza"),1),(get("French Fries"),1),(get("Coco Cola"),1)]:
    if mi: ComboItem.objects.create(combo=combo2, menu_item=mi, quantity=qty)

# All Chicken Box Meal = 190
combo3 = Combo.objects.create(name="All Chicken Box Meal", price=Decimal("190"),
    description="1 Hot & Crispy + 2 Peri Peri Strips + 1 Coco Cola", icon="🍗", is_active=True, order=3)
for mi,qty in [(get("Hot & Crispy Chicken (2 pc)"),1),(get("Crispy Strips Peri Peri"),1),(get("Coco Cola"),1)]:
    if mi: ComboItem.objects.create(combo=combo3, menu_item=mi, quantity=qty)

# Classic Zinger Box Meal = 310
combo4 = Combo.objects.create(name="Classic Zinger Box Meal", price=Decimal("310"),
    description="1 Chicken Zinger Burger + 2 Hot Wings + Regular Fries + 1 Coco Cola", icon="🍱", is_active=True, order=4)
for mi,qty in [(get("Chicken Zinger Burger"),1),(get("Chicken Hot Wings (3 pc)"),1),(get("French Fries"),1),(get("Coco Cola"),1)]:
    if mi: ComboItem.objects.create(combo=combo4, menu_item=mi, quantity=qty)

# All in One Bucket = 510
combo5 = Combo.objects.create(name="All in One Bucket", price=Decimal("510"),
    description="2 Wings + 2 Strips + 1 Hot & Crispy + 1 Leg + 2 Coco Cola", icon="🪣", is_active=True, order=5)
for mi,qty in [(get("Chicken Hot Wings (3 pc)"),1),(get("Crispy Chicken Strips (3 pc)"),1),
               (get("Hot & Crispy Chicken (2 pc)"),1),(get("Chicken Leg (1 pc)"),1),(get("Coco Cola"),2)]:
    if mi: ComboItem.objects.create(combo=combo5, menu_item=mi, quantity=qty)

print(f"  {Combo.objects.count()} combos created")
print()
print("Done! Visit /admin/ to add images and update shop details.")
print("Takeaway is built-in on the order page — no extra table needed.")
