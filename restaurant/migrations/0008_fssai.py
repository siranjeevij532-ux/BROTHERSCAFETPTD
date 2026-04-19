from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0007_order_parcel_charge'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopsettings',
            name='fssai_number',
            field=models.CharField(blank=True, default='', help_text='FSSAI License Number (Food Safety)', max_length=50),
        ),
        migrations.AlterField(
            model_name='shopsettings',
            name='gstin',
            field=models.CharField(blank=True, default='', help_text='GSTIN number', max_length=50),
        ),
    ]
