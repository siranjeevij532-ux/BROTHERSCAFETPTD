import os
from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django.utils import timezone
from .models import ShopSettings, Table, Category, MenuItem, Order, OrderItem, Discount, CustomerProfile, Combo, ComboItem
import openpyxl
from django.http import HttpResponse
from io import BytesIO


@admin.register(ShopSettings)
class ShopSettingsAdmin(admin.ModelAdmin):
    list_display = ['shop_name', 'location', 'gstin', 'fssai_number', 'phone', 'default_discount_percent', 'default_parcel_charge']
    fieldsets = (
        ('Shop Info', {'fields': ('shop_name', 'location', 'address', 'phone', 'email', 'gstin', 'fssai_number', 'logo')}),

        ('Payment', {'fields': ('upi_id', 'upi_qr_code')}),
        ('Billing & Parcel', {'fields': ('default_discount_percent', 'default_parcel_charge'), 'description': 'default_parcel_charge: Added per item on all takeaway orders. Set 0 to disable. Override per item in Menu Items.'}),

    )

    def has_add_permission(self, request):
        return not ShopSettings.objects.exists()


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['number', 'name', 'capacity', 'colored_status', 'description', 'is_active']
    list_filter = ['status', 'is_active']
    list_editable = ['is_active']
    ordering = ['number']

    def colored_status(self, obj):
        colors = {'available': '#27ae60', 'occupied': '#e74c3c', 'reserved': '#f39c12'}
        return format_html(
            '<span style="background:{bg};color:white;padding:3px 10px;border-radius:12px;font-weight:bold">{label}</span>',
            bg=colors.get(obj.status, '#999'),
            label=obj.get_status_display()
        )
    colored_status.short_description = 'Status'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'icon', 'order', 'is_active', 'item_count']
    list_editable = ['order', 'is_active']
    ordering = ['order']
    fields = ['name', 'description', 'icon', 'image', 'order', 'is_active']

    def image_preview(self, obj):
        if obj.image and getattr(obj.image, 'name', None):
            try:
                if os.path.exists(obj.image.path):
                    return format_html(
                        '<img src="{}" style="height:50px;width:80px;object-fit:cover;border-radius:8px"/>',
                        obj.image.url
                    )
            except Exception:
                pass
        return mark_safe('<span style="color:#aaa;font-size:11px">No Image</span>')
    image_preview.short_description = 'Image'

    def item_count(self, obj):
        return obj.items.filter(is_available_dine_in=True).count()
    item_count.short_description = 'Active Items'


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'category', 'price', 'availability_status', 'parcel_charge', 'item_type', 'is_featured', 'order']
    list_filter = ['category', 'item_type', 'is_available_dine_in', 'is_available_takeaway', 'is_featured']
    list_editable = ['price', 'parcel_charge', 'is_featured', 'order']
    search_fields = ['name', 'description']
    ordering = ['category', 'order']
    fieldsets = (
        ('Basic Info', {'fields': ('category', 'name', 'description', 'price', 'item_type', 'image')}),
        ('Availability', {'fields': ('is_available_dine_in', 'is_available_takeaway'), 
                         'description': 'Check "Dine In Active" for dine-in orders or "Takeaway Active" for takeaway orders'}),
        ('Display & Pricing', {'fields': ('is_featured', 'order', 'preparation_time', 'parcel_charge')}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{url}" style="height:50px;width:50px;object-fit:cover;border-radius:8px"/>',
                url=obj.image.url
            )
        return mark_safe('<span style="color:#aaa">No Image</span>')
    image_preview.short_description = 'Image'

    def availability_status(self, obj):
        """Show which order types this item is available for"""
        statuses = []
        if obj.is_available_dine_in:
            statuses.append('🍽️ Dine')
        if obj.is_available_takeaway:
            statuses.append('🎁 Away')
        if not statuses:
            return format_html('<span style="color:#e74c3c;font-weight:bold">Not Available</span>')
        return format_html('<span style="color:#27ae60">{}</span>', ' | '.join(statuses))
    availability_status.short_description = 'Available For'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['unit_price', 'total_price_display']
    
    def total_price_display(self, obj):
        if obj.pk:
            return f"₹{obj.total_price}"
        return "-"
    total_price_display.short_description = "Total"


def export_orders_excel(modeladmin, request, queryset):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Orders"
    headers = ['Order #', 'Date', 'Customer', 'Phone', 'Table', 'Items', 
               'Subtotal', 'Discount%', 'Discount Amt', 'Total', 'Status', 'Payment']
    ws.append(headers)
    for order in queryset:
        items_str = ", ".join([f"{i.quantity}x {i.menu_item.name}" for i in order.items.all()])
        ws.append([
            order.order_number,
            order.created_at.strftime('%Y-%m-%d %H:%M'),
            order.customer_name,
            order.customer_phone,
            str(order.table),
            items_str,
            float(order.subtotal),
            float(order.discount_percent),
            float(order.discount_amount),
            float(order.total_amount),
            order.get_status_display(),
            order.get_payment_status_display(),
        ])
    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)
    response = HttpResponse(buf.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="orders_export.xlsx"'
    return response

export_orders_excel.short_description = "📊 Export Selected Orders to Excel"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'table', 'colored_status', 
                    'colored_payment', 'subtotal', 'discount_display', 'total_amount', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'customer_name', 'customer_phone']
    inlines = [OrderItemInline]
    readonly_fields = ['order_number', 'subtotal', 'discount_amount', 'total_amount', 'created_at']
    actions = [export_orders_excel]
    ordering = ['-created_at']
    fieldsets = (
        ('Order Info', {'fields': ('order_number', 'table', 'customer_name', 'customer_phone', 'special_instructions')}),
        ('Status', {'fields': ('status', 'payment_status', 'payment_method')}),
        ('Billing', {'fields': ('subtotal', 'discount_percent', 'discount_amount', 'total_amount')}),
        ('Timestamps', {'fields': ('created_at',)}),
    )

    def colored_status(self, obj):
        colors = {
            'pending': '#e67e22', 'accepted': '#3498db',
            'preparing': '#9b59b6', 'ready': '#27ae60',
            'completed': '#2c3e50', 'cancelled': '#e74c3c'
        }
        return format_html(
            '<span style="background:{bg};color:white;padding:3px 10px;border-radius:12px;font-size:11px">{label}</span>',
            bg=colors.get(obj.status, '#999'), label=obj.get_status_display()
        )
    colored_status.short_description = 'Status'

    def colored_payment(self, obj):
        colors = {'unpaid': '#e74c3c', 'online_pending': '#f39c12', 
                  'paid_online': '#27ae60', 'paid_offline': '#27ae60'}
        return format_html(
            '<span style="background:{bg};color:white;padding:3px 8px;border-radius:12px;font-size:11px">{label}</span>',
            bg=colors.get(obj.payment_status, '#999'), label=obj.get_payment_status_display()
        )
    colored_payment.short_description = 'Payment'

    def discount_display(self, obj):
        if obj.discount_percent > 0:
            return format_html('<span style="color:#27ae60">{pct}% off</span>', pct=obj.discount_percent)
        return "-"
    discount_display.short_description = 'Discount'


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'percent', 'is_active', 'valid_from', 'valid_to', 'description']
    list_editable = ['is_active', 'percent']
    list_filter = ['is_active']


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display  = ['name', 'phone', 'visit_count', 'total_orders_display',
                     'total_spent_display', 'last_visit', 'created_at']
    search_fields = ['name', 'phone']
    readonly_fields = ['created_at', 'last_visit', 'visit_count']
    ordering = ['-last_visit']

    def total_orders_display(self, obj):
        return obj.total_orders
    total_orders_display.short_description = 'Orders'

    def total_spent_display(self, obj):
        return format_html('<strong style="color:#27ae60">₹{}</strong>', obj.total_spent)
    total_spent_display.short_description = 'Total Spent'


class ComboItemInline(admin.TabularInline):
    model = ComboItem
    extra = 1
    autocomplete_fields = ['menu_item']
    fields = ['menu_item', 'quantity', 'item_image_preview', 'item_price']
    readonly_fields = ['item_image_preview', 'item_price']

    def item_image_preview(self, obj):
        if obj.pk and obj.menu_item_id:
            try:
                mi = obj.menu_item
                if mi.image:
                    return format_html('<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:6px"/>', mi.image.url)
            except Exception:
                pass
        return mark_safe('<span style="color:#aaa;font-size:11px">No image</span>')
    item_image_preview.short_description = 'Image'

    def item_price(self, obj):
        if obj.pk and obj.menu_item_id:
            try:
                return f'₹{obj.menu_item.price}'
            except Exception:
                pass
        return '-'
    item_price.short_description = 'Unit Price'


@admin.register(Combo)
class ComboAdmin(admin.ModelAdmin):
    list_display = ['combo_image_preview', 'name', 'price', 'item_count_display', 'is_active', 'order']
    list_editable = ['price', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    inlines = [ComboItemInline]
    ordering = ['order', 'name']
    fieldsets = (
        ('Combo Details', {'fields': ('name', 'description', 'icon', 'price', 'image', 'is_active', 'order')}),
    )

    def combo_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;width:50px;object-fit:cover;border-radius:8px"/>', obj.image.url)
        return format_html('<span style="font-size:28px">{}</span>', obj.icon or '🎁')
    combo_image_preview.short_description = 'Image'

    def item_count_display(self, obj):
        count = obj.combo_items.count()
        return format_html('<span style="background:#e8f4ff;color:#3498db;padding:2px 8px;border-radius:10px;font-weight:700">{} items</span>', count)
    item_count_display.short_description = 'Items'
