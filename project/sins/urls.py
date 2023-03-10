from django.urls import path
from . views import admin, kelas, tambahKelas, postDatakelas

urlpatterns = [
   # path('',index,name='index'),
   path('admin',admin, name="admin"),
   path('indexKelas',kelas, name="indexkelas"),
   path('tambahKelas', tambahKelas, name="tambahkelas"),
   path('postDatakelas',postDatakelas, name="postdatakelas"),
]