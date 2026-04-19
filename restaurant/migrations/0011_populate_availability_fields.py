# Data migration to populate new availability fields from old is_available field

from django.db import migrations


def populate_new_availability_fields(apps, schema_editor):
    """
    Populate is_available_dine_in and is_available_takeaway from the old is_available field.
    If an item was available (is_available=True), it will be available for both dine-in and takeaway.
    """
    MenuItem = apps.get_model('restaurant', 'MenuItem')
    for item in MenuItem.objects.all():
        item.is_available_dine_in = item.is_available
        item.is_available_takeaway = item.is_available
        item.save()


def reverse_populate(apps, schema_editor):
    """Reverse: not needed as we're keeping the old field"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0010_menuitem_availability_split'),
    ]

    operations = [
        migrations.RunPython(populate_new_availability_fields, reverse_populate),
    ]
