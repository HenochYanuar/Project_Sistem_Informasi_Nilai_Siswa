from django.urls import path
from . views import admin, users, tambahUser, postDatauser, updateDatauser, postUpdateuser, deleteDatauser, postDeleteuser, kelas, tambahKelas, postDatakelas, updateDatakelas

urlpatterns = [
   # path('',index,name='index'),
   
   # Url For admin/user page
   path('admin',admin, name="admin"),
   path('indexUsers',users, name="indexusers"),
   path('tambahUser', tambahUser, name="tambahuser"),
   path('postDatauser', postDatauser, name="postdatauser"),
   path('updateDatauser/<str:id_user>', updateDatauser, name="updatedatauser"),
   path('postUpdateuser', postUpdateuser, name="postupdatedatauser"),
   path('deleteDatauser/<str:id_user>', deleteDatauser, name="deletedatauser"),
   path('postDeleteuser/<str:id_user>', postDeleteuser, name="postdeleteuser"),



   path('indexKelas',kelas, name="indexkelas"),
   path('tambahKelas', tambahKelas, name="tambahkelas"),
   path('postDatakelas',postDatakelas, name="postdatakelas"),
   path('updateDatakelas',updateDatakelas, name="updatedatakelas"),
]