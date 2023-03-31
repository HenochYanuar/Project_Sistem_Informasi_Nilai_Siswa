from django.db import models

class User(models.Model):
    id_user = models.CharField(max_length=4, primary_key=True)
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

class Kelas(models.Model):
    id_kelas = models.CharField(max_length=4, primary_key=True)
    nama_kelas = models.CharField(max_length=255)
    nip_waliKelas = models.ForeignKey(Guru, on_delete=models.SET_NULL, null=True)

class Siswa(models.Model):
    nis = models.CharField(max_length=10, primary_key=True)
    nama = models.CharField(max_length=255)
    jk = models.CharField(max_length=10)
    alamat = models.TextField()
    agama = models.CharField(max_length=20)
    no_tlpn = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    foto = models.CharField(max_length=255)
    tgl_lahir = models.DateField()
    id_kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)

class Mapel(models.Model):
    id_mapel = models.CharField(max_length=4, primary_key=True)
    nama_maple = models.CharField(max_length=255)
    nip_guru = models.ForeignKey(Guru, on_delete=models.CASCADE)

class Nilai(models.Model):
    id_nilai = models.CharField(max_length=4, primary_key=True)
    nil_ul1 = models.IntegerField()
    nil_ul2 = models.IntegerField()
    nil_ul3 = models.IntegerField()
    nil_uts = models.IntegerField()
    nil_uas = models.IntegerField()
    nil_rata_rata = models.IntegerField()
    id_siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    id_mapel = models.ForeignKey(Mapel, on_delete=models.CASCADE)