"""
URL configuration for sp_kanker_diagnosa_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from sp_kanker_diagnosa_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # pasien CRUD
    path('pasien/', views.pasien_list, name='pasien_list'),
    path('pasien/tambah/', views.pasien_create, name='pasien_create'),
    path('pasien/<int:pk>/edit/', views.pasien_update, name='pasien_update'),
    path('pasien/<int:pk>/hapus/', views.pasien_delete, name='pasien_delete'),
    
    # Penyakit CRUD
    path('penyakit/', views.penyakit_list, name='penyakit_list'),
    path('penyakit/tambah/', views.penyakit_create, name='penyakit_create'),
    path('penyakit/<int:pk>/edit/', views.penyakit_update, name='penyakit_update'),
    path('penyakit/<int:pk>/hapus/', views.penyakit_delete, name='penyakit_delete'),

    # Gejala CRUD
    path('gejala/', views.gejala_list, name='gejala_list'),
    path('gejala/tambah/', views.gejala_create, name='gejala_create'),
    path('gejala/<int:pk>/edit/', views.gejala_update, name='gejala_update'),
    path('gejala/<int:pk>/hapus/', views.gejala_delete, name='gejala_delete'),

    # Basis Pengetahuan CRUD
    path('aturan/', views.aturan_list, name='aturan_list'),
    path('aturan/tambah/', views.aturan_create, name='aturan_create'),
    path('aturan/<int:pk>/edit/', views.aturan_update, name='aturan_update'),
    path('aturan/<int:pk>/hapus/', views.aturan_delete, name='aturan_delete'),

    # Diagnosa
    path('diagnosa/', views.diagnosa_list, name='diagnosa_list'),
    path('diagnosa/tambah/', views.diagnosa_create, name='diagnosa_create'),
    path('diagnosa/<int:pk>/edit/', views.diagnosa_update, name='diagnosa_update'),
    path('diagnosa/<int:pk>/hapus/', views.diagnosa_delete, name='diagnosa_delete'),

    # Gejala Diagnosa
    path('gejala/diagnosa/', views.gejala_diagnosa_list, name='gejala_diagnosa_list'),
    path('gejala/diagnosa/tambah/', views.gejala_diagnosa_create, name='gejala_diagnosa_create'),
    path('gejala/diagnosa/<int:pk>/edit/', views.gejala_diagnosa_update, name='gejala_diagnosa_update'),
    path('gejala/diagnosa/<int:pk>/hapus/', views.gejala_diagnosa_delete, name='gejala_diagnosa_delete'),

    # Hasil Diagnosa
    path('hasil/', views.hasil_list, name='hasil_list'),
    path('hasil/tambah/', views.hasil_create, name='hasil_create'),
    path('hasil/<int:pk>/edit/', views.hasil_update, name='hasil_update'),
    path('hasil/<int:pk>/hapus/', views.hasil_delete, name='hasil_delete'),
]
