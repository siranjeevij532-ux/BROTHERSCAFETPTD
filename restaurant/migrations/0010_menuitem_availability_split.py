# Generated migration for splitting is_available into dine_in and takeaway availability

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0009_posdraft'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='is_available_dine_in',
            field=models.BooleanField(default=True, help_text='Item available for dine-in orders'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='is_available_takeaway',
            field=models.BooleanField(default=True, help_text='Item available for takeaway orders'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='is_available',
            field=models.BooleanField(default=True, help_text='(Deprecated: use Dine In Active / Takeaway Active below)'),
        ),
    ]
