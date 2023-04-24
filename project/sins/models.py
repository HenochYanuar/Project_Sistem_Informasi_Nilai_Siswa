from django.db import models
import os
from django.conf import settings

class User(models.Model):
    id_user = models.CharField(max_length=5, primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=10)
    role = models.CharField(max_length=5)

class Guru(models.Model):
    nip = models.CharField(max_length=10, primary_key=True)
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

class Ulangan(models.Model):
    id_ulangan = models.CharField(max_length=5, primary_key=True)
    nama_ulangan = models.CharField(max_length=255)
    nilai_ulangan = models.IntegerField()

class Nilai(models.Model):
    id_nilai = models.CharField(max_length=4, primary_key=True)
    nil_uts = models.IntegerField()
    nil_uas = models.IntegerField()
    nil_rata_rata = models.IntegerField()
    id_ulangan = models.ForeignKey(Ulangan, on_delete=models.CASCADE)
    id_siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    id_mapel = models.ForeignKey(Mapel, on_delete=models.CASCADE)
