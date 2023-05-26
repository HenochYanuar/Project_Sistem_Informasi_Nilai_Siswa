from django.core.exceptions import ValidationError
from django.db import models
import os
import random
from django.conf import settings
from faker import Faker

fake = Faker()
photo_dir = 'static/assets/dist/img'
photo_choice = 'static/assets/dist/foto_dummy'

class User(models.Model):
    id_user = models.CharField(max_length=10, primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=10)
    role = models.CharField(max_length=5)

class Guru(models.Model):
    nip = models.CharField(max_length=18, primary_key=True)
    nama = models.CharField(max_length=255)
    jk = models.CharField(max_length=10)
    alamat = models.TextField()
    agama = models.CharField(max_length=20)
    no_tlpn = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    foto = models.ImageField(upload_to= 'static/assets/dist/img', blank=True, null=True)
    tgl_lahir = models.DateField()
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        # hapus foto yang terkait dengan instance Guru saat dihapus
        if self.foto:
            os.remove(self.foto.path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # cek apakah terdapat foto baru yang diunggah
        if self.nip:
            try:
                old_image = Guru.objects.get(nip=self.nip).foto
            except Guru.DoesNotExist:
                old_image = None

            if old_image and self.foto and old_image != self.foto:
                os.remove(os.path.join(settings.MEDIA_ROOT, old_image.name))

        super().save(*args, **kwargs)

def create_fake_guru():
    guru = Guru()
    guru.nip = fake.random_int(min=100000000000000001, max=999999999999999999)
    guru.nama = fake.name()
    guru.jk = fake.random_element(elements=('Laki-laki', 'Perempuan'))
    guru.alamat = fake.address()
    guru.agama = fake.random_element(elements=('Islam', 'Kristen', 'Katolik', 'Hindu', 'Buddha', 'Konghucu'))
    guru.no_tlpn = fake.phone_number()
    guru.email = fake.email()
    # guru.foto = fake.image_url()
    guru.tgl_lahir = fake.date_of_birth(minimum_age=25, maximum_age=60)
    guru.id_user = User.objects.create(
        id_user=str(guru.nip),
        username=fake.user_name(),
        password=fake.password(length=8),
        role='Guru'
    )
    guru.save()

# # Membuat 10 data faker untuk Guru
# for _ in range(20):
#     create_fake_guru()

class Kelas(models.Model):
    id_kelas = models.CharField(max_length=10, primary_key=True)
    nama_kelas = models.CharField(max_length=255)
    nip_waliKelas = models.ForeignKey(Guru, on_delete=models.SET_NULL, null=True)

class Siswa(models.Model):
    nis = models.CharField(max_length=10, primary_key=True)
    nama = models.CharField(max_length=255)
    jk = models.CharField(max_length=10)
    alamat = models.TextField()
    agama = models.CharField(max_length=20)
    semester = models.CharField(max_length=10)
    no_tlpn = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    foto = models.ImageField(upload_to= 'static/assets/dist/img', blank=True, null=True)
    tgl_lahir = models.DateField()
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        # hapus foto yang terkait dengan instance Guru saat dihapus
        if self.foto:
            os.remove(self.foto.path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # cek apakah terdapat foto baru yang diunggah
        if self.nis:
            try:
                old_image = Siswa.objects.get(nis=self.nis).foto
            except Siswa.DoesNotExist:
                old_image = None

            if old_image and self.foto and old_image != self.foto:
                os.remove(os.path.join(settings.MEDIA_ROOT, old_image.name))

        super().save(*args, **kwargs)

def create_fake_siswa():
    siswa = Siswa()
    siswa.nis = fake.random_int(min=1001111001, max=2099999999)
    siswa.nama = fake.name()
    siswa.jk = fake.random_element(elements=('Laki-laki', 'Perempuan'))
    siswa.alamat = fake.address()
    siswa.agama = fake.random_element(elements=('Islam', 'Kristen', 'Katolik', 'Hindu', 'Buddha', 'Konghucu'))
    siswa.semester = fake.random_element(elements=('Semester 1', 'Semester 3', 'Semester 5'))
    siswa.no_tlpn = fake.phone_number()
    siswa.email = fake.email()
    foto_name = random.choice(os.listdir(photo_choice))
    siswa.foto.name = os.path.join(photo_choice, foto_name)
    siswa.tgl_lahir = fake.date_of_birth(minimum_age=12, maximum_age=18)
    siswa.id_user = User.objects.create(
        id_user=str(siswa.nis),
        username=fake.user_name(),
        password=fake.password(length=8),
        role='Siswa'
    )
    siswa.save()

# for _ in range(10):
#     create_fake_siswa()

class Siswa_Kelas(models.Model):
    nis_siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    id_kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)

class Mapel(models.Model):
    id_mapel = models.CharField(max_length=4, primary_key=True)
    nama_mapel = models.CharField(max_length=255)

class Jadwal(models.Model):
    nip_guru = models.ForeignKey(Guru, on_delete=models.CASCADE)
    id_kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    id_mapel = models.ForeignKey(Mapel, on_delete=models.CASCADE)

class Nilai(models.Model):
    nil_uts = models.FloatField()
    nil_uas = models.FloatField()
    nil_rata_ul = models.FloatField()
    nil_rata_tg = models.FloatField()
    nil_rata_rata = models.FloatField()
    id_siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    id_mapel = models.ForeignKey(Mapel, on_delete=models.CASCADE)

    def clean(self):
        # Validasi apakah kombinasi id_siswa dan id_mapel sudah ada pada model Nilai
        if Nilai.objects.filter(id_siswa=self.id_siswa, id_mapel=self.id_mapel).exists():
            raise ValidationError("Kombinasi id_siswa dan id_mapel sudah ada.")

def create_fake_nilai():
    nilai = Nilai()
    nilai.nil_uts = fake.random_int(min=20, max=100)
    nilai.nil_uas = fake.random_int(min=20, max=100)
    nilai.nil_rata_ul = fake.random_int(min=20, max=100)
    nilai.nil_rata_tg = fake.random_int(min=20, max=100)
    nilai.nil_rata_rata = (nilai.nil_uts + nilai.nil_uas + nilai.nil_rata_ul + nilai.nil_rata_tg) / 4
    nilai.id_siswa = Siswa.objects.order_by('?').first()
    nilai.id_mapel = Mapel.objects.order_by('?').first()
    nilai.full_clean()  # Melakukan validasi sebelum menyimpan objek Nilai
    nilai.save()

# for _ in range(1440):
#     create_fake_nilai()
