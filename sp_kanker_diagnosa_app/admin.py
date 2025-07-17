from django.contrib import admin
from .models import Pasien, Penyakit, Gejala, BasisPengetahuan, Diagnosa, GejalaDiagnosa, HasilDS
# Register your models here.
admin.site.register(Pasien)
admin.site.register(Penyakit)
admin.site.register(Gejala)
admin.site.register(BasisPengetahuan)
admin.site.register(Diagnosa)
admin.site.register(GejalaDiagnosa)
admin.site.register(HasilDS)
