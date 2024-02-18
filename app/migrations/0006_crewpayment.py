# Generated by Django 5.0 on 2024-01-08 06:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_ship_crew'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrewPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crew', models.PositiveIntegerField(blank=True, null=True)),
                ('payment_date', models.DateField()),
                ('amount_crew', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('ship_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ship')),
            ],
            options={
                'db_table': 'crew_payment',
            },
        ),
    ]
