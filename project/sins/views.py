from django.shortcuts import render, redirect
from .models import Kelas
from django.contrib import messages

# Create your views here.

def admin(request):
    return render(request,'admin/admin.html')

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

