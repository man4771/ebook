# Generated by Django 4.1 on 2022-08-03 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(max_length=254, unique=True)),
                ('Password', models.CharField(max_length=12)),
                ('IsActive', models.BooleanField(default=False)),
                ('RegData', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'master',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Role', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'userrole',
            },
        ),
        migrations.CreateModel(
            name='profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BirthDate', models.DateField(auto_created=True)),
                ('FullName', models.CharField(blank=True, default='', max_length=25)),
                ('Gender', models.CharField(choices=[('m', 'male'), ('f', 'female')], max_length=5)),
                ('Mobile', models.CharField(blank=True, default='', max_length=10)),
                ('Country', models.CharField(blank=True, default='', max_length=25)),
                ('State', models.CharField(blank=True, default='', max_length=25)),
                ('City', models.CharField(blank=True, default='', max_length=25)),
                ('Pincode', models.CharField(blank=True, default='', max_length=6)),
                ('Addresss', models.TextField(blank=True, default='', max_length=150)),
                ('Master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ebook_app.master')),
            ],
            options={
                'db_table': 'profile',
            },
        ),
        migrations.AddField(
            model_name='master',
            name='UserRole',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ebook_app.userrole'),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=100)),
                ('ISBN', models.CharField(max_length=18)),
                ('PublishDate', models.DateField(auto_now_add=True)),
                ('UpdateDate', models.DateField(auto_now_add=True)),
                ('Author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ebook_app.profile')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ebook_app.category')),
            ],
            options={
                'db_table': 'book',
            },
        ),
    ]
