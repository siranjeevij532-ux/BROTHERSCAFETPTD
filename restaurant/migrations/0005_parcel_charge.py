from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_alter_combo_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='parcel_charge',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Extra charge for takeaway parcel packaging', max_digits=6),
        ),
        migrations.AddField(
            model_name='shopsettings',
            name='default_parcel_charge',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Default parcel charge per item for takeaway orders (overridden by item-level charge)', max_digits=6),
        ),
    ]
