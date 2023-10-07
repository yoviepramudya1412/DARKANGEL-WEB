# Generated by Django 4.2.6 on 2023-10-07 05:24

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dosen',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nip', models.CharField(max_length=14, unique=True)),
                ('nama_dosen', models.CharField(max_length=255)),
                ('umur', models.PositiveIntegerField()),
                ('golongan', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pengolahan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sampel_1', models.ImageField(upload_to=core.models.generate_filename)),
                ('sampel_2', models.ImageField(upload_to=core.models.generate_filename)),
                ('sampel_3', models.ImageField(upload_to=core.models.generate_filename)),
                ('sampel_4', models.ImageField(upload_to=core.models.generate_filename)),
                ('sampel_5', models.ImageField(upload_to=core.models.generate_filename)),
                ('sampel_6', models.ImageField(upload_to=core.models.generate_filename)),
                ('sampel_7', models.ImageField(upload_to=core.models.generate_filename)),
                ('sampel_8', models.ImageField(upload_to=core.models.generate_filename)),
                ('sampel_9', models.ImageField(upload_to=core.models.generate_filename)),
                ('sampel_10', models.ImageField(upload_to=core.models.generate_filename)),
                ('sampel_11', models.ImageField(upload_to=core.models.generate_filename)),
                ('profil', models.ImageField(upload_to='profil/')),
                ('dosen', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.dosen')),
            ],
        ),
        migrations.CreateModel(
            name='Absensi',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tanggal_absensi', models.DateTimeField()),
                ('status_absensi', models.CharField(max_length=255)),
                ('sisa_absensi', models.IntegerField()),
                ('berapa_kali_absensi', models.IntegerField()),
                ('dosen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.dosen')),
                ('pengolahan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.pengolahan')),
            ],
        ),
    ]
