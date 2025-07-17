from django.db import models

# Model Pasien
class Pasien(models.Model):
    nama = models.CharField(max_length=100)
    jenis_kelamin = models.CharField(max_length=10, choices=[('L', 'Laki-laki'), ('P', 'Perempuan')])
    tanggal_lahir = models.DateField(null=True, blank=True)
    alamat = models.TextField(blank=True)
    no_hp = models.CharField(max_length=20, blank=True)
    dibuat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama

# 1. Penyakit (Jenis Kanker)
class Penyakit(models.Model):
    kode = models.CharField(max_length=5, unique=True)
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama

# 2. Gejala
class Gejala(models.Model):
    kode = models.CharField(max_length=5, unique=True)
    nama = models.CharField(max_length=150)

    def __str__(self):
        return self.nama

# 3. Basis Pengetahuan / Relasi Gejala-Penyakit dengan Bobot (Mass Function)
class BasisPengetahuan(models.Model):
    gejala = models.ForeignKey(Gejala, on_delete=models.CASCADE)
    penyakit = models.ForeignKey(Penyakit, on_delete=models.CASCADE)
    bobot_kepercayaan = models.FloatField(help_text="Contoh: 0.6 untuk kepercayaan 60%")

    class Meta:
        unique_together = ('gejala', 'penyakit')

    def __str__(self):
        return f"{self.gejala} - {self.penyakit} ({self.bobot_kepercayaan})"

# 4. Diagnosa oleh user (misal user memilih gejala-gejala tertentu)
class Diagnosa(models.Model):
    pasien = models.ForeignKey(Pasien, on_delete=models.SET_NULL, null=True, blank=True, related_name='diagnosa')
    nama_user = models.CharField(max_length=100)
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.pasien:
            return f"Diagnosa {self.pasien.nama} pada {self.tanggal.strftime('%d-%m-%Y')}"
        return f"Diagnosa {self.nama_user} pada {self.tanggal.strftime('%d-%m-%Y')}"

# 5. Detail Diagnosa (Gejala-gejala yang dipilih)
class GejalaDiagnosa(models.Model):
    diagnosa = models.ForeignKey(Diagnosa, on_delete=models.CASCADE, related_name='gejala_terpilih')
    gejala = models.ForeignKey(Gejala, on_delete=models.CASCADE)

    def __str__(self):
        if self.diagnosa.pasien:
            return f"{self.diagnosa.pasien.nama} - {self.gejala.nama}"
        return f"{self.diagnosa.nama_user} - {self.gejala.nama}"

# 6. Hasil Diagnosa berdasarkan Dempster-Shafer
class HasilDS(models.Model):
    diagnosa = models.ForeignKey(Diagnosa, on_delete=models.CASCADE, related_name='hasil_ds')
    penyakit = models.ForeignKey(Penyakit, on_delete=models.CASCADE)
    nilai_kepercayaan = models.FloatField(help_text="Nilai akhir kepercayaan setelah perhitungan DS")

    def __str__(self):
        return f"{self.penyakit.nama} ({self.nilai_kepercayaan:.2f})"
