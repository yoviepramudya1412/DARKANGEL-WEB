import uuid
from django.db import models

# Create your models here.
# acckey serve --yoviepramudya


class Dosen(models.Model):
    id = models.AutoField(primary_key=True)
    nip = models.CharField(max_length=14, unique=True)
    nama_dosen = models.CharField(max_length=255)
    umur = models.PositiveIntegerField()
    golongan = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.nama_dosen

def generate_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'sampel/{filename}'

class Pengolahan(models.Model):
    id = models.AutoField(primary_key=True)
    dosen = models.OneToOneField(Dosen, on_delete=models.CASCADE)
    sampel_1 = models.ImageField(upload_to=generate_filename)
    sampel_2 = models.ImageField(upload_to=generate_filename)
    sampel_3 = models.ImageField(upload_to=generate_filename)
    sampel_4 = models.ImageField(upload_to=generate_filename)
    sampel_5 = models.ImageField(upload_to=generate_filename)
    sampel_6 = models.ImageField(upload_to=generate_filename)
    sampel_7 = models.ImageField(upload_to=generate_filename)
    sampel_8 = models.ImageField(upload_to=generate_filename)
    sampel_9 = models.ImageField(upload_to=generate_filename)
    sampel_10 = models.ImageField(upload_to=generate_filename)
    sampel_11 = models.ImageField(upload_to=generate_filename)
    profil = models.ImageField(upload_to='profil/')

    def __str__(self):
        return self.dosen.nama_dosen
    
class Absensi(models.Model):
    id = models.AutoField(primary_key=True)
    dosen = models.ForeignKey(Dosen, on_delete=models.CASCADE)
    pengolahan = models.ForeignKey(Pengolahan, on_delete=models.CASCADE)
    tanggal_absensi = models.DateTimeField()
    status_absensi = models.CharField(max_length=255)
    sisa_absensi = models.IntegerField()
    berapa_kali_absensi = models.IntegerField()

    def __str__(self):
        return f"{self.dosen.nama_dosen} - {self.tanggal_absensi}"
