from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from restaurant.models import ShopSettings, Table, Category, MenuItem, Discount


class Command(BaseCommand):
    help = 'Seeds the database with sample data for Brothers Cafe'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding Brothers Cafe database...')

        # Shop Settings
        shop, _ = ShopSettings.objects.get_or_create(id=1, defaults={
            'shop_name': 'Brothers Cafe',
            'location': 'Tirupattur',
            'gstin': '23278537256752',
            'phone': '+91 98765 43210',
            'address': '123 Main Street, Tirupattur, Tamil Nadu - 635601',
            'upi_id': 'brotherscafe@upi',
            'default_discount_percent': 0,
        })
        self.stdout.write(self.style.SUCCESS('✅ Shop settings created'))

        # Tables (4 initial, more can be added via admin)
        tables_data = [
            (1, 'Window Table', 4, 'Near the window, great view'),
            (2, 'Corner Table', 2, 'Quiet corner, perfect for couples'),
            (3, 'Center Table', 6, 'Main hall, great for groups'),
            (4, 'Garden Table', 4, 'Near the garden area'),
        ]
        for num, name, cap, desc in tables_data:
            Table.objects.get_or_create(number=num, defaults={
                'name': name, 'capacity': cap, 'description': desc
            })
        self.stdout.write(self.style.SUCCESS('✅ 4 tables created'))

        # Categories (4)
        cats = [
            ('South Indian', '🍛', 1),
            ('Snacks & Starters', '🍟', 2),
            ('Beverages', '☕', 3),
            ('Desserts', '🍰', 4),
        ]
        cat_objs = {}
        for name, icon, order in cats:
            c, _ = Category.objects.get_or_create(name=name, defaults={'icon': icon, 'order': order})
            cat_objs[name] = c
        self.stdout.write(self.style.SUCCESS('✅ 4 categories created'))

        # Menu Items (30 items, ~7-8 per category)
        items = [
            # South Indian (8 items)
            ('South Indian', 'Idli (2 pcs)', 'Soft steamed rice cakes served with sambar and chutney', 40, 'veg', True),
            ('South Indian', 'Masala Dosa', 'Crispy dosa with spiced potato filling', 80, 'veg', True),
            ('South Indian', 'Plain Dosa', 'Classic thin crispy dosa', 60, 'veg', False),
            ('South Indian', 'Vada (2 pcs)', 'Crispy urad dal fritters with chutney', 50, 'veg', False),
            ('South Indian', 'Pongal', 'Creamy rice and lentil dish with ghee', 70, 'veg', True),
            ('South Indian', 'Uthappam', 'Thick rice pancake with vegetables', 75, 'veg', False),
            ('South Indian', 'Sambar Rice', 'Rice with flavorful sambar and papad', 90, 'veg', False),
            ('South Indian', 'Mini Meals', 'Full south Indian thali with rice, sambar, rasam, curries', 150, 'veg', True),
            # Snacks (8 items)
            ('Snacks & Starters', 'Samosa (2 pcs)', 'Crispy pastry with spiced potato filling', 30, 'veg', False),
            ('Snacks & Starters', 'Bajji Plate', 'Mixed vegetable fritters', 45, 'veg', True),
            ('Snacks & Starters', 'Bread Omelette', 'Egg omelette with toasted bread', 60, 'nonveg', True),
            ('Snacks & Starters', 'Chicken Sandwich', 'Grilled chicken with veggies in sandwich', 120, 'nonveg', True),
            ('Snacks & Starters', 'Veg Sandwich', 'Fresh vegetable sandwich', 70, 'veg', False),
            ('Snacks & Starters', 'French Fries', 'Crispy golden fries with ketchup', 80, 'veg', True),
            ('Snacks & Starters', 'Chicken Rolls', 'Spicy chicken wrapped in roti', 100, 'nonveg', False),
            ('Snacks & Starters', 'Paneer Tikka', 'Grilled paneer with spices', 130, 'veg', True),
            # Beverages (8 items)
            ('Beverages', 'Filter Coffee', 'Traditional south Indian filter coffee', 30, 'beverage', True),
            ('Beverages', 'Masala Chai', 'Spiced Indian tea', 25, 'beverage', True),
            ('Beverages', 'Cold Coffee', 'Chilled coffee with milk and ice cream', 80, 'beverage', True),
            ('Beverages', 'Mango Lassi', 'Refreshing mango yogurt drink', 70, 'beverage', True),
            ('Beverages', 'Fresh Lime Soda', 'Lime with soda, sweet or salted', 50, 'beverage', False),
            ('Beverages', 'Banana Milkshake', 'Thick banana milkshake', 80, 'beverage', False),
            ('Beverages', 'Buttermilk', 'Spiced traditional buttermilk', 30, 'beverage', False),
            ('Beverages', 'Watermelon Juice', 'Fresh seasonal fruit juice', 60, 'beverage', False),
            # Desserts (6 items)
            ('Desserts', 'Gulab Jamun', 'Soft milk solid balls in sugar syrup', 60, 'veg', True),
            ('Desserts', 'Ice Cream (2 scoops)', 'Vanilla / Chocolate / Strawberry', 80, 'veg', True),
            ('Desserts', 'Payasam', 'Sweet rice pudding with dry fruits', 70, 'veg', False),
            ('Desserts', 'Halwa', 'Semolina pudding with ghee and nuts', 60, 'veg', False),
            ('Desserts', 'Jalebi', 'Crispy sweet spirals in sugar syrup', 50, 'veg', True),
            ('Desserts', 'Banana Split', 'Banana with ice cream and chocolate sauce', 120, 'veg', False),
        ]

        order_counter = 1
        for cat_name, name, desc, price, itype, featured in items:
            MenuItem.objects.get_or_create(name=name, defaults={
                'category': cat_objs[cat_name],
                'description': desc,
                'price': price,
                'item_type': itype,
                'is_featured': featured,
                'preparation_time': 10 if 'beverage' in itype else 15,
                'order': order_counter,
            })
            order_counter += 1
        self.stdout.write(self.style.SUCCESS(f'✅ {len(items)} menu items created'))

        # Discounts
        discounts = [
            ('Weekend Special', 10, 'Enjoy 10% off every weekend!'),
            ('Festival Offer', 21, 'Special 21% festival discount'),
            ('Student Discount', 5, '5% off for students with ID'),
            ('Loyalty Offer', 15, '15% off for regular customers'),
        ]
        for name, pct, desc in discounts:
            Discount.objects.get_or_create(name=name, defaults={'percent': pct, 'description': desc, 'is_active': False})
        self.stdout.write(self.style.SUCCESS('✅ 4 discounts created'))

        # Admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@brotherscafe.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('✅ Admin user: admin / admin123'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Brothers Cafe setup complete!'))
        self.stdout.write('📱 Customer URL: http://localhost:8000/')
        self.stdout.write('👨‍🍳 Staff Portal: http://localhost:8000/staff/')
        self.stdout.write('⚙️  Admin Panel: http://localhost:8000/admin/')
        self.stdout.write('🔑 Admin login: admin / admin123')
