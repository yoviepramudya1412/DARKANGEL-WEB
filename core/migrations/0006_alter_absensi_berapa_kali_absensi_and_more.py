# Generated by Django 4.2.6 on 2023-11-07 13:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_pengolahan_sampel_10_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absensi',
            name='berapa_kali_absensi',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='absensi',
            name='sisa_absensi',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='absensi',
            name='status_absensi',
            field=models.CharField(choices=[('belum absen', 'Belum Absen'), ('sudah absen', 'Sudah Absen')], default='belum absen', max_length=255),
        ),
        migrations.AlterField(
            model_name='absensi',
            name='tanggal_absensi',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
