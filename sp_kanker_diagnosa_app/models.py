from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

# Model Pasien
class Pasien(models.Model):
    JENIS_KELAMIN_CHOICES = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ]
    
    nama = models.CharField(max_length=100)
    jenis_kelamin = models.CharField(max_length=10, choices=JENIS_KELAMIN_CHOICES)
    tanggal_lahir = models.DateField(null=True, blank=True)
    alamat = models.TextField(blank=True)
    no_hp = models.CharField(max_length=20, blank=True)
    umur = models.PositiveIntegerField(null=True, blank=True, help_text="Umur dalam tahun")
    riwayat_keluarga = models.TextField(blank=True, help_text="Riwayat kanker dalam keluarga")
    dibuat = models.DateTimeField(auto_now_add=True)
    diperbarui = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pasien"
        verbose_name_plural = "Pasien"
        ordering = ['-dibuat']

    def __str__(self):
        return self.nama

# 1. Penyakit (Jenis Kanker)
class Penyakit(models.Model):
    kode = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True)
    tingkat_keganasan = models.CharField(max_length=20, choices=[
        ('RENDAH', 'Rendah'),
        ('SEDANG', 'Sedang'),
        ('TINGGI', 'Tinggi'),
    ], default='SEDANG')
    pengobatan = models.TextField(blank=True)
    pencegahan = models.TextField(blank=True)
    dibuat = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Penyakit"
        verbose_name_plural = "Penyakit"
        ordering = ['nama']

    def __str__(self):
        return f"{self.kode} - {self.nama}"

# 2. Gejala
class Gejala(models.Model):
    KATEGORI_CHOICES = [
        ('UMUM', 'Gejala Umum'),
        ('KHUSUS', 'Gejala Khusus'),
        ('LANJUTAN', 'Gejala Lanjutan'),
    ]
    
    kode = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=150)
    deskripsi = models.TextField(blank=True)
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES, default='UMUM')
    pertanyaan = models.TextField(help_text="Pertanyaan untuk mengidentifikasi gejala")
    dibuat = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Gejala"
        verbose_name_plural = "Gejala"
        ordering = ['kategori', 'nama']

    def __str__(self):
        return f"{self.kode} - {self.nama}"

# 3. Basis Pengetahuan / Relasi Gejala-Penyakit dengan Bobot (Mass Function)
class BasisPengetahuan(models.Model):
    gejala = models.ForeignKey(Gejala, on_delete=models.CASCADE, related_name='basis_pengetahuan')
    penyakit = models.ForeignKey(Penyakit, on_delete=models.CASCADE, related_name='basis_pengetahuan')
    bobot_kepercayaan = models.DecimalField(
        max_digits=5, 
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0000')), MaxValueValidator(Decimal('1.0000'))],
        help_text="Nilai antara 0.0000 - 1.0000 (Contoh: 0.6000 untuk kepercayaan 60%)"
    )
    bobot_ketidakpercayaan = models.DecimalField(
        max_digits=5, 
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0000')), MaxValueValidator(Decimal('1.0000'))],
        default=Decimal('0.0000'),
        help_text="Nilai ketidakpercayaan (1 - bobot_kepercayaan)"
    )
    sumber_referensi = models.CharField(max_length=200, blank=True, help_text="Sumber referensi untuk bobot ini")
    dibuat = models.DateTimeField(auto_now_add=True)
    diperbarui = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('gejala', 'penyakit')
        verbose_name = "Basis Pengetahuan"
        verbose_name_plural = "Basis Pengetahuan"
        ordering = ['penyakit', 'gejala']

    def save(self, *args, **kwargs):
        # Otomatis menghitung bobot ketidakpercayaan
        if self.bobot_kepercayaan:
            self.bobot_ketidakpercayaan = Decimal('1.0000') - self.bobot_kepercayaan
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.gejala.nama} → {self.penyakit.nama} ({self.bobot_kepercayaan})"

# 4. Diagnosa oleh user
class Diagnosa(models.Model):
    STATUS_CHOICES = [
        ('PROSES', 'Dalam Proses'),
        ('SELESAI', 'Selesai'),
        ('BATAL', 'Dibatalkan'),
    ]
    
    pasien = models.ForeignKey(Pasien, on_delete=models.SET_NULL, null=True, blank=True, related_name='diagnosa')
    tanggal = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PROSES')
    catatan = models.TextField(blank=True, help_text="Catatan tambahan dari diagnosa")
    total_gejala = models.PositiveIntegerField(default=0, help_text="Jumlah gejala yang dipilih")
    
    class Meta:
        verbose_name = "Diagnosa"
        verbose_name_plural = "Diagnosa"
        ordering = ['-tanggal']

    def __str__(self):
        if self.pasien:
            return f"Diagnosa {self.pasien.nama} pada {self.tanggal.strftime('%d-%m-%Y %H:%M')}"
        return f"Diagnosa pada {self.tanggal.strftime('%d-%m-%Y %H:%M')}"

# 5. Detail Diagnosa (Gejala-gejala yang dipilih)
class GejalaDiagnosa(models.Model):
    diagnosa = models.ForeignKey(Diagnosa, on_delete=models.CASCADE, related_name='gejala_terpilih')
    gejala = models.ForeignKey(Gejala, on_delete=models.CASCADE)
    tingkat_keparahan = models.CharField(max_length=20, choices=[
        ('RINGAN', 'Ringan'),
        ('SEDANG', 'Sedang'),
        ('BERAT', 'Berat'),
    ], default='SEDANG')
    durasi = models.CharField(max_length=50, blank=True, help_text="Berapa lama gejala muncul")
    bobot_pengguna = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0000')), MaxValueValidator(Decimal('1.0000'))],
        default=Decimal('1.0000'),
        help_text="Bobot kepercayaan pengguna terhadap gejala (0.0000 - 1.0000)"
    )
    catatan = models.TextField(blank=True, help_text="Catatan tambahan untuk gejala ini")
    dipilih_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('diagnosa', 'gejala')
        verbose_name = "Gejala Diagnosa"
        verbose_name_plural = "Gejala Diagnosa"

    def __str__(self):
        if self.diagnosa.pasien:
            return f"{self.diagnosa.pasien.nama} - {self.gejala.nama} ({self.tingkat_keparahan})"
        return f"{self.diagnosa.nama_user} - {self.gejala.nama} ({self.tingkat_keparahan})"

# 6. Hasil Diagnosa berdasarkan Dempster-Shafer
class HasilDS(models.Model):
    diagnosa = models.ForeignKey(Diagnosa, on_delete=models.CASCADE, related_name='hasil_ds')
    penyakit = models.ForeignKey(Penyakit, on_delete=models.CASCADE)
    nilai_kepercayaan = models.DecimalField(
        max_digits=5, 
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0000')), MaxValueValidator(Decimal('1.0000'))],
        help_text="Nilai akhir kepercayaan setelah perhitungan DS"
    )
    nilai_ketidakpercayaan = models.DecimalField(
        max_digits=5, 
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0000')), MaxValueValidator(Decimal('1.0000'))],
        help_text="Nilai ketidakpercayaan"
    )
    nilai_uncertainty = models.DecimalField(
        max_digits=5, 
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0000')), MaxValueValidator(Decimal('1.0000'))],
        help_text="Nilai ketidakpastian (uncertainty)"
    )
    ranking = models.PositiveIntegerField(help_text="Peringkat hasil diagnosa")
    rekomendasi = models.TextField(blank=True, help_text="Rekomendasi berdasarkan hasil diagnosa")
    dibuat = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('diagnosa', 'penyakit')
        verbose_name = "Hasil Dempster-Shafer"
        verbose_name_plural = "Hasil Dempster-Shafer"
        ordering = ['diagnosa', 'ranking']

    def save(self, *args, **kwargs):
        # Otomatis menghitung nilai uncertainty
        if self.nilai_kepercayaan and self.nilai_ketidakpercayaan:
            self.nilai_uncertainty = Decimal('1.0000') - self.nilai_kepercayaan - self.nilai_ketidakpercayaan
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.penyakit.nama} ({self.nilai_kepercayaan:.2%}) - Ranking: {self.ranking}"

# 7. Model untuk menyimpan perhitungan intermediate Dempster-Shafer
class PerhitunganDS(models.Model):
    diagnosa = models.ForeignKey(Diagnosa, on_delete=models.CASCADE, related_name='perhitungan_ds')
    gejala = models.ForeignKey(Gejala, on_delete=models.CASCADE)
    penyakit = models.ForeignKey(Penyakit, on_delete=models.CASCADE)
    mass_function = models.DecimalField(
        max_digits=5, 
        decimal_places=4,
        help_text="Mass function untuk gejala-penyakit ini"
    )
    belief_function = models.DecimalField(
        max_digits=5, 
        decimal_places=4,
        help_text="Belief function"
    )
    plausibility_function = models.DecimalField(
        max_digits=5, 
        decimal_places=4,
        help_text="Plausibility function"
    )
    langkah_perhitungan = models.TextField(help_text="Detail langkah perhitungan")
    dibuat = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Perhitungan DS"
        verbose_name_plural = "Perhitungan DS"
        ordering = ['diagnosa', 'gejala']

    def __str__(self):
        return f"DS: {self.gejala.nama} → {self.penyakit.nama} ({self.mass_function})"
