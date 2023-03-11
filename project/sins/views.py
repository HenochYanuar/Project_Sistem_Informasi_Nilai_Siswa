from django.shortcuts import render, redirect
from .models import User, Kelas
from django.contrib import messages

# Create Views For Users CRUD
def admin(request):
    return render(request,'admin/admin.html')

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
        messages.error(request, 'User already exists')
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

def  postDeleteuser(request, id_user):
    data_user = User.objects.get(id_user=id_user).delete()
    messages.success(request, 'User deleted successfully')

    return redirect('/indexUsers')




# Create Views For Kelas CRUD

def kelas(request):
    data_kelas = Kelas.objects.all()
    context = {
        'data_kelas': data_kelas
    }
    return render(request, 'admin/kelas/index.html', context)

def tambahKelas(request):
    return render(request, 'admin/kelas/tambahData.html')

def postDatakelas(request):
    id_kelas = request.POST['id_kelas']
    nama_kelas = request.POST['nama_kelas']
    nip_waliKelas = request.POST['nip_waliKelas']

    if Kelas.objects.filter(id_kelas=id_kelas).exists():
        messages.error(request,'Kelas already exists')
    else:
        tambah_kelas = Kelas(
            id_kelas=id_kelas,
            nama_kelas = nama_kelas,
            nip_waliKelas = nip_waliKelas,
        )
        tambah_kelas.save()
        messages.success(request,'Kelas successfully saved')
    return redirect('/admin/kelas/index')

def updateDatakelas(request, kelas_id):
    data_kelas = Kelas.objects.all(kelas_id=kelas_id)
    context = {
        'data_kelas': data_kelas
    }
    return render(request, 'admin/kelas/updateData.html', context)
