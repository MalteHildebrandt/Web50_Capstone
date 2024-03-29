# Generated by Django 3.1.6 on 2021-04-26 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drinx', '0009_auto_20210423_2010'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description_short', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='images/articles')),
                ('content_qty', models.DecimalField(decimal_places=2, max_digits=3)),
                ('package_qty', models.PositiveSmallIntegerField(default=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=3)),
                ('stock', models.PositiveSmallIntegerField(default=False)),
                ('categories', models.ManyToManyField(related_name='articles', to='drinx.Category')),
                ('content_qty_unit', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='drinx.contentunit')),
            ],
        ),
    ]
