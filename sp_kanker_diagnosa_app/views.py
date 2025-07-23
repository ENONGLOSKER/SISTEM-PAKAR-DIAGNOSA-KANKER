from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
from django.http import JsonResponse
from decimal import Decimal
from .forms import DiagnosaForm, GejalaDiagnosaForm
from django.forms import formset_factory
from .models import (
    Pasien, Penyakit, Gejala, BasisPengetahuan,
    Diagnosa, GejalaDiagnosa, HasilDS, PerhitunganDS
)
from .forms import (
    PenyakitForm, GejalaForm, BasisPengetahuanForm,
    DiagnosaForm, GejalaDiagnosaForm, HasilDSForm, PasienForm,
    PerhitunganDSForm, PencarianPasienForm, PencarianGejalaForm,
    PencarianPenyakitForm, DiagnosaStep1Form, DiagnosaStep2Form,
    DiagnosaStep3Form
)
from django.http import JsonResponse
from django.db.models.functions import TruncMonth
from django.db.models import F
from django.db.models.functions import TruncDate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login berhasil!")
            return redirect('dashboard')
        else:
            messages.error(request, "Username atau password salah.")
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form, 'title': 'Login'})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Anda telah logout.")
    return redirect('login_view')

# Dashboard
def index(request):
    return render(request, 'dashboard.html')

def dashboard(request):
    # Statistik dashboard
    total_pasien = Pasien.objects.count()
    total_penyakit = Penyakit.objects.count()
    total_gejala = Gejala.objects.count()
    total_diagnosa = Diagnosa.objects.count()
    total_aturan = BasisPengetahuan.objects.count()
    
    # Diagnosa terbaru
    diagnosa_terbaru = Diagnosa.objects.select_related('pasien').order_by('-tanggal')[:5]
    
    # Statistik jenis kelamin
    laki_laki_count = Pasien.objects.filter(jenis_kelamin='L').count()
    perempuan_count = Pasien.objects.filter(jenis_kelamin='P').count()
    
    # Penyakit berdasarkan tingkat keganasan
    penyakit_rendah = Penyakit.objects.filter(tingkat_keganasan='RENDAH').count()
    penyakit_sedang = Penyakit.objects.filter(tingkat_keganasan='SEDANG').count()
    penyakit_tinggi = Penyakit.objects.filter(tingkat_keganasan='TINGGI').count()
    
    #gejala
    gejala_list = Gejala.objects.order_by('id')
    pasien_list = Pasien.objects.all()

    # grafik penyakit
    # Ambil hanya hasil diagnosa dengan ranking 1
    hasil_utama = HasilDS.objects.filter(ranking=1)
    
    # Hitung jumlah kemunculan tiap penyakit
    data_grafik = hasil_utama.values('penyakit__nama').annotate(jumlah=Count('penyakit')).order_by('-jumlah')

    labels = [item['penyakit__nama'] for item in data_grafik]
    data = [item['jumlah'] for item in data_grafik]


    context = {
        'total_pasien': total_pasien,
        'total_penyakit': total_penyakit,
        'total_gejala': total_gejala,
        'total_diagnosa': total_diagnosa,
        'total_aturan': total_aturan,
        'diagnosa_terbaru': diagnosa_terbaru,
        'laki_laki_count': laki_laki_count,
        'perempuan_count': perempuan_count,
        'penyakit_rendah': penyakit_rendah,
        'penyakit_sedang': penyakit_sedang,
        'penyakit_tinggi': penyakit_tinggi,
        'gejala_list':gejala_list,
        'pasien_list':pasien_list,
        # grafik penyakit
        'labels': labels,
        'data': data
    }
    return render(request, 'dashboard.html', context)



def data_korelasi_gejala_penyakit(request):
    data = (
        BasisPengetahuan.objects
        .values('penyakit__nama')
        .annotate(jumlah_gejala=Count('gejala'))
        .order_by('-jumlah_gejala')
    )

    labels = [item['penyakit__nama'] for item in data]
    values = [item['jumlah_gejala'] for item in data]

    return JsonResponse({'labels': labels, 'data': values})

def data_distribusi_penyakit(request):
    data = (
        HasilDS.objects
        .filter(ranking=1)
        .values('penyakit__nama')
        .annotate(jumlah=Count('id'))
        .order_by('-jumlah')
    )

    labels = [item['penyakit__nama'] for item in data]
    values = [item['jumlah'] for item in data]

    return JsonResponse({'labels': labels, 'data': values})

def data_keparahan_gejala(request):
    data = (
        GejalaDiagnosa.objects
        .values('tingkat_keparahan')
        .annotate(jumlah=Count('id'))
        .order_by('tingkat_keparahan')
    )

    # Urutan tetap
    urutan = ['RINGAN', 'SEDANG', 'BERAT']
    label_map = {
        'RINGAN': 'Ringan',
        'SEDANG': 'Sedang',
        'BERAT': 'Berat'
    }

    hasil = {k: 0 for k in urutan}
    for item in data:
        hasil[item['tingkat_keparahan']] = item['jumlah']

    labels = [label_map[k] for k in urutan]
    values = [hasil[k] for k in urutan]

    return JsonResponse({'labels': labels, 'data': values})

def data_gender_pasien(request):
    data = (
        Pasien.objects
        .values('jenis_kelamin')
        .annotate(jumlah=Count('id'))
    )

    # Mapping untuk label
    label_map = {
        'L': 'Laki-laki',
        'P': 'Perempuan'
    }

    hasil = {'L': 0, 'P': 0}
    for item in data:
        hasil[item['jenis_kelamin']] = item['jumlah']

    labels = [label_map[k] for k in hasil.keys()]
    values = [hasil[k] for k in hasil.keys()]

    return JsonResponse({'labels': labels, 'data': values})

def data_tren_diagnosa_per_hari(request):
    data = (
        Diagnosa.objects
        .annotate(tanggal_hari=TruncDate('tanggal'))
        .values('tanggal_hari')
        .annotate(jumlah=Count('id'))
        .order_by('tanggal_hari')
    )

    labels = [item['tanggal_hari'].strftime('%d %b %Y') for item in data]
    values = [item['jumlah'] for item in data]

    return JsonResponse({'labels': labels, 'data': values})

def data_akurasi_diagnosa(request):
    # Ambil hanya hasil dengan ranking terbaik (1)
    hasil = HasilDS.objects.filter(ranking=1).values_list('nilai_kepercayaan', flat=True)

    # Buat kelompok (binning) manual
    bins = {
        '0–20%': 0,
        '21–40%': 0,
        '41–60%': 0,
        '61–80%': 0,
        '81–100%': 0
    }

    for nilai in hasil:
        if nilai <= 0.20:
            bins['0–20%'] += 1
        elif nilai <= 0.40:
            bins['21–40%'] += 1
        elif nilai <= 0.60:
            bins['41–60%'] += 1
        elif nilai <= 0.80:
            bins['61–80%'] += 1
        else:
            bins['81–100%'] += 1

    labels = list(bins.keys())
    values = list(bins.values())

    return JsonResponse({'labels': labels, 'data': values})

# ------------------ PASIEN ------------------
def pasien_list(request):
    # Pencarian dan filter
    search_form = PencarianPasienForm(request.GET)
    pasien_qs = Pasien.objects.all()
    
    if search_form.is_valid():
        nama = search_form.cleaned_data.get('nama')
        jenis_kelamin = search_form.cleaned_data.get('jenis_kelamin')
        
        if nama:
            pasien_qs = pasien_qs.filter(nama__icontains=nama)
        if jenis_kelamin:
            pasien_qs = pasien_qs.filter(jenis_kelamin=jenis_kelamin)
    
    # Pagination
    paginator = Paginator(pasien_qs.order_by('-dibuat'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistik
    pasien_count = pasien_qs.count()
    laki_laki_count = pasien_qs.filter(jenis_kelamin='L').count()
    perempuan_count = pasien_qs.filter(jenis_kelamin='P').count()
    
    context = {
        'page_obj': page_obj,
        'pasien_count': pasien_count,
        'laki_laki_count': laki_laki_count,
        'perempuan_count': perempuan_count,
        'search_form': search_form,
    }
    return render(request, 'pasien/list.html', context)

def pasien_create(request):
    if request.method == 'POST':
        form = PasienForm(request.POST)
        if form.is_valid():
            pasien = form.save()
            messages.success(request, f"Pasien {pasien.nama} berhasil ditambahkan.")
            return redirect('pasien_list')
    else:
        form = PasienForm()
    
    context = {
        'form': form,
        'form_name': 'Pasien',
        'form_fungsi': 'Tambah',
    }   
    return render(request, 'form/form.html', context)

def pasien_update(request, pk):
    pasien = get_object_or_404(Pasien, pk=pk)
    if request.method == 'POST':
        form = PasienForm(request.POST, instance=pasien)
        if form.is_valid():
            pasien = form.save()
            messages.success(request, f"Pasien {pasien.nama} berhasil diupdate.")
            return redirect('pasien_list')
    else:
        form = PasienForm(instance=pasien)
    
    context = {
        'form': form,
        'form_name': 'Pasien',
        'form_fungsi': 'Update',
        'object': pasien,
    }
    return render(request, 'form/form.html', context)

def pasien_delete(request, pk):
    pasien = get_object_or_404(Pasien, pk=pk)
    nama = pasien.nama
    pasien.delete()
    messages.success(request, f"Pasien {nama} berhasil dihapus.")
    return redirect('pasien_list')
    
def pasien_detail(request, pk):
    pasien = get_object_or_404(Pasien, pk=pk)
    diagnosa_list = pasien.diagnosa.all().order_by('-tanggal')
    
    context = {
        'pasien': pasien,
        'diagnosa_list': diagnosa_list,
    }
    return render(request, 'pasien/detail.html', context)

# ------------------ PENYAKIT ------------------
def penyakit_list(request):
    # Pencarian dan filter
    search_form = PencarianPenyakitForm(request.GET)
    penyakit_qs = Penyakit.objects.all()
    
    if search_form.is_valid():
        nama = search_form.cleaned_data.get('nama')
        tingkat_keganasan = search_form.cleaned_data.get('tingkat_keganasan')
        
        if nama:
            penyakit_qs = penyakit_qs.filter(nama__icontains=nama)
        if tingkat_keganasan:
            penyakit_qs = penyakit_qs.filter(tingkat_keganasan=tingkat_keganasan)
    
    # Pagination
    paginator = Paginator(penyakit_qs.order_by('nama'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistik
    penyakit_count = penyakit_qs.count()
    penyakit_rendah = penyakit_qs.filter(tingkat_keganasan='RENDAH').count()
    penyakit_sedang = penyakit_qs.filter(tingkat_keganasan='SEDANG').count()
    penyakit_tinggi = penyakit_qs.filter(tingkat_keganasan='TINGGI').count()
    
    context = {
        'page_obj': page_obj,
        'penyakit_count': penyakit_count,
        'penyakit_rendah': penyakit_rendah,
        'penyakit_sedang': penyakit_sedang,
        'penyakit_tinggi': penyakit_tinggi,
        'search_form': search_form,
    }
    return render(request, 'penyakit/list.html', context)

def penyakit_create(request):
    if request.method == 'POST':
        form = PenyakitForm(request.POST)
        if form.is_valid():
            penyakit = form.save()
            messages.success(request, f"Penyakit {penyakit.nama} berhasil ditambahkan.")
            return redirect('penyakit_list')
    else:
        form = PenyakitForm()
    
    context = {
        'form': form,
        'form_name': 'Penyakit',
        'form_fungsi': 'Tambah',
    }
    return render(request, 'form/form.html', context)

def penyakit_update(request, pk):
    penyakit = get_object_or_404(Penyakit, pk=pk)
    if request.method == 'POST':
        form = PenyakitForm(request.POST, instance=penyakit)
        if form.is_valid():
            penyakit = form.save()
            messages.success(request, f"Penyakit {penyakit.nama} berhasil diupdate.")
            return redirect('penyakit_list')
    else:
        form = PenyakitForm(instance=penyakit)
    
    context = {
        'form': form,
        'form_name': 'Penyakit',
        'form_fungsi': 'Update',
        'object': penyakit,
    }
    return render(request, 'form/form.html', context)

def penyakit_delete(request, pk):
    penyakit = get_object_or_404(Penyakit, pk=pk)
    if request.method == 'POST':
        nama = penyakit.nama
        penyakit.delete()
        messages.success(request, f"Penyakit {nama} berhasil dihapus.")
        return redirect('penyakit_list')
    
    context = {'object': penyakit}
    return render(request, 'penyakit/confirm_delete.html', context)

def penyakit_detail(request, pk):
    penyakit = get_object_or_404(Penyakit, pk=pk)
    basis_pengetahuan = penyakit.basis_pengetahuan.all().select_related('gejala')

    # staistik kategori gejal (umum, khusus, lanjutan)
    gejala_umum = basis_pengetahuan.filter(gejala__kategori='UMUM').count()
    gejala_khusus = basis_pengetahuan.filter(gejala__kategori='KHUSUS').count()
    gejala_lanjutan = basis_pengetahuan.filter(gejala__kategori='LANJUTAN').count()  

    context = {
        'penyakit': penyakit,
        'basis_pengetahuan': basis_pengetahuan,
        'gejala_umum': gejala_umum,
        'gejala_khusus': gejala_khusus,
        'gejala_lanjutan': gejala_lanjutan
    }
    return render(request, 'penyakit/detail.html', context)

# ------------------ GEJALA ------------------
def gejala_list(request):
    # Pencarian dan filter
    search_form = PencarianGejalaForm(request.GET)
    gejala_qs = Gejala.objects.all()
    
    if search_form.is_valid():
        nama = search_form.cleaned_data.get('nama')
        kategori = search_form.cleaned_data.get('kategori')
        
        if nama:
            gejala_qs = gejala_qs.filter(nama__icontains=nama)
        if kategori:
            gejala_qs = gejala_qs.filter(kategori=kategori)
    
    # Pagination
    paginator = Paginator(gejala_qs.order_by('dibuat'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistik
    gejala_count = gejala_qs.count()
    gejala_umum = gejala_qs.filter(kategori='UMUM').count()
    gejala_khusus = gejala_qs.filter(kategori='KHUSUS').count()
    gejala_lanjutan = gejala_qs.filter(kategori='LANJUTAN').count()
    
    context = {
        'page_obj': page_obj,
        'gejala_count': gejala_count,
        'gejala_umum': gejala_umum,
        'gejala_khusus': gejala_khusus,
        'gejala_lanjutan': gejala_lanjutan,
        'search_form': search_form,
    }
    return render(request, 'gejala/list.html', context)

def gejala_create(request):
    if request.method == 'POST':
        form = GejalaForm(request.POST)
        if form.is_valid():
            gejala = form.save()
            messages.success(request, f"Gejala {gejala.nama} berhasil ditambahkan.")
            return redirect('gejala_list')
    else:
        form = GejalaForm()
    
    context = {
        'form': form,
        'form_name': 'Gejala',
        'form_fungsi': 'Tambah'
    }
    return render(request, 'form/form.html', context)

def gejala_update(request, pk):
    gejala = get_object_or_404(Gejala, pk=pk)
    if request.method == 'POST':
        form = GejalaForm(request.POST, instance=gejala)
        if form.is_valid():
            gejala = form.save()
            messages.success(request, f"Gejala {gejala.nama} berhasil diupdate.")
            return redirect('gejala_list')
    else:
        form = GejalaForm(instance=gejala)
    
    context = {
        'form': form,
        'form_name': 'Gejala',
        'form_fungsi': 'Update',
        'object': gejala,
    }
    return render(request, 'form/form.html', context)

def gejala_delete(request, pk):
    gejala = get_object_or_404(Gejala, pk=pk)
    nama = gejala.nama
    gejala.delete()
    messages.success(request, f"Gejala {nama} berhasil dihapus.")
    return redirect('gejala_list')
def gejala_detail(request, pk):
    gejala = get_object_or_404(Gejala, pk=pk)
    basis_pengetahuan = gejala.basis_pengetahuan.all().select_related('penyakit')
    
    context = {
        'gejala': gejala,
        'basis_pengetahuan': basis_pengetahuan,
    }
    return render(request, 'gejala/detail.html', context)

# ------------------ ATURAN (Basis Pengetahuan) ------------------
def aturan_list(request):
    aturan_qs = BasisPengetahuan.objects.select_related('gejala', 'penyakit').all()
    
    # Pagination
    paginator = Paginator(aturan_qs.order_by('penyakit', 'gejala'), 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'aturan_count': aturan_qs.count(),
    }
    return render(request, 'aturan/list.html', context)

def aturan_create(request):
    if request.method == 'POST':
        form = BasisPengetahuanForm(request.POST)
        if form.is_valid():
            aturan = form.save()
            messages.success(request, f"Aturan {aturan.gejala.nama} → {aturan.penyakit.nama} berhasil ditambahkan.")
            return redirect('aturan_list')
    else:
        form = BasisPengetahuanForm()
    
    context = {
        'form': form,
        'form_name': 'Basis Pengetahuan',
        'form_fungsi': 'Tambah',
    }
    return render(request, 'form/form.html', context)

def aturan_update(request, pk):
    aturan = get_object_or_404(BasisPengetahuan, pk=pk)
    if request.method == 'POST':
        form = BasisPengetahuanForm(request.POST, instance=aturan)
        if form.is_valid():
            aturan = form.save()
            messages.success(request, f"Aturan {aturan.gejala.nama} → {aturan.penyakit.nama} berhasil diupdate.")
            return redirect('aturan_list')
    else:
        form = BasisPengetahuanForm(instance=aturan)
    
    context = {
        'form': form,
        'form_name': 'Basis Pengetahuan',
        'form_fungsi': 'Update',
        'object': aturan,
    }
    return render(request, 'form/form.html', context)

def aturan_delete(request, pk):
    aturan = get_object_or_404(BasisPengetahuan, pk=pk)
    if request.method == 'POST':
        gejala_penyakit = f"{aturan.gejala.nama} → {aturan.penyakit.nama}"
        aturan.delete()
        messages.success(request, f"Aturan {gejala_penyakit} berhasil dihapus.")
        return redirect('aturan_list')
    
    context = {'object': aturan}
    return render(request, 'aturan/confirm_delete.html', context)

# ------------------ DIAGNOSA ------------------
def diagnosa_list(request):
    diagnosa_qs = Diagnosa.objects.select_related('pasien').all()
    
    # Pagination
    paginator = Paginator(diagnosa_qs.order_by('-tanggal'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'diagnosa_count': diagnosa_qs.count(),
    }
    return render(request, 'diagnosa/list.html', context)

def diagnosa_update(request, pk):
    diagnosa = get_object_or_404(Diagnosa, pk=pk)
    if request.method == 'POST':
        form = DiagnosaForm(request.POST, instance=diagnosa)
        if form.is_valid():
            diagnosa = form.save()
            messages.success(request, f"Diagnosa berhasil diupdate.")
            return redirect('diagnosa_detail', pk=diagnosa.pk)
    else:
        form = DiagnosaForm(instance=diagnosa)
    
    context = {
        'form': form,
        'form_name': 'Diagnosa',
        'form_fungsi': 'Update',
        'object': diagnosa,
    }
    return render(request, 'form/form.html', context)

def diagnosa_delete(request, pk):
    diagnosa = get_object_or_404(Diagnosa, pk=pk)
    pasien_id = diagnosa.pasien_id
    diagnosa.delete()
    messages.success(request, "Diagnosa berhasil dihapus.")
    return redirect('pasien_detail', pk=pasien_id)

def diagnosa_detail(request, pk):
    diagnosa = get_object_or_404(Diagnosa, pk=pk)
    gejala_terpilih = diagnosa.gejala_terpilih.all().select_related('gejala')
    hasil_ds = diagnosa.hasil_ds.all().select_related('penyakit').order_by('-nilai_kepercayaan')
    perhitungan_ds = diagnosa.perhitungan_ds.all().select_related('gejala', 'penyakit')
    
    context = {
        'diagnosa': diagnosa,
        'gejala_terpilih': gejala_terpilih,
        'hasil_ds': hasil_ds,
        'perhitungan_ds': perhitungan_ds,
    }
    return render(request, 'diagnosa/detail.html', context)

# ------------------ DWTAIL GEJALA DIAGNOSA ------------------
def gejala_diagnosa_list(request):
    gejala_diagnosa_qs = GejalaDiagnosa.objects.select_related('diagnosa', 'gejala').all()
    
    # Pagination
    paginator = Paginator(gejala_diagnosa_qs.order_by('-dipilih_pada'), 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'gejala_diagnosa_count': gejala_diagnosa_qs.count(),
    }
    return render(request, 'diagnosa_gejala/list.html', context)


def gejala_diagnosa_update(request, pk):
    gejala_diagnosa = get_object_or_404(GejalaDiagnosa, pk=pk)
    if request.method == 'POST':
        form = GejalaDiagnosaForm(request.POST, instance=gejala_diagnosa)
        if form.is_valid():
            gejala_diagnosa = form.save()
            messages.success(request, f"Gejala {gejala_diagnosa.gejala.nama} berhasil diupdate.")
            return redirect('gejala_diagnosa_list')
    else:
        form = GejalaDiagnosaForm(instance=gejala_diagnosa)
    
    context = {
        'form': form,
        'form_name': 'Gejala Diagnosa',
        'form_fungsi': 'Update',
        'object': gejala_diagnosa,
    }
    return render(request, 'form/form.html', context)

def gejala_diagnosa_delete(request, pk):
    gejala_diagnosa = get_object_or_404(GejalaDiagnosa, pk=pk)
    if request.method == 'POST':
        nama_gejala = gejala_diagnosa.gejala.nama
        gejala_diagnosa.delete()
        messages.success(request, f"Gejala {nama_gejala} berhasil dihapus dari diagnosa.")
        return redirect('gejala_diagnosa_list')
    
    context = {'object': gejala_diagnosa}
    return render(request, 'gejala_diagnosa/confirm_delete.html', context)

# ------------------ HASIL DS ------------------
def hasil_list(request):
    hasil_qs = HasilDS.objects.select_related('diagnosa', 'penyakit').all()

    # jumlah
    total_hasil = hasil_qs.count()
    total_positif = hasil_qs.filter(nilai_kepercayaan__gte=0.5).count()
    total_negatif = hasil_qs.filter(nilai_kepercayaan__lt=0.5).count()
    
    # Pagination
    paginator = Paginator(hasil_qs.order_by('-nilai_kepercayaan'), 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'hasil_count': hasil_qs.count(),
        'total_hasil': total_hasil,
        'total_positif': total_positif,
        'total_negatif': total_negatif,
    }
    return render(request, 'hasil/list.html', context)


def hasil_update(request, pk):
    hasil = get_object_or_404(HasilDS, pk=pk)
    if request.method == 'POST':
        form = HasilDSForm(request.POST, instance=hasil)
        if form.is_valid():
            hasil = form.save()
            messages.success(request, f"Hasil DS untuk {hasil.penyakit.nama} berhasil diupdate.")
            return redirect('hasil_list')
    else:
        form = HasilDSForm(instance=hasil)
    
    context = {
        'form': form,
        'form_name': 'Hasil DS',
        'form_fungsi': 'Update',
        'object': hasil,
    }
    return render(request, 'hasil/form.html', context)

def hasil_delete(request, pk):
    hasil = get_object_or_404(HasilDS, pk=pk)
    if request.method == 'POST':
        nama_penyakit = hasil.penyakit.nama
        hasil.delete()
        messages.success(request, f"Hasil DS untuk {nama_penyakit} berhasil dihapus.")
        return redirect('hasil_list')
    
    context = {'object': hasil}
    return render(request, 'hasil/confirm_delete.html', context)

# ------------------ PERHITUNGAN DS ------------------
'''
pada fungsi ini akan memproses gejala diagnosa menggunakan metode Dempster-Shafer secara otomatis
'''

# ------------------ PROSES DIAGNOSA ------------------
def proses_diagnosa(request):
    """
    View untuk memproses diagnosa dari modal
    """
    if request.method == 'POST':
        try:
            # Ambil data dari form
            pasien_id = request.POST.get('pasien_id')
            gejala_ids = request.POST.getlist('gejala_ids')
            
            # Validasi input            
            if not gejala_ids:
                return JsonResponse({
                    'success': False,
                    'message': 'Pilih minimal satu gejala'
                })
            
            # Buat diagnosa baru
            diagnosa = Diagnosa.objects.create(
                pasien_id=pasien_id if pasien_id else None,
                status='PROSES',
                total_gejala=len(gejala_ids)
            )
            
            # Simpan gejala yang dipilih
            for gejala_id in gejala_ids:
                gejala = Gejala.objects.get(id=gejala_id)
                
                # Ambil data tambahan untuk gejala ini
                tingkat_keparahan = request.POST.get(f'tingkat_keparahan_{gejala_id}', 'SEDANG')
                durasi = request.POST.get(f'durasi_{gejala_id}', '')
                bobot_pengguna = request.POST.get(f'bobot_pengguna_{gejala_id}', '1.0000')
                catatan = request.POST.get(f'catatan_{gejala_id}', '')
                
                GejalaDiagnosa.objects.create(
                    diagnosa=diagnosa,
                    gejala=gejala,
                    tingkat_keparahan=tingkat_keparahan,
                    durasi=durasi,
                    bobot_pengguna=bobot_pengguna,
                    catatan=catatan
                )
            
            # Proses perhitungan Dempster-Shafer
            hasil_perhitungan = hitung_dempster_shafer(diagnosa)
            
            if hasil_perhitungan['success']:
                # Update status diagnosa menjadi selesai
                diagnosa.status = 'SELESAI'
                diagnosa.save()
                
                # return JsonResponse({
                #     'success': True,
                #     'redirect_url': f'/diagnosa/{diagnosa.id}/',
                #     'message': 'Diagnosa berhasil diproses'
                # })
                return redirect('dashboard')
            else:
                # Jika gagal, hapus diagnosa yang dibuat
                diagnosa.delete()
                return JsonResponse({
                    'success': False,
                    'message': hasil_perhitungan['message']
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Terjadi kesalahan: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Method tidak diizinkan'
    })

def hitung_dempster_shafer(diagnosa):
    """
    Fungsi untuk menghitung diagnosa menggunakan metode Dempster-Shafer
    """
    try:
        # Ambil gejala yang dipilih
        gejala_terpilih = diagnosa.gejala_terpilih.all()
        
        if not gejala_terpilih.exists():
            return {
                'success': False,
                'message': 'Tidak ada gejala yang dipilih'
            }
        
        # Ambil semua penyakit yang ada
        penyakit_list = Penyakit.objects.all()
        
        if not penyakit_list.exists():
            return {
                'success': False,
                'message': 'Tidak ada data penyakit yang tersedia'
            }
        
        # Dictionary untuk menyimpan hasil perhitungan
        hasil_perhitungan = {}
        
        # Proses perhitungan untuk setiap penyakit
        for penyakit in penyakit_list:
            # Ambil basis pengetahuan untuk penyakit ini
            basis_pengetahuan = BasisPengetahuan.objects.filter(penyakit=penyakit)
            
            if not basis_pengetahuan.exists():
                continue
            
            # Inisialisasi nilai kepercayaan dan ketidakpercayaan
            belief = Decimal('0.0000')
            disbelief = Decimal('0.0000')
            uncertainty = Decimal('1.0000')
            
            # Proses gejala yang dipilih
            for gejala_diagnosa in gejala_terpilih:
                # Cari basis pengetahuan untuk gejala ini
                bp = basis_pengetahuan.filter(gejala=gejala_diagnosa.gejala).first()
                
                if bp:
                    # Ambil bobot dari basis pengetahuan
                    m1 = bp.bobot_kepercayaan
                    m2 = Decimal('1.0000') - m1  # ketidakpercayaan
                    
                    # Ambil bobot pengguna
                    bobot_pengguna = gejala_diagnosa.bobot_pengguna
                    
                    # Kombinasi bobot
                    combined_belief = m1 * bobot_pengguna
                    combined_disbelief = m2 * bobot_pengguna
                    
                    # Update nilai
                    belief += combined_belief
                    disbelief += combined_disbelief
            
            # Normalisasi nilai
            total = belief + disbelief
            if total > 0:
                belief = belief / total
                disbelief = disbelief / total
                uncertainty = Decimal('1.0000') - belief - disbelief
            
            # Simpan hasil
            hasil_perhitungan[penyakit.id] = {
                'belief': belief,
                'disbelief': disbelief,
                'uncertainty': uncertainty
            }
        
        # Urutkan hasil berdasarkan nilai kepercayaan
        sorted_results = sorted(
            hasil_perhitungan.items(),
            key=lambda x: x[1]['belief'],
            reverse=True
        )
        
        # Simpan hasil ke database
        for ranking, (penyakit_id, hasil) in enumerate(sorted_results, 1):
            penyakit = Penyakit.objects.get(id=penyakit_id)
            
            HasilDS.objects.create(
                diagnosa=diagnosa,
                penyakit=penyakit,
                nilai_kepercayaan=hasil['belief'],
                nilai_ketidakpercayaan=hasil['disbelief'],
                nilai_uncertainty=hasil['uncertainty'],
                ranking=ranking,
                rekomendasi=f"Berdasarkan gejala yang dipilih, kemungkinan {penyakit.nama} sebesar {hasil['belief']:.2%}"
            )
        
        return {
            'success': True,
            'message': 'Perhitungan berhasil',
            'redirect_url': f'/pasien/{diagnosa.pasien.id}/' if diagnosa.pasien_id else '/'
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Error dalam perhitungan: {str(e)}'
        }
