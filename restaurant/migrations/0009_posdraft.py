from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0008_fssai'),
    ]

    operations = [
        migrations.CreateModel(
            name='PosDraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('draft_number', models.CharField(max_length=20, unique=True)),
                ('customer_name', models.CharField(blank=True, default='Walk-in', max_length=100)),
                ('customer_phone', models.CharField(blank=True, default='', max_length=15)),
                ('table_name', models.CharField(blank=True, default='Takeaway', max_length=50)),
                ('items_json', models.TextField(help_text='JSON list of items')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('discount_pct', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('note', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
