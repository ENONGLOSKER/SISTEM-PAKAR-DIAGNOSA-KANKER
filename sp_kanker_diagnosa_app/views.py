from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import (
    Pasien, Penyakit, Gejala, BasisPengetahuan,
    Diagnosa, GejalaDiagnosa, HasilDS, Pasien
)
from .forms import (
    PenyakitForm, GejalaForm, BasisPengetahuanForm,
    DiagnosaForm, GejalaDiagnosaForm, HasilDSForm, PasienForm
)

# Dashboard
def index(request):
    return render(request, 'dashboard.html')

def dashboard(request):
    return render(request, 'dashboard.html')

# ------------------ PASIEN ------------------
def pasien_list(request):
    # Ambil semua data pasien
    pasien_qs = Pasien.objects.all().order_by('-id')
    # Hitung total pasien
    pasien_count = pasien_qs.count()
    # Ambil 5 pasien terakhir untuk highlight
    pasien_terbaru = pasien_qs[:5]
    # Data statistik tambahan (misal: jumlah pasien laki-laki & perempuan)
    laki_laki_count = pasien_qs.filter(jenis_kelamin='L').count()
    perempuan_count = pasien_qs.filter(jenis_kelamin='P').count()
    context = {
        'pasien_list': pasien_qs,
        'pasien_count': pasien_count,
        'pasien_terbaru': pasien_terbaru,
        'laki_laki_count': laki_laki_count,
        'perempuan_count': perempuan_count,
    }
    return render(request, 'pasien/list.html', context)

def pasien_create(request):
    if request.method == 'POST':
        form = PasienForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pasien berhasil ditambahkan.")
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
            form.save()
            messages.success(request, "Pasien berhasil diupdate.")
            return redirect('pasien_list')
    else:
        form = PasienForm(instance=pasien)
    context = {'form': form}
    return render(request, 'form/form.html', context)

def pasien_delete(request, pk):
    pasien = get_object_or_404(Pasien, pk=pk)
    pasien.delete()
    messages.success(request, "Pasien berhasil dihapus.")
    return redirect('pasien_list')

# ------------------ PENYAKIT ------------------
def penyakit_list(request):
    context = {
        'penyakit_list': Penyakit.objects.all()
    }
    return render(request, 'penyakit/list.html', context)

def penyakit_create(request):
    if request.method == 'POST':
        form = PenyakitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Penyakit berhasil ditambahkan.")
            return redirect('penyakit_list')
    else:
        form = PenyakitForm()
    context = {'form': form}
    return render(request, 'penyakit/form.html', context)

def penyakit_update(request, pk):
    penyakit = get_object_or_404(Penyakit, pk=pk)
    if request.method == 'POST':
        form = PenyakitForm(request.POST, instance=penyakit)
        if form.is_valid():
            form.save()
            messages.success(request, "Penyakit berhasil diupdate.")
            return redirect('penyakit_list')
    else:
        form = PenyakitForm(instance=penyakit)
    context = {'form': form}
    return render(request, 'penyakit/form.html', context)

def penyakit_delete(request, pk):
    penyakit = get_object_or_404(Penyakit, pk=pk)
    if request.method == 'POST':
        penyakit.delete()
        messages.success(request, "Penyakit berhasil dihapus.")
        return redirect('penyakit_list')
    context = {'object': penyakit}
    return render(request, 'penyakit/confirm_delete.html', context)

# ------------------ GEJALA ------------------
def gejala_list(request):
    gejala_list = Gejala.objects.all()
    context = {
        'gejala_list': gejala_list,
        'gejala_count': gejala_list.count(),
    }
    return render(request, 'gejala/list.html', context)

def gejala_create(request):
    if request.method == 'POST':
        form = GejalaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Gejala berhasil ditambahkan.")
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
            form.save()
            messages.success(request, "Gejala berhasil diupdate.")
            return redirect('gejala_list')
    else:
        form = GejalaForm(instance=gejala)
    context = {
        'form': form,
        'form_name': 'Gejala',
        'form_fungsi': 'Edit'
    }
    return render(request, 'form/form.html', context)

def gejala_delete(request, pk):
    gejala = get_object_or_404(Gejala, pk=pk)
    gejala.delete()
    messages.success(request, "Gejala berhasil dihapus.")
    return redirect('gejala_list')

# ------------------ ATURAN (Basis Pengetahuan) ------------------
def aturan_list(request):
    context = {
        'aturan_list': BasisPengetahuan.objects.all()
    }
    return render(request, 'aturan/list.html', context)

def aturan_create(request):
    if request.method == 'POST':
        form = BasisPengetahuanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Aturan berhasil ditambahkan.")
            return redirect('aturan_list')
    else:
        form = BasisPengetahuanForm()
    context = {'form': form}
    return render(request, 'aturan/form.html', context)

def aturan_update(request, pk):
    aturan = get_object_or_404(BasisPengetahuan, pk=pk)
    if request.method == 'POST':
        form = BasisPengetahuanForm(request.POST, instance=aturan)
        if form.is_valid():
            form.save()
            messages.success(request, "Aturan berhasil diupdate.")
            return redirect('aturan_list')
    else:
        form = BasisPengetahuanForm(instance=aturan)
    context = {'form': form}
    return render(request, 'aturan/form.html', context)

def aturan_delete(request, pk):
    aturan = get_object_or_404(BasisPengetahuan, pk=pk)
    if request.method == 'POST':
        aturan.delete()
        messages.success(request, "Aturan berhasil dihapus.")
        return redirect('aturan_list')
    context = {'object': aturan}
    return render(request, 'aturan/confirm_delete.html', context)

# ------------------ DIAGNOSA ------------------
def diagnosa_list(request):
    context = {
        'diagnosa_list': Diagnosa.objects.all()
    }
    return render(request, 'diagnosa/list.html', context)

def diagnosa_create(request):
    if request.method == 'POST':
        form = DiagnosaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Diagnosa berhasil ditambahkan.")
            return redirect('diagnosa_list')
    else:
        form = DiagnosaForm()
    context = {'form': form}
    return render(request, 'diagnosa/form.html', context)

def diagnosa_update(request, pk):
    diagnosa = get_object_or_404(Diagnosa, pk=pk)
    if request.method == 'POST':
        form = DiagnosaForm(request.POST, instance=diagnosa)
        if form.is_valid():
            form.save()
            messages.success(request, "Diagnosa berhasil diupdate.")
            return redirect('diagnosa_list')
    else:
        form = DiagnosaForm(instance=diagnosa)
    context = {'form': form}
    return render(request, 'diagnosa/form.html', context)

def diagnosa_delete(request, pk):
    diagnosa = get_object_or_404(Diagnosa, pk=pk)
    if request.method == 'POST':
        diagnosa.delete()
        messages.success(request, "Diagnosa berhasil dihapus.")
        return redirect('diagnosa_list')
    context = {'object': diagnosa}
    return render(request, 'diagnosa/confirm_delete.html', context)

# ------------------ GEJALA DIAGNOSA ------------------
def gejala_diagnosa_list(request):
    context = {
        'gejala_diagnosa_list': GejalaDiagnosa.objects.all()
    }
    return render(request, 'gejala_diagnosa/list.html', context)

def gejala_diagnosa_create(request):
    if request.method == 'POST':
        form = GejalaDiagnosaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Gejala Diagnosa berhasil ditambahkan.")
            return redirect('gejala_diagnosa_list')
    else:
        form = GejalaDiagnosaForm()
    context = {'form': form}
    return render(request, 'gejala_diagnosa/form.html', context)

def gejala_diagnosa_update(request, pk):
    gejala_diagnosa = get_object_or_404(GejalaDiagnosa, pk=pk)
    if request.method == 'POST':
        form = GejalaDiagnosaForm(request.POST, instance=gejala_diagnosa)
        if form.is_valid():
            form.save()
            messages.success(request, "Gejala Diagnosa berhasil diupdate.")
            return redirect('gejala_diagnosa_list')
    else:
        form = GejalaDiagnosaForm(instance=gejala_diagnosa)
    context = {'form': form}
    return render(request, 'gejala_diagnosa/form.html', context)

def gejala_diagnosa_delete(request, pk):
    gejala_diagnosa = get_object_or_404(GejalaDiagnosa, pk=pk)
    if request.method == 'POST':
        gejala_diagnosa.delete()
        messages.success(request, "Gejala Diagnosa berhasil dihapus.")
        return redirect('gejala_diagnosa_list')
    context = {'object': gejala_diagnosa}
    return render(request, 'gejala_diagnosa/confirm_delete.html', context)

# ------------------ HASIL DS ------------------
def hasil_list(request):
    context = {
        'hasil_list': HasilDS.objects.all()
    }
    return render(request, 'hasil/list.html', context)

def hasil_create(request):
    if request.method == 'POST':
        form = HasilDSForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Hasil DS berhasil ditambahkan.")
            return redirect('hasil_list')
    else:
        form = HasilDSForm()
    context = {'form': form}
    return render(request, 'hasil/form.html', context)

def hasil_update(request, pk):
    hasil = get_object_or_404(HasilDS, pk=pk)
    if request.method == 'POST':
        form = HasilDSForm(request.POST, instance=hasil)
        if form.is_valid():
            form.save()
            messages.success(request, "Hasil DS berhasil diupdate.")
            return redirect('hasil_list')
    else:
        form = HasilDSForm(instance=hasil)
    context = {'form': form}
    return render(request, 'hasil/form.html', context)

def hasil_delete(request, pk):
    hasil = get_object_or_404(HasilDS, pk=pk)
    if request.method == 'POST':
        hasil.delete()
        messages.success(request, "Hasil DS berhasil dihapus.")
        return redirect('hasil_list')
    context = {'object': hasil}
    return render(request, 'hasil/confirm_delete.html', context)
