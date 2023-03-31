from django.shortcuts import render, redirect
from .models import User, Guru, Kelas, Siswa
from django.contrib import messages

# Views For Admin Pages


def admin(request):
    data_guru = Guru.objects.count()
    data_siswa = Siswa.objects.count()
    data_kelas = Kelas.objects.count()
    context = {
        'data_guru': data_guru,
        'data_siswa': data_siswa,
        'data_kelas': data_kelas
    }
    return render(request, 'admin/admin.html', context)

# Create Views For Users CRUD


def users(request):
    data_user = User.objects.all()
    context = {
        'data_user': data_user
    }
    return render(request, 'admin/users/index.html', context)

def tambahUser(request):
    return render(request, 'admin/users/tambahData.html')

def postDatauser(request):

    id_user = request.POST['id_user']
    username = request.POST['username']
    password = request.POST['password']
    password2 = request.POST['password2']
    role = request.POST['role']

    if User.objects.filter(id_user=id_user).exists():
        messages.error(request, 'User is already exists')
    else:
        if password == password2:
            tambah_user = User(
                id_user=id_user,
                username=username,
                password=password,
                role=role,
            )
            tambah_user.save()
            messages.success(request, 'User saved successfully')
        else:
            messages.error(request, 'User do not match')
    return redirect('/indexUsers')

def updateDatauser(request, id_user):
    data_user = User.objects.get(id_user=id_user)
    context = {
        'data_user': data_user
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
        messages.success(request, 'User Update successfully')
    else:
        messages.error(request, 'User not do match password')
    return redirect('/indexUsers')

def deleteDatauser(request, id_user):
    data_user = User.objects.get(id_user=id_user)
    context = {
        'data_user': data_user
    }
    return render(request, 'admin/users/deleteData.html', context)

def postDeleteuser(request, id_user):
    data_user = User.objects.get(id_user=id_user).delete()
    messages.success(request, 'User deleted successfully')

    return redirect('/indexUsers')


# Cerate Views For Guru CRUD
def guru(request):
    data_guru = Guru.objects.all()
    context = {
        'data_guru': data_guru
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
        
        user = User.objects.get(id_user = id_user)
        
        if Guru.objects.filter(nip = nip).exists():
            messages.error(request, 'Data is already exists')
        else:
            data_guru = Guru(
            nip = nip,
            nama = nama,
            jk = jk,
            alamat = alamat,
            agama = agama,
            no_tlpn = no_tlpn,
            email = email,
            tgl_lahir = tgl_lahir,
            foto = foto,
            id_user = user,
            )
            data_guru.save()
            messages.success(request,  ' Data is successfully saved')
        return redirect('/indexGuru')
    else:
        users = User.objects.all()
        data_userGuru = Guru.objects.values_list('id_user', flat=True)
        context = {
            'users': users,
            'data_userGuru' : data_userGuru
        }
        return render(request, 'admin/guru/tambahData.html', context)
    
def detailGuru(request, nip):
    data_wali = Kelas.objects.values_list('nip_waliKelas', flat=True)
    data_guru = Guru.objects.select_related('id_user').get(nip = nip)
    context = {
        'data_wali' : data_wali,
        'data_guru':data_guru
    }
    return render(request, 'admin/guru/detail.html', context)

def updateDataGuru(request, nip):
    if request.method == 'POST':
        id_user = request.POST['id_user']

        user = User.objects.get(id_user = id_user)

        data_guru = Guru(
        nip = request.POST['nip'],
        nama = request.POST['nama'],
        jk = request.POST['jk'],
        alamat = request.POST['alamat'],
        agama = request.POST['agama'],
        no_tlpn = request.POST['no_tlpn'],
        email = request.POST['email'],
        tgl_lahir = request.POST['tgl_lahir'],
        foto = request.FILES['foto'],
        id_user = user,
        )
        data_guru.save()
        messages.success(request,  ' Data is successfully saved')
        return redirect('/indexGuru')
    else:
        data_guru = Guru.objects.select_related('id_user').get(nip = nip)
        users = User.objects.all()
        data_userGuru = Guru.objects.values_list('id_user', flat=True)
        context = {
            'data_guru' : data_guru,
            'users' : users,
            'data_userGuru' : data_userGuru,
        }
        return render(request, 'admin/guru/updateData.html', context)
    
def deleteDataGuru(request, nip):
    data_guru = Guru.objects.get(nip = nip)
    context = {
        'data_guru' : data_guru
    }
    return render(request, 'admin/guru/deleteData.html', context)

def postDeleteGuru(request, nip):
    data_guru = Guru.objects.get(nip = nip).delete()
    messages.success(request, 'Data Guru deleted successfully')

    return redirect('/indexGuru')
    

# Create Views For Kelas CRUD

def kelas(request):
    data_kelas = Kelas.objects.all()
    context = {
        'data_kelas': data_kelas
    }
    return render(request, 'admin/kelas/index.html', context)

def tambahKelas(request):
    if request.method == 'POST':
        id_kelas = request.POST['id_kelas']
        nama_kelas = request.POST['nama_kelas']
        nip_waliKelas = request.POST['nip_waliKelas']

        wali_kelas = Guru.objects.get(nip = nip_waliKelas)

        if Kelas.objects.filter(id_kelas = id_kelas).exists():
            messages.error(request, 'ID Kelas is already exists')
        else :
            data_kelas = Kelas(
                id_kelas = id_kelas,
                nama_kelas = nama_kelas,
                nip_waliKelas = wali_kelas
            )
            data_kelas.save()
            messages.success(request, 'Kelas saved successfully')

        kelas_guru = Kelas.objects.select_related('nip_waliKelas').all()
        return redirect('/indexKelas')
    else:
        data_guru = Guru.objects.all()
        data_waliKelas = Kelas.objects.values_list('nip_waliKelas', flat=True)
        context = {
            'data_guru': data_guru,
            'data_waliKelas': data_waliKelas
        }
        return render(request, 'admin/kelas/tambahData.html', context)

def updateDatakelas(request, id_kelas): 
    if request.method == 'POST':
        nip_waliKelas = request.POST['nip_waliKelas']

        wali_kelas = Guru.objects.get(nip = nip_waliKelas)

        data_kelas = Kelas(
            id_kelas = request.POST['id_kelas'],
            nama_kelas = request.POST['nama_kelas'],
            nip_waliKelas = wali_kelas
        )
        data_kelas.save()
        messages.success(request,  ' Data is successfully saved')
        return redirect('/indexKelas')
    else:
        data_kelas = Kelas.objects.select_related('nip_waliKelas').get(id_kelas = id_kelas)
        data_guru = Guru.objects.all()
        data_wali = Kelas.objects.values_list('nip_waliKelas', flat=True)
        context = {
            'data_kelas': data_kelas,
            'data_wali': data_wali,
            'data_guru': data_guru,
        }
        return render(request, 'admin/kelas/updateData.html', context)

def deleteDataKelas(request, id_kelas):
    data_kelas = Kelas.objects.select_related('nip_waliKelas').get(id_kelas = id_kelas)
    context = {
        'data_kelas': data_kelas
    }
    return render(request, 'admin/kelas/deleteData.html', context)

def postDeleteKelas(request, id_kelas):
    data_kelas = Kelas.objects.select_related('nip_waliKelas').get(id_kelas = id_kelas).delete()
    messages.success(request, 'Data Kelas deleted successfully')

    return redirect('/indexKelas')