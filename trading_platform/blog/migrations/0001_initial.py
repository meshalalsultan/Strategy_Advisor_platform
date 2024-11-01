# Generated by Django 5.0.1 on 2024-10-28 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='الاسم')),
                ('slug', models.SlugField(unique=True, verbose_name='الرابط')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
            ],
            options={
                'verbose_name': 'تصنيف',
                'verbose_name_plural': 'تصنيفات',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='العنوان')),
                ('slug', models.SlugField(unique=True, verbose_name='الرابط')),
                ('content', models.TextField(verbose_name='المحتوى')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ النشر')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')),
            ],
            options={
                'verbose_name': 'مقال',
                'verbose_name_plural': 'مقالات',
                'ordering': ['-created_at'],
            },
        ),
    ]
