# Generated by Django 4.2.6 on 2023-11-11 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_pengolahan_sampel_2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absensi',
            name='status_absensi',
            field=models.CharField(choices=[('belum absen', 'Belum Absen'), ('sudah absen', 'Sudah Absen')], default='sudah absen', max_length=255),
        ),
    ]