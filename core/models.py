import uuid
from django.contrib.auth.hashers import make_password
from django.utils import timezone



from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, nip, nama, umur, golongan, password=None):
        if not nip:
            raise ValueError('NIP field must be set')
        user = self.model(
            nip=nip,
            nama=nama,
            umur=umur,
            golongan=golongan,
        )
        user.set_password(password)  # hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, nip, nama, umur, golongan, password=None):
        user = self.create_user(
            nip=nip,
            nama=nama,
            umur=umur,
            golongan=golongan,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    nip = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=255)
    umur = models.IntegerField()
    golongan = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    # Use NIP as the username field
    USERNAME_FIELD = 'nip'
    REQUIRED_FIELDS = ['nama', 'umur', 'golongan']

    def __str__(self):
        return self.nama

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser








def generate_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'sampel/{filename}'
def generate_filename2(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'training/{filename}'

class Pengolahan(models.Model):
    id = models.AutoField(primary_key=True)
    staff = models.name = models.ForeignKey(CustomUser, related_name='pengolahan', on_delete=models.CASCADE)
    sampel_1 = models.ImageField(upload_to=generate_filename, null=True, blank=True)
    sampel_2 = models.ImageField(upload_to=generate_filename2, null=True, blank=True)
    profil = models.ImageField(upload_to='profil/', null=True, blank=True)

    def __str__(self):
        return self.staff.nama 
    
    
    

class Absensi(models.Model):
    ABSENCE_STATUS_CHOICES = [
        ('belum absen', 'Belum Absen'),
        ('sudah absen', 'Sudah Absen'),
    ]

    id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='absensi')
    pengolahan = models.ForeignKey(Pengolahan, on_delete=models.CASCADE)
    tanggal_absensi = models.DateTimeField(default=timezone.now)
    status_absensi = models.CharField(max_length=255, choices=ABSENCE_STATUS_CHOICES, default='sudah absen')
    sisa_absensi = models.IntegerField(default=0)
    berapa_kali_absensi = models.IntegerField(default=2)

    def save(self, *args, **kwargs):
        # Menghitung sisa_absensi berdasarkan status_absensi dan berapa_kali_absensi
        if self.status_absensi == 'sudah absen':
            self.sisa_absensi = self.berapa_kali_absensi - 1
        else:
            self.sisa_absensi = self.berapa_kali_absensi
        
        super(Absensi, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.staff.nama} - {self.tanggal_absensi}"
