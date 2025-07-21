from django import forms
from .models import (
    Penyakit, Gejala, BasisPengetahuan, Diagnosa, 
    HasilDS, GejalaDiagnosa, Pasien, PerhitunganDS
)

class BootstrapModelForm(forms.ModelForm):
    """Base form to add Bootstrap classes to all fields."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect, forms.CheckboxSelectMultiple)):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

class PasienForm(BootstrapModelForm):
    class Meta:
        model = Pasien
        fields = [
            'nama', 'jenis_kelamin', 'tanggal_lahir', 'alamat', 
            'no_hp', 'umur', 'riwayat_keluarga'
        ]
        widgets = {
            'tanggal_lahir': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'placeholder': 'Pilih tanggal lahir'
            }),
            'nama': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan nama lengkap'
            }),
            'jenis_kelamin': forms.Select(attrs={
                'class': 'form-control'
            }),
            'alamat': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Masukkan alamat lengkap'
            }),
            'no_hp': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: 08123456789'
            }),
            'umur': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan umur dalam tahun',
                'min': '0',
                'max': '150'
            }),
            'riwayat_keluarga': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Riwayat kanker dalam keluarga (opsional)'
            }),
        }

    def clean_umur(self):
        umur = self.cleaned_data.get('umur')
        if umur is not None and (umur < 0 or umur > 150):
            raise forms.ValidationError("Umur harus antara 0-150 tahun")
        return umur

class PenyakitForm(BootstrapModelForm):
    class Meta:
        model = Penyakit
        fields = [
            'kode', 'nama', 'deskripsi', 'tingkat_keganasan', 
            'pengobatan', 'pencegahan'
        ]
        widgets = {
            'kode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: K001'
            }),
            'nama': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama jenis kanker'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Deskripsi penyakit'
            }),
            'tingkat_keganasan': forms.Select(attrs={
                'class': 'form-control'
            }),
            'pengobatan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Metode pengobatan yang tersedia'
            }),
            'pencegahan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Cara pencegahan'
            }),
        }

class GejalaForm(BootstrapModelForm):
    class Meta:
        model = Gejala
        fields = [
            'kode', 'nama', 'deskripsi', 'kategori', 'pertanyaan'
        ]
        widgets = {
            'kode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: G001'
            }),
            'nama': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama gejala'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Deskripsi gejala'
            }),
            'kategori': forms.Select(attrs={
                'class': 'form-control'
            }),
            'pertanyaan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Pertanyaan untuk mengidentifikasi gejala'
            }),
        }

class BasisPengetahuanForm(BootstrapModelForm):
    class Meta:
        model = BasisPengetahuan
        fields = [
            'gejala', 'penyakit', 'bobot_kepercayaan', 'sumber_referensi'
        ]
        widgets = {
            'gejala': forms.Select(attrs={
                'class': 'form-control'
            }),
            'penyakit': forms.Select(attrs={
                'class': 'form-control'
            }),
            'bobot_kepercayaan': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0001',
                'min': '0.0000',
                'max': '1.0000',
                'placeholder': 'Contoh: 0.6000 untuk 60%'
            }),
            'sumber_referensi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sumber referensi untuk bobot ini'
            }),
        }

    def clean_bobot_kepercayaan(self):
        bobot = self.cleaned_data.get('bobot_kepercayaan')
        if bobot is not None and (bobot < 0 or bobot > 1):
            raise forms.ValidationError("Bobot kepercayaan harus antara 0.0000 - 1.0000")
        return bobot

class DiagnosaForm(BootstrapModelForm):
    class Meta:
        model = Diagnosa
        fields = "__all__"
        widgets = {
            'pasien': forms.Select(attrs={
                'class': 'form-control'
            }),
            'nama_user': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama user yang melakukan diagnosa'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'catatan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Catatan tambahan dari diagnosa'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tambahkan opsi kosong untuk pasien
        self.fields['pasien'].empty_label = "Pilih pasien (opsional)"

class GejalaDiagnosaForm(BootstrapModelForm):
    class Meta:
        model = GejalaDiagnosa
        fields = "__all__"
        widgets = {
            'diagnosa': forms.Select(attrs={
                'class': 'form-control'
            }),
            'gejala': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tingkat_keparahan': forms.Select(attrs={
                'class': 'form-control'
            }),
            'durasi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: 2 minggu, 1 bulan'
            }),
            'catatan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Catatan tambahan untuk gejala ini'
            }),
        }

class HasilDSForm(BootstrapModelForm):
    class Meta:
        model = HasilDS
        fields = [
            'diagnosa', 'penyakit', 'nilai_kepercayaan', 
            'nilai_ketidakpercayaan', 'ranking', 'rekomendasi'
        ]
        widgets = {
            'diagnosa': forms.Select(attrs={
                'class': 'form-control'
            }),
            'penyakit': forms.Select(attrs={
                'class': 'form-control'
            }),
            'nilai_kepercayaan': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0001',
                'min': '0.0000',
                'max': '1.0000',
                'placeholder': 'Nilai kepercayaan (0.0000-1.0000)'
            }),
            'nilai_ketidakpercayaan': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0001',
                'min': '0.0000',
                'max': '1.0000',
                'placeholder': 'Nilai ketidakpercayaan (0.0000-1.0000)'
            }),
            'ranking': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Peringkat hasil diagnosa'
            }),
            'rekomendasi': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Rekomendasi berdasarkan hasil diagnosa'
            }),
        }

    def clean_nilai_kepercayaan(self):
        nilai = self.cleaned_data.get('nilai_kepercayaan')
        if nilai is not None and (nilai < 0 or nilai > 1):
            raise forms.ValidationError("Nilai kepercayaan harus antara 0.0000 - 1.0000")
        return nilai

    def clean_nilai_ketidakpercayaan(self):
        nilai = self.cleaned_data.get('nilai_ketidakpercayaan')
        if nilai is not None and (nilai < 0 or nilai > 1):
            raise forms.ValidationError("Nilai ketidakpercayaan harus antara 0.0000 - 1.0000")
        return nilai

class PerhitunganDSForm(BootstrapModelForm):
    class Meta:
        model = PerhitunganDS
        fields = [
            'diagnosa', 'gejala', 'penyakit', 'mass_function',
            'belief_function', 'plausibility_function', 'langkah_perhitungan'
        ]
        widgets = {
            'diagnosa': forms.Select(attrs={
                'class': 'form-control'
            }),
            'gejala': forms.Select(attrs={
                'class': 'form-control'
            }),
            'penyakit': forms.Select(attrs={
                'class': 'form-control'
            }),
            'mass_function': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0001',
                'min': '0.0000',
                'max': '1.0000',
                'placeholder': 'Mass function'
            }),
            'belief_function': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0001',
                'min': '0.0000',
                'max': '1.0000',
                'placeholder': 'Belief function'
            }),
            'plausibility_function': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0001',
                'min': '0.0000',
                'max': '1.0000',
                'placeholder': 'Plausibility function'
            }),
            'langkah_perhitungan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Detail langkah perhitungan Dempster-Shafer'
            }),
        }

# Form untuk pencarian dan filter
class PencarianPasienForm(forms.Form):
    nama = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cari berdasarkan nama...'
        })
    )
    jenis_kelamin = forms.ChoiceField(
        choices=[('', 'Semua')] + Pasien.JENIS_KELAMIN_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class PencarianGejalaForm(forms.Form):
    nama = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cari gejala...'
        })
    )
    kategori = forms.ChoiceField(
        choices=[('', 'Semua Kategori')] + Gejala.KATEGORI_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class PencarianPenyakitForm(forms.Form):
    nama = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cari penyakit...'
        })
    )
    tingkat_keganasan = forms.ChoiceField(
        choices=[('', 'Semua Tingkat')] + [
            ('RENDAH', 'Rendah'),
            ('SEDANG', 'Sedang'),
            ('TINGGI', 'Tinggi'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

# Form untuk diagnosa multi-step
class DiagnosaStep1Form(forms.Form):
    """Form untuk langkah 1: Input data pasien"""
    nama_user = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan nama Anda'
        })
    )
    pasien = forms.ModelChoiceField(
        queryset=Pasien.objects.all(),
        required=False,
        empty_label="Pilih pasien (opsional)",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class DiagnosaStep2Form(forms.Form):
    """Form untuk langkah 2: Pilih gejala"""
    gejala_list = forms.ModelMultipleChoiceField(
        queryset=Gejala.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Kelompokkan gejala berdasarkan kategori
        gejala_umum = Gejala.objects.filter(kategori='UMUM')
        gejala_khusus = Gejala.objects.filter(kategori='KHUSUS')
        gejala_lanjutan = Gejala.objects.filter(kategori='LANJUTAN')
        
        self.fields['gejala_umum'] = forms.ModelMultipleChoiceField(
            queryset=gejala_umum,
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            required=False,
            label="Gejala Umum"
        )
        self.fields['gejala_khusus'] = forms.ModelMultipleChoiceField(
            queryset=gejala_khusus,
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            required=False,
            label="Gejala Khusus"
        )
        self.fields['gejala_lanjutan'] = forms.ModelMultipleChoiceField(
            queryset=gejala_lanjutan,
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            required=False,
            label="Gejala Lanjutan"
        )

class DiagnosaStep3Form(forms.Form):
    """Form untuk langkah 3: Detail gejala yang dipilih"""
    def __init__(self, gejala_terpilih, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for gejala in gejala_terpilih:
            field_name = f'gejala_{gejala.id}'
            self.fields[field_name] = forms.ChoiceField(
                choices=[
                    ('RINGAN', 'Ringan'),
                    ('SEDANG', 'Sedang'),
                    ('BERAT', 'Berat'),
                ],
                widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                label=f"Tingkat keparahan: {gejala.nama}",
                initial='SEDANG'
            )
            
            # Field untuk durasi
            durasi_field = f'durasi_{gejala.id}'
            self.fields[durasi_field] = forms.CharField(
                max_length=50,
                required=False,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Berapa lama gejala muncul?'
                }),
                label=f"Durasi: {gejala.nama}"
            )
