from django.db import models
from django.utils import timezone
import json


class ShopSettings(models.Model):
    shop_name = models.CharField(max_length=200, default="Brothers Cafe")
    location = models.CharField(max_length=200, default="Tirupattur")
    gstin = models.CharField(max_length=50, default="", blank=True, help_text='GSTIN number')
    fssai_number = models.CharField(max_length=50, default="", blank=True, help_text='FSSAI License Number (Food Safety)')
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    logo = models.ImageField(upload_to='shop/', blank=True, null=True)
    upi_qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True, 
                                     help_text="Upload QR code image for online payments")
    upi_id = models.CharField(max_length=100, blank=True, help_text="e.g. brotherscafe@upi")
    default_discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                                    help_text="Default discount % shown on bills")
    default_parcel_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0,
                                                 help_text="Default parcel charge per item for takeaway orders (overridden by item-level charge)")
    class Meta:
        verbose_name = "Shop Settings"
        verbose_name_plural = "Shop Settings"

    def __str__(self):
        return self.shop_name


class Table(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
    ]
    number = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=50, help_text="e.g. Table 1, VIP Table")
    capacity = models.PositiveIntegerField(default=4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    description = models.TextField(blank=True, help_text="Optional: location description like 'Near window'")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"{self.name} (#{self.number})"

    @property
    def current_order(self):
        return self.orders.filter(status__in=['pending', 'accepted', 'preparing', 'ready']).first()


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Emoji icon e.g. 🍕")
    image = models.ImageField(upload_to='category_images/', blank=True, null=True, help_text='Category banner image shown on menu page')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    TYPE_CHOICES = [
        ('veg', 'Vegetarian'),
        ('nonveg', 'Non-Vegetarian'),
        ('vegan', 'Vegan'),
        ('beverage', 'Beverage'),
    ]
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    item_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='veg')
    is_available = models.BooleanField(default=True, help_text='(Deprecated: use Dine In Active / Takeaway Active below)')
    is_available_dine_in = models.BooleanField(default=True, help_text='Item available for dine-in orders')
    is_available_takeaway = models.BooleanField(default=True, help_text='Item available for takeaway orders')
    is_featured = models.BooleanField(default=False)
    preparation_time = models.PositiveIntegerField(default=15, help_text="Minutes")
    order = models.PositiveIntegerField(default=0)
    parcel_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0,
                                          help_text='Extra charge for takeaway parcel packaging')

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - ₹{self.price}"

    def is_available_for_order_type(self, order_type):
        """Check if item is available for the given order type ('dine_in' or 'takeaway')"""
        if order_type == 'takeaway':
            return self.is_available_takeaway
        else:  # dine_in
            return self.is_available_dine_in


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_STATUS = [
        ('unpaid', 'Unpaid'),
        ('online_pending', 'Online Payment Pending'),
        ('paid_online', 'Paid Online'),
        ('paid_offline', 'Paid Offline'),
    ]

    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, related_name='orders')
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    special_instructions = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    payment_method = models.CharField(max_length=20, blank=True)  # 'online' or 'offline'
    order_type = models.CharField(max_length=20, default='dine_in',
        choices=[('dine_in', 'Dine In'), ('takeaway', 'Takeaway')])
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    parcel_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Total parcel charge for takeaway orders')
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    staff_notified = models.BooleanField(default=False)
    parent_order = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='reorders', help_text='If this is a reorder, points to the original order')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_number} - {self.customer_name} - {self.table}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            import random
            self.order_number = f"BC{timezone.now().strftime('%Y%m%d')}{random.randint(1000,9999)}"
        # Recalculate totals only if NOT called right after an explicit .update()
        # Skip_recalc kwarg lets views bypass this when they have already called calculate_totals()
        if self.pk and not kwargs.pop('skip_recalc', False):
            self.calculate_totals()
        super().save(*args, **kwargs)
        # Update table status
        if self.status in ['pending', 'accepted', 'preparing', 'ready']:
            if self.table:
                Table.objects.filter(pk=self.table.pk).update(status='occupied')
        elif self.status in ['completed', 'cancelled']:
            if self.table:
                # Only free if no other active orders
                active = Order.objects.filter(
                    table=self.table,
                    status__in=['pending', 'accepted', 'preparing', 'ready']
                ).exclude(pk=self.pk).exists()
                if not active:
                    Table.objects.filter(pk=self.table.pk).update(status='available')

    def calculate_totals(self):
        from decimal import Decimal, ROUND_HALF_UP
        items = list(self.items.all())
        self.subtotal = sum(item.total_price for item in items)
        if self.subtotal and self.discount_percent:
            self.discount_amount = (self.subtotal * self.discount_percent / 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            self.discount_amount = Decimal('0.00')
        self.total_amount = self.subtotal - self.discount_amount


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"

    @property
    def total_price(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.menu_item.price
        super().save(*args, **kwargs)


class Discount(models.Model):
    name = models.CharField(max_length=100, help_text="e.g. Festival Offer, Weekend Special")
    percent = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.percent}%"

    class Meta:
        ordering = ['-is_active', 'name']


class CustomerProfile(models.Model):
    """Customer identified by phone number — created on first login via QR scan."""
    name          = models.CharField(max_length=100)
    phone         = models.CharField(max_length=15, unique=True, db_index=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    last_visit    = models.DateTimeField(auto_now=True)
    visit_count   = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['-last_visit']
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.name} ({self.phone})"

    @property
    def total_orders(self):
        return Order.objects.filter(customer_phone=self.phone, parent_order__isnull=True).count()

    @property
    def total_spent(self):
        from decimal import Decimal
        from django.db.models import Sum
        result = Order.objects.filter(
            customer_phone=self.phone,
            status='completed',
            parent_order__isnull=True
        ).aggregate(total=Sum('total_amount'))['total']
        return result or Decimal('0')


class Combo(models.Model):
    """Staff-defined combo meals shown on the categories page."""
    name        = models.CharField(max_length=200)
    description = models.TextField(blank=True, help_text="Short description shown to customers")
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    image       = models.ImageField(upload_to='combo_images/', blank=True, null=True)
    icon        = models.CharField(max_length=50, blank=True, default='🎁', help_text="Emoji icon e.g. 🎁")
    is_active   = models.BooleanField(default=True)
    order       = models.PositiveIntegerField(default=0, help_text="Display order")
    items       = models.ManyToManyField(MenuItem, through='ComboItem', related_name='combos')

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Combo"
        verbose_name_plural = "Combos"

    def __str__(self):
        return f"{self.name} — ₹{self.price}"

    @property
    def item_count(self):
        return self.combo_items.count()


class ComboItem(models.Model):
    """Through table: links a MenuItem to a Combo with quantity."""
    combo     = models.ForeignKey(Combo, on_delete=models.CASCADE, related_name='combo_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity  = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['menu_item__name']
        verbose_name = "Combo Item"
        verbose_name_plural = "Combo Items"

    def __str__(self):
        return f"{self.quantity}× {self.menu_item.name}"


class PosDraft(models.Model):
    """POS saved draft orders - stored in DB, exportable to Excel."""
    draft_number  = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=100, blank=True, default='Walk-in')
    customer_phone= models.CharField(max_length=15,  blank=True, default='')
    table_name    = models.CharField(max_length=50,  blank=True, default='Takeaway')
    items_json    = models.TextField(help_text='JSON list of items')
    subtotal      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_pct  = models.DecimalField(max_digits=5,  decimal_places=2, default=0)
    total_amount  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    note          = models.TextField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    is_deleted    = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.draft_number} - {self.table_name} - ₹{self.total_amount}"
