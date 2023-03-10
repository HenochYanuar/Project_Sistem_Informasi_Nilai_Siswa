from django.shortcuts import render
from .models import Kelas

# Create your views here.

def index(request):
    return render(request,'index.html')

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