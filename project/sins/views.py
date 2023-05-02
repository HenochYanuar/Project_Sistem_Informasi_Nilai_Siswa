from django.shortcuts import render, redirect
from .models import User, Guru, Kelas, Siswa, Mapel, Jadwal, Siswa_Kelas
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404

# Views For Admin Pages

@login_required
def admin(request):
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

@login_required
def users(request):
    data_user = User.objects.all()
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_user': data_user,
        'user': user
    }
    return render(request, 'admin/users/index.html', context)

@login_required
def tambahUser(request):
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    return render(request, 'admin/users/tambahData.html', {'user' : user})

@login_required
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

@login_required
def updateDatauser(request, id_user):
    data_user = User.objects.get(id_user=id_user)
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_user': data_user,
        'user' : user
    }
    return render(request, 'admin/users/updateData.html', context)

@login_required
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

@login_required
def deleteDatauser(request, id_user):
    data_user = User.objects.get(id_user=id_user)
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_user': data_user,
        'user' : user
    }
    return render(request, 'admin/users/deleteData.html', context)

@login_required
def postDeleteuser(request, id_user):
    data_user = User.objects.get(id_user=id_user).delete()
    messages.success(request, 'Data User Berhasil Dihapus')

    return redirect('/indexUsers')


# Cerate Views For Guru CRUD
@login_required
def guru(request):
    data_guru = Guru.objects.all()
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_guru': data_guru,
        'user' : user
    }
    return render(request, 'admin/guru/index.html', context)

@login_required
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

@login_required
def detailGuru(request, nip):
    data_guru = Guru.objects.select_related('id_user').get(nip=nip)
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_guru': data_guru,
        'user' : user
    }
    return render(request, 'admin/guru/detail.html', context)

@login_required
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

@login_required
def deleteDataGuru(request, nip):
    data_guru = Guru.objects.get(nip=nip)
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_guru': data_guru,
        'user' : user
    }
    return render(request, 'admin/guru/deleteData.html', context)

@login_required
def postDeleteGuru(request, nip):
    data_guru = Guru.objects.get(nip=nip).delete()
    messages.success(request, 'Data Guru Berhasil Dihapus')

    return redirect('/indexGuru')


# Create Views For Kelas CRUD

@login_required
def kelas(request):
    jumlahSiswa = Siswa_Kelas.objects.values('id_kelas').annotate(jumlah_siswa=Count('nis_siswa'))
    data_kelas = Kelas.objects.all()
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'jumlahSiswa': jumlahSiswa,
        'data_kelas': data_kelas,
        'user' : user
    }
    return render(request, 'admin/kelas/index.html', context)


@login_required
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

@login_required
def updateDatakelas(request, id_kelas):
    if request.method == 'POST':
        nip_waliKelas = request.POST['nip_waliKelas']

        wali_kelas = Guru.objects.get(nip=nip_waliKelas)

        data_kelas = Kelas(
            id_kelas=request.POST['id_kelas'],
            nama_kelas=request.POST['nama_kelas'],
            nip_waliKelas=wali_kelas
        )
        data_kelas.save()
        list_siswa = request.POST.getlist('siswa[]')
        for nis_siswa in list_siswa:
            siswa = Siswa.objects.get(nis=nis_siswa)
            siswaKelas = Siswa_Kelas(
                nis_siswa=siswa,
                id_kelas=data_kelas,
            )
            siswaKelas.save()
        list_mapel = request.POST.getlist('mapel[]')
        list_guru = request.POST.getlist('guru[]')
        for m_id, g_nip in zip(list_mapel, list_guru):
            mapel = Mapel.objects.get(id_mapel=m_id)
            guru = Guru.objects.get(nip=g_nip)
            jadwal = Jadwal(
                nip_guru = guru,
                id_kelas = data_kelas,
                id_mapel = mapel
            )
            jadwal.save()
        messages.success(request,  'Data Kelas Berhasil Diupdate')
        return redirect('/indexKelas')
    else:
        data_mapel = Mapel.objects.all()
        data_siswa = Siswa.objects.all()
        data_kelas = Kelas.objects.select_related('nip_waliKelas').get(id_kelas=id_kelas)
        data_siswaKelas = Siswa_Kelas.objects.values_list('nis_siswa', flat=True)
        data_guru = Guru.objects.all()
        data_wali = Kelas.objects.values_list('nip_waliKelas', flat=True)
        id_user = request.session['id_user']
        user = User.objects.get(id_user = id_user)
        context = {
            'data_mapel' : data_mapel,
            'data_siswa' : data_siswa,
            'data_kelas': data_kelas,
            'data_siswaKelas' : data_siswaKelas,
            'data_wali': data_wali,
            'data_guru': data_guru,
            'user' : user
        }
        return render(request, 'admin/kelas/updateData.html', context)

@login_required
def deleteDataKelas(request, id_kelas):
    data_kelas = Kelas.objects.select_related('nip_waliKelas').get(id_kelas=id_kelas)
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_kelas': data_kelas,
        'user' : user
    }
    return render(request, 'admin/kelas/deleteData.html', context)

@login_required
def postDeleteKelas(request, id_kelas):
    data_kelas = Kelas.objects.select_related('nip_waliKelas').get(id_kelas=id_kelas).delete()
    messages.success(request, 'Data Kelas Berhasil Dihapus')

    return redirect('/indexKelas')

@login_required
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

@login_required
def mapel(request):
    data_mapel = Mapel.objects.all()
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_mapel': data_mapel,
        'user' : user
    }
    return render(request, 'admin/mapel/index.html', context)

@login_required
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

@login_required
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

@login_required
def deleteDataMapel(request, id_mapel):
    data_mapel = Mapel.objects.get(id_mapel=id_mapel)
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_mapel': data_mapel,
        'user' : user
    }
    return render(request, 'admin/mapel/deleteData.html', context)

@login_required
def postDeleteMapel(request, id_mapel):
    Mapel.objects.get(id_mapel=id_mapel).delete()
    messages.success(request, 'Data Mata pelajaran Berhasil Dihpaus')

    return redirect('/indexMapel')

# Cerate Views For Siswa CRUD

@login_required
def siswa(request):
    data_siswa = Siswa.objects.all()
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_siswa': data_siswa,
        'user' : user
    }
    return render(request, 'admin/siswa/index.html', context)

@login_required
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

@login_required
def detailSiswa(request, nis):
    data_siswa = Siswa.objects.select_related('id_user').get(nis=nis)
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_siswa': data_siswa,
        'user' : user
    }
    return render(request, 'admin/siswa/detail.html', context)

@login_required
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

@login_required
def deleteDataSiswa(request, nis):
    data_siswa = Siswa.objects.get(nis=nis)
    id_user = request.session['id_user']
    user = User.objects.get(id_user = id_user)
    context = {
        'data_siswa': data_siswa,
        'user' : user
    }
    return render(request, 'admin/siswa/deleteData.html', context)

@login_required
def postDeleteSiswa(request, nis):
    data_siswa = Siswa.objects.get(nis=nis).delete()
    messages.success(request, 'Data Siswa deleted successfully')

    return redirect('/indexSiswa')

@login_required
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

@login_required
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

#Create Views For Guru Pages
#Create Viewa For Guru Dashboard

def guruProfile(request):
    guru = Guru.objects.all()
    context = {
        'guru' : guru
    }
    return render(request, 'guru/guru.html', context)