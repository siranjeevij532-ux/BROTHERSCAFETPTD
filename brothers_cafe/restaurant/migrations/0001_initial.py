from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('icon', models.CharField(blank=True, help_text='Emoji icon e.g. \U0001f355', max_length=50)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['order', 'name'], 'verbose_name_plural': 'Categories'},
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='e.g. Festival Offer, Weekend Special', max_length=100)),
                ('percent', models.DecimalField(decimal_places=2, max_digits=5)),
                ('is_active', models.BooleanField(default=True)),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={'ordering': ['-is_active', 'name']},
        ),
        migrations.CreateModel(
            name='ShopSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(default='Brothers Cafe', max_length=200)),
                ('location', models.CharField(default='Tirupattur', max_length=200)),
                ('gstin', models.CharField(default='23278537256752', max_length=50)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True)),
                ('address', models.TextField(blank=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='shop/')),
                ('upi_qr_code', models.ImageField(blank=True, help_text='Upload QR code image for online payments', null=True, upload_to='qr_codes/')),
                ('upi_id', models.CharField(blank=True, help_text='e.g. brotherscafe@upi', max_length=100)),
                ('default_discount_percent', models.DecimalField(decimal_places=2, default=0, help_text='Default discount % shown on bills', max_digits=5)),
            ],
            options={'verbose_name': 'Shop Settings', 'verbose_name_plural': 'Shop Settings'},
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(unique=True)),
                ('name', models.CharField(help_text='e.g. Table 1, VIP Table', max_length=50)),
                ('capacity', models.PositiveIntegerField(default=4)),
                ('status', models.CharField(choices=[('available', 'Available'), ('occupied', 'Occupied'), ('reserved', 'Reserved')], default='available', max_length=20)),
                ('description', models.TextField(blank=True, help_text="Optional: location description like 'Near window'")),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['number']},
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='menu_images/')),
                ('item_type', models.CharField(choices=[('veg', 'Vegetarian'), ('nonveg', 'Non-Vegetarian'), ('vegan', 'Vegan'), ('beverage', 'Beverage')], default='veg', max_length=20)),
                ('is_available', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('preparation_time', models.PositiveIntegerField(default=15, help_text='Minutes')),
                ('order', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='restaurant.category')),
            ],
            options={'ordering': ['order', 'name']},
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_phone', models.CharField(max_length=15)),
                ('special_instructions', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('preparing', 'Preparing'), ('ready', 'Ready'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('payment_status', models.CharField(choices=[('unpaid', 'Unpaid'), ('online_pending', 'Online Payment Pending'), ('paid_online', 'Paid Online'), ('paid_offline', 'Paid Offline')], default='unpaid', max_length=20)),
                ('payment_method', models.CharField(blank=True, max_length=20)),
                ('order_type', models.CharField(choices=[('dine_in', 'Dine In'), ('takeaway', 'Takeaway')], default='dine_in', max_length=20)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('discount_percent', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('discount_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('order_number', models.CharField(blank=True, max_length=20, unique=True)),
                ('staff_notified', models.BooleanField(default=False)),
                ('table', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='restaurant.table')),
                ('parent_order', models.ForeignKey(blank=True, help_text='If this is a reorder, points to the original order', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reorders', to='restaurant.order')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('notes', models.TextField(blank=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='restaurant.order')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.menuitem')),
            ],
        ),
    ]
