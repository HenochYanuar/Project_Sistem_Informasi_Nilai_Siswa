from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Guru, Kelas, Siswa, Mapel, Jadwal, Siswa_Kelas, Nilai
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, HttpResponse
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
import io
from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.template.loader import get_template
from django_xhtml2pdf.utils import pdf_decorator
from django.template.loader import render_to_string
from django.conf import settings
from xhtml2pdf import pisa


def index(request):
    return render(request, 'aboutUs.html')

# Views For Admin Pages


def admin(request):
    data_nilai = Nilai.objects.count()
    data_guru = Guru.objects.count()
    data_siswa = Siswa.objects.count()
    data_kelas = Kelas.objects.count()
    data_mapel = Mapel.objects.count()
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_guru': data_guru,
        'data_siswa': data_siswa,
        'data_kelas': data_kelas,
        'data_mapel': data_mapel,
        'data_nilai': data_nilai,
        'user' : user
    }
    return render(request, 'admin/admin.html', context)

def adminLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username, password=password)

        except User.DoesNotExist:
            messages.error(request, 'Username atau Password tidak ditemukan')
            return render(request, 'admin/adminLogin.html')
        
        if user.role == 'Admin':
            request.session['id_user'] = user.id_user
            return redirect('/admin')
        
        else:
            messages.error(request, 'Hanya Admin yang Dapat Mengakses Halaman Ini')
            return render(request, 'admin/adminLogin.html')
    else:
        return render(request, 'admin/adminLogin.html')
    
def adminLogout(request):
    del request.session['id_user']
    return redirect('/adminLogin')



# Create Views For Users CRUD
# def produk(request):
#     search_term = request.GET.get('search')
#     produk = UserProduct.objects.all()

#     if search_term:
#         produk = produk.filter(namaproduct__icontains=search_term)

#     context = {
#         'produk': produk,
#         'search_term': search_term
#     }

#     return render(request, 'user/produk.html', context

def users(request):
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    query = request.GET.get('search')  # Mendapatkan nilai parameter pencarian dari URL
    data_user = User.objects.all()
    
    if query:
        # Lakukan pencarian menggunakan model atau sumber data Anda
        data_user = data_user.filter(
                Q(role__icontains=query) |
                Q(username__icontains=query) |
                Q(id_user__icontains=query) 
            )
    
    context = {
        'data_user': data_user,
        'user': user,
        'query': query
    }
    return render(request, 'admin/users/index.html', context)


def tambahUser(request):
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    return render(request, 'admin/users/tambahData.html', {'user' : user})


def postDatauser(request):

    id_user = request.POST['id_user']
    username = request.POST['username']
    password = request.POST['password']
    password2 = request.POST['password2']
    role = request.POST['role']

    message = None
    if not id_user:
        message = 'ID User Tidak Boleh Kosong'
    elif not username:
        message = 'Username Tidak Boleh Kosong'
    elif not password:
        message = 'Password Tidak Boleh Kosong'
    elif not password2:
        message = 'Chack Password Tidak Boleh Kosong'

    if message:
        return render(request, 'admin/users/tambahData.html', {'message': message})
    else:
        if User.objects.filter(id_user=id_user).exists():
            message = 'ID User Sudah Ada, ID User Tidak Boleh Sama'
            return render(request, 'admin/users/tambahData.html', {'message': message})
        else:
            if password == password2:
                tambah_user = User(
                    id_user=id_user,
                    username=username,
                    password=password,
                    role=role,
                )
                tambah_user.save()
                messages.success(request, 'Data User Berhasil Ditambahkan')
            else:
                messages.error(request, 'User do not match')
        return redirect('/indexUsers')


def updateDatauser(request, id_user):
    data_user = User.objects.get(id_user=id_user)
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_user': data_user,
        'user' : user
    }
    return render(request, 'admin/users/updateData.html', context)


def postUpdateuser(request):
    id_user = request.POST['id_user']
    username = request.POST['username']
    password = request.POST['password']
    password2 = request.POST['password2']
    role = request.POST['role']

    user = User.objects.get(id_user=id_user)
    if password == password2:
        user.username = username
        user.password = password
        user.role = role
        user.save()
        messages.success(request, 'Data User Berhasil Diupdate')
    else:
        messages.error(request, 'User not do match password')
    return redirect('/indexUsers')


def deleteDatauser(request, id_user):
    data_user = User.objects.get(id_user=id_user)
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_user': data_user,
        'user' : user
    }
    return render(request, 'admin/users/deleteData.html', context)


def postDeleteuser(request, id_user):
    data_user = User.objects.get(id_user=id_user).delete()
    messages.success(request, 'Data User Berhasil Dihapus')

    return redirect('/indexUsers')


# Cerate Views For Guru CRUD

def guru(request):
    query = request.GET.get('search')
    data_guru = Guru.objects.all()
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)

    if query:
        # Lakukan pencarian menggunakan model atau sumber data Anda
        data_guru = data_guru.filter(
                Q(nip__icontains=query) |
                Q(nama__icontains=query)
            )
        
    context = {
        'data_guru': data_guru,
        'user' : user,
        'query': query
    }
    return render(request, 'admin/guru/index.html', context)


def tambahGuru(request):
    if request.method == 'POST':
        nip = request.POST['nip']
        nama = request.POST['nama']
        jk = request.POST['jk']
        alamat = request.POST['alamat']
        agama = request.POST['agama']
        no_tlpn = request.POST['no_tlpn']
        email = request.POST['email']
        tgl_lahir = request.POST['tgl_lahir']
        foto = request.FILES['foto']
        id_user = request.POST['id_user']

        user = User.objects.get(id_user=id_user)

        message = None
        if not nip:
            message = 'NIP Tidak Boleh Kosong'
        elif not nama:
            message = 'nama Tidak Boleh Kosong'
        elif not alamat:
            message = 'alamat Tidak Boleh Kosong'
        elif not agama:
            message = 'Agama Tidak Boleh Kosong'
        elif not no_tlpn:
            message = 'No Telepon Tidak Boleh Kosong'
        elif not email:
            message = 'E-mail Tidak Boleh Kosong'
        elif not tgl_lahir:
            message = 'Tanggal Lahir Tidak Boleh Kosong'
        elif not foto:
            message = 'Foto Tidak Boleh Kosong'
        elif not id_user:
            message = 'ID User Tidak Boleh Kosong'

        if message:
            return render(request, 'admin/guru/tambahData.html', {'message': message})
        else:

            if Guru.objects.filter(nip=nip).exists():
                message = 'NIP Sudah Ada, NIP Tidak Boleh Sama'
                return render(request, 'admin/guru/tambahData.html', {'message': message})
            else:
                data_guru = Guru(
                    nip=nip,
                    nama=nama,
                    jk=jk,
                    alamat=alamat,
                    agama=agama,
                    no_tlpn=no_tlpn,
                    email=email,
                    tgl_lahir=tgl_lahir,
                    foto=foto,
                    id_user=user,
                )
                data_guru.save()
                messages.success(request,  'Data Guru Berhasil Ditambahkan')
            return redirect('/indexGuru')
    else:
        users = User.objects.all()
        data_userGuru = Guru.objects.values_list('id_user', flat=True)
        id_user = request.session['id_user']
        user = User.objects.get(id_user = id_user)
        context = {
            'users': users,
            'data_userGuru': data_userGuru,
            'user' : user
        }
        return render(request, 'admin/guru/tambahData.html', context)


def detailGuru(request, nip):
    data_guru = Guru.objects.select_related('id_user').get(nip=nip)
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_guru': data_guru,
        'user' : user
    }
    return render(request, 'admin/guru/detail.html', context)


def updateDataGuru(request, nip):
    if request.method == 'POST':
        id_user = request.POST['id_user']

        user = User.objects.get(id_user=id_user)

        data_guru = Guru(
            nip=request.POST['nip'],
            nama=request.POST['nama'],
            jk=request.POST['jk'],
            alamat=request.POST['alamat'],
            agama=request.POST['agama'],
            no_tlpn=request.POST['no_tlpn'],
            email=request.POST['email'],
            tgl_lahir=request.POST['tgl_lahir'],
            foto=request.FILES['foto'],
            id_user=user,
        )
        data_guru.save()
        messages.success(request,  'Data Guru Berhasil Diupdate')
        return redirect('/indexGuru')
    else:
        data_guru = Guru.objects.select_related('id_user').get(nip=nip)
        users = User.objects.all()
        data_userGuru = Guru.objects.values_list('id_user', flat=True)
        id_user = request.session['id_user']
        user = User.objects.get(id_user = id_user)
        context = {
            'data_guru': data_guru,
            'users': users,
            'data_userGuru': data_userGuru,
            'user' : user
        }
        return render(request, 'admin/guru/updateData.html', context)


def deleteDataGuru(request, nip):
    data_guru = Guru.objects.get(nip=nip)
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_guru': data_guru,
        'user' : user
    }
    return render(request, 'admin/guru/deleteData.html', context)


def postDeleteGuru(request, nip):
    data_guru = Guru.objects.get(nip=nip).delete()
    messages.success(request, 'Data Guru Berhasil Dihapus')

    return redirect('/indexGuru')


# Create Views For Kelas CRUD


def kelas(request):
    # jumlahSiswa = Siswa_Kelas.objects.values('id_kelas').annotate(jumlah_siswa=Count('nis_siswa'))
    data_kelas = Kelas.objects.all()
    id_user = request.session['id_user']
    query = request.GET.get('search')
    user = User.objects.get(id_user = id_user)

    if query:
        # Lakukan pencarian menggunakan model atau sumber data Anda
        data_kelas = data_kelas.filter(
                Q(id_kelas__icontains=query) |
                Q(nama_kelas__icontains=query) 
            )

    context = {
        # 'jumlahSiswa': jumlahSiswa,
        'data_kelas': data_kelas,
        'user' : user,
        'query': query
    }
    return render(request, 'admin/kelas/index.html', context)


def tambahKelas(request):
    if request.method == 'POST':
            id_kelas = request.POST['id_kelas']
            nama_kelas = request.POST['nama_kelas']
            nip_waliKelas = request.POST['nip_waliKelas']

            message = None
            if not id_kelas:
                message = 'ID Kelas Tidak Boleh Kosong'
            elif not nama_kelas:
                message = 'Nama Kelas Tidak Boleh Kosong'

            if message:
                return render(request, 'admin/kelas/tambahData.html', {'message': message})
            else:
                wali_kelas = Guru.objects.get(nip=nip_waliKelas)

                if Kelas.objects.filter(id_kelas=id_kelas).exists():
                    message = 'ID Kelas Sudah Ada, ID Kelas Tidak Boleh Sama'
                    return render(request, 'admin/kelas/tambahData.html', {'message': message})
                else:

                    kelas = Kelas(
                        id_kelas=id_kelas,
                        nama_kelas=nama_kelas,
                        nip_waliKelas=wali_kelas,
                    )
                    kelas.save()
                    list_siswa = request.POST.getlist('siswa[]')
                    for nis_siswa in list_siswa:
                        siswa = Siswa.objects.get(nis=nis_siswa)
                        siswaKelas = Siswa_Kelas(
                            nis_siswa=siswa,
                            id_kelas=kelas,
                        )
                        siswaKelas.save()
                    list_mapel = request.POST.getlist('mapel[]')
                    list_guru = request.POST.getlist('guru[]')
                    for m_id, g_nip in zip(list_mapel, list_guru):
                        mapel = Mapel.objects.get(id_mapel=m_id)
                        guru = Guru.objects.get(nip=g_nip)
                        jadwal = Jadwal(
                            nip_guru = guru,
                            id_kelas = kelas,
                            id_mapel = mapel
                        )
                        jadwal.save()
                    messages.success(request, 'Data Kelas Berhasil Ditambahkan')
                return redirect('/indexKelas')
    else:
        data_mapel = Mapel.objects.all()
        data_siswa = Siswa.objects.all()
        data_guru = Guru.objects.all()
        data_siswaKelas = Siswa_Kelas.objects.values_list('nis_siswa', flat=True)
        data_waliKelas = Kelas.objects.values_list('nip_waliKelas', flat=True)
        id_user = request.session['id_user']
        user = User.objects.get(id_user = id_user)
        context = {
            'data_mapel' : data_mapel,
            'data_siswaKelas': data_siswaKelas,
            'data_siswa': data_siswa,
            'data_guru': data_guru,
            'data_waliKelas': data_waliKelas,
            'user' : user
        }
        return render(request, 'admin/kelas/tambahData.html', context)


def updateDatakelas(request, id_kelas):
    if request.method == 'POST':
        nip_waliKelas = request.POST['nip_waliKelas']

        wali_kelas = Guru.objects.get(nip=nip_waliKelas)

        data_kelas = Kelas.objects.get(id_kelas=id_kelas)
        data_kelas.id_kelasi=request.POST['id_kelas']
        data_kelas.nama_kelas=request.POST['nama_kelas']
        data_kelas.nip_waliKelas=wali_kelas
        data_kelas.save()

        list_siswa = request.POST.getlist('siswa[]')

        for nis_siswa in list_siswa:
            siswa = Siswa.objects.get(nis=nis_siswa)
            siswaKelas = Siswa_Kelas.objects.get(nis_siswa=siswa)
            siswaKelas.nis_siswa =siswa
            siswaKelas.id_kelas=data_kelas
            siswaKelas.save()

        list_mapel = request.POST.getlist('mapel[]')
        list_guru = request.POST.getlist('guru[]')
        kelas_id = request.POST['id_kelas']

        for m_id, g_nip in zip(list_mapel, list_guru):
            mapel = Mapel.objects.get(id_mapel=m_id)
            guru = Guru.objects.get(nip=g_nip)
            kelas = Kelas.objects.get(id_kelas=kelas_id)
            jadwal = Jadwal.objects.filter(id_kelas=kelas, id_mapel=mapel)
            for j in jadwal:
                j.nip_guru =guru
                j.id_kelas=data_kelas
                j.id_mapel=mapel
                j.save()

        messages.success(request,  'Data Kelas Berhasil Diupdate')
        return redirect('/indexKelas')
    else:
        data_mapel = Mapel.objects.all()
        jadwal = Jadwal.objects.all()
        data_siswa = Siswa.objects.all()
        data_kelas = Kelas.objects.select_related('nip_waliKelas').get(id_kelas=id_kelas)
        data_siswaKelas = Siswa_Kelas.objects.values_list('nis_siswa', flat=True)
        data_guru = Guru.objects.all()
        data_wali = Kelas.objects.values_list('nip_waliKelas', flat=True)
        id_user = request.session['id_user']
        user = User.objects.get(id_user = id_user)
        context = {
            'data_mapel' : data_mapel,
            'jadwal' : jadwal,
            'data_siswa' : data_siswa,
            'data_kelas': data_kelas,
            'data_siswaKelas' : data_siswaKelas,
            'data_wali': data_wali,
            'data_guru': data_guru,
            'user' : user
        }
        return render(request, 'admin/kelas/updateData.html', context)


def deleteDataKelas(request, id_kelas):
    data_kelas = Kelas.objects.select_related('nip_waliKelas').get(id_kelas=id_kelas)
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_kelas': data_kelas,
        'user' : user
    }
    return render(request, 'admin/kelas/deleteData.html', context)


def postDeleteKelas(request, id_kelas):
    data_kelas = Kelas.objects.select_related('nip_waliKelas').get(id_kelas=id_kelas).delete()
    messages.success(request, 'Data Kelas Berhasil Dihapus')

    return redirect('/indexKelas')


def detailKelas(request, id_kelas):
    data_mapel = Jadwal.objects.select_related('id_mapel').filter(id_kelas=id_kelas)
    siswa = Siswa_Kelas.objects.select_related('id_kelas').filter(id_kelas=id_kelas)
    kelas = Kelas.objects.get(id_kelas=id_kelas)
    data_siswa = Siswa_Kelas.objects.select_related('nis_siswa').filter(id_kelas=id_kelas)
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'siswa': siswa,
        'kelas': kelas,
        'data_siswa': data_siswa,
        'data_mapel' : data_mapel,
        'user' : user
    }
    return render(request, 'admin/kelas/detail.html', context)

# Create Views For Mapel CRUD


def mapel(request):
    data_mapel = Mapel.objects.all()
    id_user = request.session['id_user']
    query = request.GET.get('search')
    user = User.objects.get(id_user = id_user)

    if query:
        # Lakukan pencarian menggunakan model atau sumber data Anda
        data_mapel = data_mapel.filter(
                Q(id_mapel__icontains=query) |
                Q(nama_mapel__icontains=query)
            )
        
    context = {
        'data_mapel': data_mapel,
        'user' : user,
        'query': query
    }
    return render(request, 'admin/mapel/index.html', context)


def tambahMapel(request):
    if request.method == 'POST':
        id_mapel = request.POST['id_mapel']
        nama_mapel = request.POST['nama_mapel']

        message = None
        if not id_mapel:
            message = 'ID Mata Pelajaran Tidak Boleh Kosong'
        elif not nama_mapel:
            message = 'Nama Mata Pelajaran Tidak Boleh Kosong'

        if message:
            return render(request, 'admin/mapel/tambahData.html', {'message': message})
        else:
            if Mapel.objects.filter(id_mapel=id_mapel).exists():
                message = 'ID Mata Pelajaran Sudah Ada, ID Mata Pelajaran Tidak Boleh Sama'
                return render(request, 'admin/mapel/tambahData.html', {'message': message})
            else:
                data_mapel = Mapel(
                    id_mapel=id_mapel,
                    nama_mapel=nama_mapel
                )
                data_mapel.save()
                messages.success(request, 'Data Mata Pelajaran Berhasil Ditambahkan')
            return redirect('/indexMapel')
    else:
        id_user = request.session['id_user']
        user = User.objects.get(id_user = id_user)
        return render(request, 'admin/mapel/tambahData.html', {'user' : user})


def updateDataMapel(request, id_mapel):
    if request.method == 'POST':
        data_kelas = Mapel(
            id_mapel=request.POST['id_mapel'],
            nama_mapel=request.POST['nama_mapel']
        )
        data_kelas.save()
        messages.success(request, 'Data Mata Pelajaran berhasil Diupdate')
        return redirect('/indexMapel')
    else:
        data_mapel = Mapel.objects.get(id_mapel=id_mapel)
        id_user = request.session['id_user']
        user = User.objects.get(id_user = id_user)
        context = {
            'data_mapel': data_mapel,
            'user' : user
        }
        return render(request, 'admin/mapel/updateData.html', context)


def deleteDataMapel(request, id_mapel):
    data_mapel = Mapel.objects.get(id_mapel=id_mapel)
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_mapel': data_mapel,
        'user' : user
    }
    return render(request, 'admin/mapel/deleteData.html', context)


def postDeleteMapel(request, id_mapel):
    Mapel.objects.get(id_mapel=id_mapel).delete()
    messages.success(request, 'Data Mata pelajaran Berhasil Dihpaus')

    return redirect('/indexMapel')

# Cerate Views For Siswa CRUD


def siswa(request):
    data_siswa = Siswa.objects.all()
    id_user = request.session['id_user']
    query = request.GET.get('search')
    user = User.objects.get(id_user = id_user)

    if query:
        # Lakukan pencarian menggunakan model atau sumber data Anda
        data_siswa = data_siswa.filter(
                Q(nis__icontains=query) |
                Q(nama__icontains=query)
            )
        
    context = {
        'data_siswa': data_siswa,
        'user' : user,
        'query': query
    }
    return render(request, 'admin/siswa/index.html', context)


def tambahSiswa(request):
    if request.method == 'POST':
        nis = request.POST['nis']
        nama = request.POST['nama']
        jk = request.POST['jk']
        alamat = request.POST['alamat']
        agama = request.POST['agama']
        semester = request.POST['semester']
        no_tlpn = request.POST['no_tlpn']
        email = request.POST['email']
        foto = request.FILES['foto']
        tgl_lahir = request.POST['tgl_lahir']
        id_user = request.POST['id_user']

        user = User.objects.get(id_user=id_user)

        if Siswa.objects.filter(nis=nis).exists():
            message = messages.error(request, 'Data is already exists')
            return render(request, 'admin/siswa/tambahData.html', {'message': message})
        else:
            data_siswa = Siswa(
                nis=nis,
                nama=nama,
                jk=jk,
                alamat=alamat,
                agama=agama,
                semester=semester,
                no_tlpn=no_tlpn,
                email=email,
                foto=foto,
                tgl_lahir=tgl_lahir,
                id_user=user,
            )
            data_siswa.save()
            messages.success(request,  ' Data is successfully saved')
        return redirect('/indexSiswa')
    else:
        users = User.objects.all()
        data_userSiswa = Siswa.objects.values_list('id_user', flat=True)
        id_user = request.session['id_user']
        user = User.objects.get(id_user = id_user)
        context = {
            'users': users,
            'data_userSiswa': data_userSiswa,
            'user' : user
        }
    return render(request, 'admin/siswa/tambahData.html', context)


def detailSiswa(request, nis):
    data_siswa = Siswa.objects.select_related('id_user').get(nis=nis)
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_siswa': data_siswa,
        'user' : user
    }
    return render(request, 'admin/siswa/detail.html', context)


def updateDataSiswa(request, nis):
    if request.method == 'POST':
        id_user = request.POST['id_user']

        user = User.objects.get(id_user=id_user)

        data_siswa = Siswa(
            nis=request.POST['nis'],
            nama=request.POST['nama'],
            jk=request.POST['jk'],
            alamat=request.POST['alamat'],
            semester=request.POST['semester'],
            agama=request.POST['agama'],
            no_tlpn=request.POST['no_tlpn'],
            foto=request.FILES['foto'],
            email=request.POST['email'],
            tgl_lahir=request.POST['tgl_lahir'],
            id_user=user,
        )
        data_siswa.save()
        messages.success(request,  ' Data is successfully saved')
        return redirect('/indexSiswa')
    else:
        data_siswa = Siswa.objects.select_related('id_user').get(nis=nis)
        users = User.objects.all()
        data_userSiswa = Siswa.objects.values_list('id_user', flat=True)
        id_user = request.session['id_user']
        user = User.objects.get(id_user = id_user)
        context = {
            'data_siswa': data_siswa,
            'users': users,
            'data_userSiswa': data_userSiswa,
            'user' : user
        }
        return render(request, 'admin/siswa/updateData.html', context)


def deleteDataSiswa(request, nis):
    data_siswa = Siswa.objects.get(nis=nis)
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_siswa': data_siswa,
        'user' : user
    }
    return render(request, 'admin/siswa/deleteData.html', context)


def postDeleteSiswa(request, nis):
    data_siswa = Siswa.objects.get(nis=nis).delete()
    messages.success(request, 'Data Siswa deleted successfully')

    return redirect('/indexSiswa')


def postDatasiswa(request):
    nis = request.POST['nis']
    nama = request.POST['nama']
    jk = request.POST['jeniskelamin']
    alamat = request.POST['alamat']
    agama = request.POST['agama']
    no_tlpn = request.POST['nomortelepon']
    email = request.POST['email']
    foto = request.POST['foto']
    tgl_lahir = request.POST['tanggallahir']

    if Siswa.objects.filter(nis=nis).exists():
        messages.error(request, 'nis already exists')
    else:
        tambah_siswa = Siswa(
            nis=nis,
            nama=nama,
            jk=jk,
            alamat=alamat,
            agama=agama,
            no_tlpn=no_tlpn,
            email=email,
            foto=foto,
            tgl_lahir=tgl_lahir,
        )
        tambah_siswa.save()
        messages.success(request, 'Siswa successfully saved')
    return redirect('/admin/siswa/index')


def siswakelas(request):
    if request.method == 'POST':
        id_kelas = request.POST.get('id_kelas')
        siswa = request.POST.getlist('siswa[]')
        for s in siswa:
            list_siswa = Siswa.objects.get(nis=s)
            Siswa_Kelas.objects.create(
                nis_siswa=list_siswa,
                id_kelas=id_kelas,
            )
            # return HttpResponse(s)
    else:
        data_kelas = Kelas.objects.all()
        data_siswa = Siswa.objects.all()
        data_guru = Guru.objects.all()
        data_waliKelas = Kelas.objects.values_list('nip_waliKelas', flat=True)
        id_user = request.session['id_user']
        user = User.objects.get(id_user = id_user)
        context = {
            'data_kelas': data_kelas,
            'data_siswa': data_siswa,
            'data_guru': data_guru,
            'data_waliKelas': data_waliKelas,
            'user' : user
        }
        return render(request, 'siswakelas.html', context)
    
#Create Views For Nilai Siswa di halaman Admin


def exportPdfSiswa(request):
    kelas = request.GET.get('kelas')
    mapel = request.GET.get('mapel')
    if not kelas and not mapel:
        siswa = Siswa_Kelas.objects.all()
        mapel = Mapel.objects.all()
    elif not kelas :
        siswa = Siswa_Kelas.objects.all()
        mapel = Mapel.objects.filter(id_mapel=mapel)
    elif not mapel:
        siswa = Siswa_Kelas.objects.filter(id_kelas=kelas)
        mapel = Mapel.objects.all()
    else:
        siswa = Siswa_Kelas.objects.filter(id_kelas=kelas)
        mapel = Mapel.objects.filter(id_mapel=mapel)


    # nilai = Nilai.objects.filter(id_siswa=siswa.nis)
    nilai = Nilai.objects.all()

    template = get_template('admin/export/pdf_siswa_template.html')

    html_string = template.render({'siswa': siswa, 'nilai' : nilai, 'mapel' : mapel})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="dataSiswa.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        # Jika terjadi kesalahan saat konversi
        return HttpResponse('Terjadi kesalahan saat mengonversi HTML ke PDF')

    return response

def hapus(request):
    user = User.objects.all()

    for u in user:
        if u.role == "Siswa":
            u.delete()
    
    return render(request, 'admin/user/index.html')

def exportSiswa(request):
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    siswa = Siswa.objects.all()
    kelas = Kelas.objects.all()
    mapel = Mapel.objects.all()

    context = {
        'user' : user,
        'siswa' : siswa,
        'mapel' : mapel,
        'kelas' : kelas
    }
    return render(request, 'admin/export/exportSiswa.html', context)

def exportPdfGuru(request):
    kelas = request.GET.get('kelas')
    mapel = request.GET.get('mapel')

    if not kelas and not mapel:
        guru_list = Jadwal.objects.all().select_related('id_mapel')
    elif not mapel:
        guru_list = Jadwal.objects.filter(id_kelas=kelas)
    elif not kelas:
        guru_list = Jadwal.objects.filter(id_mapel=mapel)
    else:
        guru_list = Jadwal.objects.filter(id_mapel=mapel, id_kelas=kelas)


    guru = set()
    for g in guru_list:
        guru.add((g.nip_guru.nama, g.nip_guru.nip))

    one_guru = list(guru)

    template = get_template('admin/export/pdf_guru_template.html')

    html_string = template.render({'one_guru' : one_guru, 'guru_list' : guru_list})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="dataGuru.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        # Jika terjadi kesalahan saat konversi
        return HttpResponse('Terjadi kesalahan saat mengonversi HTML ke PDF')

    return response

def exportGuru(request):
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    guru = Guru.objects.all()
    mapel = Mapel.objects.all()
    kelas = Kelas.objects.all()

    context = {
        'user' : user,
        'guru' : guru,
        'mapel' : mapel,
        'kelas' : kelas
    }

    return render(request, 'admin/export/exportGuru.html', context)

#Create Views For Guru Pages
#Create Viewa For Guru Dashboard

def guruLogin(request):
    if request.method == 'POST':
        nip = request.POST['nip']
        password = request.POST['password']

        try:
            guru = Guru.objects.get(nip=nip)

        except Guru.DoesNotExist:
            messages.error(request, 'NIP Tidak Ditemukan')
            return render(request, 'guru/guruLogin.html')
        
        try:
            user = User.objects.get(password=password, id_user=guru.id_user.id_user)
            gr_pss = user.password

        except User.DoesNotExist:
            messages.error(request, 'Passwoord Tidak Valid')
            return render(request, 'guru/guruLogin.html')
        
        if password == gr_pss and user.role == 'Guru':
            request.session['nip'] = guru.nip
            return redirect('/guruDashboard')
        else:
            messages.error(request, 'Hanya Guru yang Dapat Mengakses Halaman Ini')
            return render(request, 'guru/guruLogin.html')
    else:
        return render(request, 'guru/guruLogin.html')
    
def guruLogout(request):
    del request.session['nip']
    return redirect('/guruLogin')

def guruDashboard(request):
    guru = Guru.objects.all()
    nip = request.session['nip']
    user = Guru.objects.get(nip = nip)
    # kelas = Kelas.objects.get(nip_waliKelas=user.nip)
    # siswa = Siswa_Kelas.objects.filter(id_kelas=kelas.id_kelas)
    context = {
        'guru' : guru,
        'user' : user,
        # 'kelas' : kelas,
        # 'siswa' : siswa
    }
    return render(request, 'guru/guru.html', context)
    
def guruProfile(request):
    nip = request.session['nip']
    user = Guru.objects.get(nip = nip)
    wali = Kelas.objects.values_list('nip_waliKelas', flat=True)
    if nip in wali:
        kelas = Kelas.objects.get(nip_waliKelas=nip)
        return render(request, 'guru/guruProfile.html', {'user': user, 'kelas' : kelas, 'wali' : wali})
    else:
        kelas = "--Anda Bukan Wali Kelas--"
        return render(request, 'guru/guruProfile.html', {'user': user, 'kelas' : kelas, 'wali' : wali})

def penilaian(request):
    nip = request.session['nip']
    user = Guru.objects.get(nip = nip)
    jadwal = Jadwal.objects.filter(nip_guru=user).select_related('id_mapel', 'id_kelas')

    context = {
        'user': user,
        'jadwal': jadwal
    }
    return render(request, 'guru/penilaian.html', context)

def nilaiSiswa(request, id_kelas, id_mapel):
    nip = request.session['nip']
    user = Guru.objects.get(nip = nip)
    siswa = Siswa_Kelas.objects.all()
    kelas = Kelas.objects.get(id_kelas=id_kelas)
    mapel = Mapel.objects.get(id_mapel=id_mapel)
    jadwal = Jadwal.objects.filter(nip_guru=user, id_mapel=id_mapel, id_kelas=id_kelas)

    context = {
        'user' : user,
        'siswa': siswa,
        'kelas': kelas,
        'jadwal' : jadwal,
        'mapel' : mapel,

    }
    return render(request, 'guru/nilaiSiswa.html', context)

def detailNilai(request, nis_siswa, id_mapel):
    nip = request.session['nip']
    user = Guru.objects.get(nip = nip)
    nilai = Nilai.objects.filter(id_siswa=nis_siswa, id_mapel=id_mapel)
    siswa = Siswa_Kelas.objects.get(nis_siswa=nis_siswa)
    mapel = Mapel.objects.get(id_mapel=id_mapel)

    context = {
        'nilai' : nilai,
        'user' : user,
        'siswa' : siswa,
        'mapel' : mapel
    }
    return render(request, 'guru/detailNilai.html', context)

def uploadNilai(request, nis_siswa, id_mapel):
    if request.method == 'POST':
        pelajaran = request.POST['id_mapel']
        nis = request.POST['nis_siswa']
        tugas = request.POST['tugas']
        ulangan = request.POST['ulangan']
        uts = request.POST['uts']
        uas = request.POST['uas']
        rata_rata = (float(tugas) + float(ulangan) + float(uts) + float(uas)) / 4.0

        siswa = Siswa.objects.get(nis=nis)
        matapel = Mapel.objects.get(id_mapel=pelajaran)

        if float(tugas) > 100 or float(ulangan) > 100 or float(uts) > 100 or float(uas) > 100 :
            messages.error(request, ' Nilai Tidak Boleh Lebih Dari 100')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            nilai = Nilai(
                nil_uts=uts,
                nil_uas=uas,
                nil_rata_tg=tugas,
                nil_rata_ul=ulangan,
                nil_rata_rata=rata_rata,
                id_siswa=siswa,
                id_mapel=matapel
            )

            nilai.save()
            messages.success(request,  ' Nilai Berhasil Disimpan')
            url = reverse('detailnilai', args=[nis_siswa, id_mapel])
            return redirect(url)
    else:
        nip = request.session['nip']
        user = Guru.objects.get(nip = nip)
        siswa = Siswa.objects.get(nis=nis_siswa)
        mapel = Mapel.objects.get(id_mapel=id_mapel)

        context ={
            'user' : user,
            'siswa' :siswa,
            'mapel' : mapel,
        }
        return render(request, 'guru/uploadNilai.html', context)
    
def updateNilai(request, nis_siswa, id_mapel):
    if request.method == 'POST':
        pelajaran = request.POST['id_mapel']
        nis = request.POST['nis_siswa']
        tugas = request.POST['tugas']
        ulangan = request.POST['ulangan']
        uts = request.POST['uts']
        uas = request.POST['uas']
        rata_rata = (float(tugas) + float(ulangan) + float(uts) + float(uas)) / 4.0

        siswa = Siswa.objects.get(nis=nis)
        matapel = Mapel.objects.get(id_mapel=pelajaran)

        if float(tugas) > 100 or float(ulangan) > 100 or float(uts) > 100 or float(uas) > 100 :
            messages.error(request, ' Nilai Tidak Boleh Lebih Dari 100')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:

            nilai = Nilai.objects.get(id_siswa=nis_siswa, id_mapel=id_mapel)

            nilai.nil_uts=uts
            nilai.nil_uas=uas
            nilai.nil_rata_tg=tugas
            nilai.nil_rata_ul=ulangan
            nilai.nil_rata_rata=rata_rata
            nilai.id_siswa=siswa
            nilai.id_mapel=matapel

            nilai.save()
            messages.success(request,  ' Nilai Berhasil Disimpan')
            url = reverse('detailnilai', args=[nis_siswa, id_mapel])
            return redirect(url)
    else:
        nip = request.session['nip']
        user = Guru.objects.get(nip = nip)
        siswa = Siswa.objects.get(nis=nis_siswa)
        mapel = Mapel.objects.get(id_mapel=id_mapel)
        nilai = Nilai.objects.filter(id_siswa=nis_siswa, id_mapel=id_mapel)

        context = {
            'user' : user,
            'siswa' : siswa,
            'mapel' : mapel,
            'nilai' : nilai
        }
        return render(request, 'guru/updateNilai.html', context)
    
def deleteNilai(request, nis_siswa, id_mapel):
    nip = request.session['nip']
    user = Guru.objects.get(nip = nip)
    siswa = Siswa.objects.get(nis=nis_siswa)
    mapel = Mapel.objects.get(id_mapel=id_mapel)
    nilai = Nilai.objects.filter(id_siswa=nis_siswa, id_mapel=id_mapel)

    context = {
        'user' : user,
        'siswa' : siswa,
        'mapel' : mapel,
        'nilai' : nilai
    }
    return render(request, 'guru/deleteNilai.html', context)

def pushDeleteNilai(request, nis_siswa, id_mapel):
    nilai = Nilai.objects.filter(id_siswa=nis_siswa, id_mapel=id_mapel)
    nilai.delete()
    messages.success(request,  ' Nilai Berhasil Dihapus')
    url = reverse('detailnilai', args=[nis_siswa, id_mapel])
    return redirect(url)

def siswaWali(request):
    nip = request.session['nip']
    user = Guru.objects.get(nip = nip)
    wali = Kelas.objects.values_list('nip_waliKelas', flat=True)

    if nip in wali:
        kelas = Kelas.objects.get(nip_waliKelas=user.nip)
        mapel = Mapel.objects.all()
        siswa = Siswa_Kelas.objects.filter(id_kelas=kelas)
        nilai = Nilai.objects.select_related('id_siswa', 'id_mapel')

        context = {
            'user' : user,
            'kelas' : kelas,
            'siswa' : siswa,
            'mapel' : mapel,
            'wali' : wali,
            'nilai' : nilai
        }
    else:
        message1 = 'Belum Ada Nilai Untuk Siswa Wali Anda'
        message2 = 'Mungkin Anda Bukan Wali Kelas'
        context = {
            'user' : user,
            'message1' : message1,
            'message2' : message2,
        }
    return render(request, 'guru/siswaWali.html', context)

def printNilaiWali(request, id_mapel):
    nip = request.session['nip']
    user = Guru.objects.get(nip = nip)
    kelas = Kelas.objects.get(nip_waliKelas=user.nip)
    mapel = Mapel.objects.get(id_mapel=id_mapel)
    siswa = Siswa_Kelas.objects.filter(id_kelas=kelas)
    nilai = Nilai.objects.select_related('id_siswa', 'id_mapel')

    context = {
            'user' : user,
            'kelas' : kelas,
            'siswa' : siswa,
            'mapel' : mapel,
            'nilai' : nilai
        }
    
    template = get_template('guru/printNilaiWali.html')

    html_string = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="nilaiSiswaWali.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        # Jika terjadi kesalahan saat konversi
        return HttpResponse('Terjadi kesalahan saat mengonversi HTML ke PDF')

    return response

#Create Views For Siswa Pages
#Create Views For Siswa Dashboard

def siswaLogin(request):
    if request.method == 'POST':
        nis = request.POST['nis']
        password = request.POST['password']

        try:
            siswa = Siswa.objects.get(nis=nis)

        except Siswa.DoesNotExist:
            messages.error(request, 'NIS Tidak Ditemukan')
            return render(request, 'siswa/siswaLogin.html')
        
        try:
            user = User.objects.get(password=password, id_user=siswa.id_user.id_user)
            sw_pss = user.password

        except User.DoesNotExist:
            messages.error(request, 'Passwoord Tidak Valid')
            return render(request, 'siswa/siswaLogin.html')
        
        if password == sw_pss and user.role == 'Siswa':
            request.session['nis'] = siswa.nis
            return redirect('/siswaDashboard')
        else:
            messages.error(request, 'Hanya Siswa yang Dapat Mengakses Halaman Ini')
            return render(request, 'siswa/siswaLogin.html')
    else:
        return render(request, 'siswa/siswaLogin.html')
    
def siswaLogout(request):
    del request.session['nis']
    return redirect('/siswaLogin')

def siswaDashboard(request):
    siswa = Siswa.objects.all()
    nis = request.session['nis']
    user = Siswa.objects.get(nis = nis)
    context = {
        'siswa' : siswa,
        'user' : user
    }
    return render(request, 'siswa/siswa.html', context)

def siswaProfile(request):
    nis = request.session['nis']
    user = Siswa.objects.get(nis = nis)
    kelas = Siswa_Kelas.objects.get(nis_siswa=nis)
    return render(request, 'siswa/siswaProfile.html', {'user': user, 'kelas' : kelas})

def nilai(request):
    nis = request.session['nis']
    user = Siswa.objects.get(nis = nis)
    nilai = Nilai.objects.filter(id_siswa=nis).select_related('id_siswa', 'id_mapel')
    siswa = Siswa_Kelas.objects.get(nis_siswa=nis)

    context = {
        'user': user,
        'nilai': nilai,
        'siswa' : siswa
    }

    return render(request, 'siswa/nilai.html', context)

def exportNilaiPribadi(request):
    nis = request.session['nis']
    user = Siswa.objects.get(nis = nis)
    nilai = Nilai.objects.filter(id_siswa=nis).select_related('id_siswa', 'id_mapel')
    siswa = Siswa_Kelas.objects.get(nis_siswa=nis)

    context = {
        'user': user,
        'nilai': nilai,
        'siswa' : siswa
    }

    template = get_template('siswa/pdf_raport_template.html')

    html_string = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="nilaiRaport.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        # Jika terjadi kesalahan saat konversi
        return HttpResponse('Terjadi kesalahan saat mengonversi HTML ke PDF')

    return response
