from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='parcel_charge',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Total parcel charge for takeaway orders', max_digits=10),
        ),
    ]
