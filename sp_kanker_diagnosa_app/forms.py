from django import forms
from .models import Penyakit, Gejala, BasisPengetahuan, Diagnosa, HasilDS, GejalaDiagnosa, Pasien

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
        fields = ['nama', 'jenis_kelamin', 'tanggal_lahir', 'alamat', 'no_hp']

        widgets = {
            'tanggal_lahir': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-control'}),
            'alamat': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'no_hp': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PenyakitForm(BootstrapModelForm):
    class Meta:
        model = Penyakit
        fields = ['kode', 'nama']

class GejalaForm(BootstrapModelForm):
    class Meta:
        model = Gejala
        fields = ['kode', 'nama']

class BasisPengetahuanForm(BootstrapModelForm):
    class Meta:
        model = BasisPengetahuan
        fields = ['gejala', 'penyakit', 'bobot_kepercayaan']

class DiagnosaForm(BootstrapModelForm):
    class Meta:
        model = Diagnosa
        fields = ['nama_user']

class GejalaDiagnosaForm(BootstrapModelForm):
    class Meta:
        model = GejalaDiagnosa
        fields = ['diagnosa', 'gejala']

class HasilDSForm(BootstrapModelForm):
    class Meta:
        model = HasilDS
        fields = ['diagnosa', 'penyakit', 'nilai_kepercayaan']
