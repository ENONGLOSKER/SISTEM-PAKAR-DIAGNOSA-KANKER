from django.contrib import admin
from django.urls import path
from sp_kanker_diagnosa_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Pasien
    path('pasien/', views.pasien_list, name='pasien_list'),
    path('pasien/tambah/', views.pasien_create, name='pasien_create'),
    path('pasien/<int:pk>/edit/', views.pasien_update, name='pasien_update'),
    path('pasien/<int:pk>/hapus/', views.pasien_delete, name='pasien_delete'),
    path('pasien/<int:pk>/', views.pasien_detail, name='pasien_detail'),

    # Penyakit
    path('penyakit/', views.penyakit_list, name='penyakit_list'),
    path('penyakit/tambah/', views.penyakit_create, name='penyakit_create'),
    path('penyakit/<int:pk>/edit/', views.penyakit_update, name='penyakit_update'),
    path('penyakit/<int:pk>/hapus/', views.penyakit_delete, name='penyakit_delete'),
    path('penyakit/<int:pk>/', views.penyakit_detail, name='penyakit_detail'),

    # Gejala
    path('gejala/', views.gejala_list, name='gejala_list'),
    path('gejala/tambah/', views.gejala_create, name='gejala_create'),
    path('gejala/<int:pk>/edit/', views.gejala_update, name='gejala_update'),
    path('gejala/<int:pk>/hapus/', views.gejala_delete, name='gejala_delete'),
    path('gejala/<int:pk>/', views.gejala_detail, name='gejala_detail'),

    # Basis Pengetahuan (Aturan)
    path('aturan/', views.aturan_list, name='aturan_list'),
    path('aturan/tambah/', views.aturan_create, name='aturan_create'),
    path('aturan/<int:pk>/edit/', views.aturan_update, name='aturan_update'),
    path('aturan/<int:pk>/hapus/', views.aturan_delete, name='aturan_delete'),

    # Diagnosa
    path('diagnosa/', views.diagnosa_list, name='diagnosa_list'),
    path('diagnosa/<int:pk>/edit/', views.diagnosa_update, name='diagnosa_update'),
    path('diagnosa/<int:pk>/hapus/', views.diagnosa_delete, name='diagnosa_delete'),
    path('diagnosa/<int:pk>/', views.diagnosa_detail, name='diagnosa_detail'),

    # Gejala Diagnosa
    path('gejala/diagnosa/', views.gejala_diagnosa_list, name='gejala_diagnosa_list'),
    path('gejala/diagnosa/<int:pk>/edit/', views.gejala_diagnosa_update, name='gejala_diagnosa_update'),
    path('gejala/diagnosa/<int:pk>/hapus/', views.gejala_diagnosa_delete, name='gejala_diagnosa_delete'),

    # Hasil Diagnosa
    path('hasil/', views.hasil_list, name='hasil_list'),
    path('hasil/<int:pk>/edit/', views.hasil_update, name='hasil_update'),
    path('hasil/<int:pk>/hapus/', views.hasil_delete, name='hasil_delete'),

    # proses
    path('diagnosa/<int:pk>/', views.diagnosa_detail, name='diagnosa_detail'),
    
    # Proses diagnosa dari modal
    path('proses-diagnosa/', views.proses_diagnosa, name='proses_diagnosa'),

]
