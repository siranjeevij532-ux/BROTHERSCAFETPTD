from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_customerprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Combo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, help_text='Short description shown to customers')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='combo_images/')),
                ('icon', models.CharField(blank=True, default='\U0001f381', help_text='Emoji icon', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0, help_text='Display order')),
            ],
            options={
                'verbose_name': 'Combo',
                'verbose_name_plural': 'Combos',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='ComboItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('combo', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='combo_items',
                    to='restaurant.combo',
                )),
                ('menu_item', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='restaurant.menuitem',
                )),
            ],
            options={
                'verbose_name': 'Combo Item',
                'verbose_name_plural': 'Combo Items',
                'ordering': ['menu_item__name'],
            },
        ),
        migrations.AddField(
            model_name='combo',
            name='items',
            field=models.ManyToManyField(
                related_name='combos',
                through='restaurant.ComboItem',
                to='restaurant.menuitem',
            ),
        ),
    ]
