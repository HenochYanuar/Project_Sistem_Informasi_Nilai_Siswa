# Generated by Django 4.1.7 on 2023-03-15 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sins', '0002_alter_nilai_nil_rata_rata_alter_nilai_nil_uas_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guru',
            name='nip',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='siswa',
            name='nis',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
