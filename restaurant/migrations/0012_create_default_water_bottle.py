from django.db import migrations


def create_default_water_bottle(apps, schema_editor):
    Category = apps.get_model('restaurant', 'Category')
    MenuItem = apps.get_model('restaurant', 'MenuItem')

    category, created = Category.objects.get_or_create(
        name='Beverages',
        defaults={
            'description': 'Drinks and refreshments',
            'icon': '🥤',
            'order': 0,
            'is_active': True,
        }
    )

    if not MenuItem.objects.filter(name__iexact='Water Bottle').exists():
        MenuItem.objects.create(
            category=category,
            name='Water Bottle',
            description='Pure drinking water',
            price='10.00',
            item_type='beverage',
            is_available_dine_in=True,
            is_available_takeaway=True,
            is_featured=False,
            preparation_time=1,
            order=999,
            parcel_charge=0,
        )


def remove_default_water_bottle(apps, schema_editor):
    MenuItem = apps.get_model('restaurant', 'MenuItem')
    Category = apps.get_model('restaurant', 'Category')

    MenuItem.objects.filter(name__iexact='Water Bottle').delete()
    Category.objects.filter(name__iexact='Beverages').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0011_populate_availability_fields'),
    ]

    operations = [
        migrations.RunPython(create_default_water_bottle, reverse_code=remove_default_water_bottle),
    ]
