from django.urls import path
from . views import admin
from . views import users, tambahUser, postDatauser, updateDatauser, postUpdateuser, deleteDatauser, postDeleteuser
from . views import guru , tambahGuru, detailGuru, updateDataGuru, deleteDataGuru, postDeleteGuru
from . views import kelas, tambahKelas, postDatakelas, updateDatakelas
urlpatterns = [
   # path('',index,name='index'),
   
   
   path('admin',admin, name="admin"),

   # Url For admin/user page
   path('indexUsers',users, name="indexusers"),
   path('tambahUser', tambahUser, name="tambahuser"),
   path('postDatauser', postDatauser, name="postdatauser"),
   path('updateDatauser/<str:id_user>', updateDatauser, name="updatedatauser"),
   path('postUpdateuser', postUpdateuser, name="postupdatedatauser"),
   path('deleteDatauser/<str:id_user>', deleteDatauser, name="deletedatauser"),
   path('postDeleteuser/<str:id_user>', postDeleteuser, name="postdeleteuser"),

   # Url For admin/guru page
   path('indexGuru', guru, name="indexguru"),
   path('tambahGuru', tambahGuru, name="tambahguru"),
   path('detailGuru/<str:nip>', detailGuru, name="detailguru"),
   path('updateDataGuru/<str:nip>', updateDataGuru, name="updatedataguru"),
   path('deleteDataGuru/<str:nip>', deleteDataGuru, name="deletedataguru"),
   path('postDeleteGuru/<str:nip>', postDeleteGuru, name="postdeleteguru"),

   path('indexKelas',kelas, name="indexkelas"),
   path('tambahKelas', tambahKelas, name="tambahkelas"),
   path('postDatakelas',postDatakelas, name="postdatakelas"),
   path('updateDatakelas',updateDatakelas, name="updatedatakelas"),
]