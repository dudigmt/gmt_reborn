from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    """Auto-synced from database table: hr_employee"""
    nik = models.CharField(max_length=8)
    nama = models.CharField(max_length=200)
    sex = models.CharField(max_length=10)
    tgl_lahir = models.DateField()
    tempat_lahir = models.CharField(max_length=100)
    no_ktp = models.CharField(max_length=20)
    no_kk = models.CharField(max_length=20, blank=True, null=True)
    no_hp = models.CharField(max_length=15, blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    kelurahan = models.CharField(max_length=100, blank=True, null=True)
    kecamatan = models.CharField(max_length=100, blank=True, null=True)
    kabupaten_kota = models.CharField(max_length=100, blank=True, null=True)
    kode_pos = models.CharField(max_length=10, blank=True, null=True)
    provinsi = models.CharField(max_length=100, blank=True, null=True)
    status_kawin = models.CharField(max_length=20, blank=True, null=True)
    tanggungan = models.IntegerField()
    agama = models.CharField(max_length=20, blank=True, null=True)
    tinggi_badan = models.IntegerField(blank=True, null=True)
    berat_badan = models.IntegerField(blank=True, null=True)
    gol_darah = models.CharField(max_length=2, blank=True, null=True)
    pendidikan = models.CharField(max_length=50, blank=True, null=True)
    tgl_rekrut = models.DateField()
    status_karyawan = models.CharField(max_length=20)
    tgl_kartetap = models.DateField(blank=True, null=True)
    posisi_karyawan = models.CharField(max_length=100)
    no_kartu_kpk = models.CharField(max_length=50, blank=True, null=True)
    group = models.CharField(max_length=50)
    dept = models.CharField(max_length=50)
    jabatan = models.CharField(max_length=100)
    kontrak_ke = models.IntegerField()
    kontrak_berakhir = models.DateField(blank=True, null=True)
    kode_gaji = models.CharField(max_length=50, blank=True, null=True)
    no_rek_bank = models.CharField(max_length=30, blank=True, null=True)
    kode_bank = models.CharField(max_length=10, blank=True, null=True)
    nama_bank = models.CharField(max_length=100, blank=True, null=True)
    status_ptkp = models.CharField(max_length=10, blank=True, null=True)
    no_npwp = models.CharField(max_length=20, blank=True, null=True)
    status_pajak = models.CharField(max_length=20, blank=True, null=True)
    bpjs_tk = models.BooleanField(default=False)
    bpjs_tk_ditanggung = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    bpjs_tk_no = models.CharField(max_length=20, blank=True, null=True)
    bpjs_kes = models.BooleanField(default=False)
    bpjs_kes_ditanggung = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    bpjs_kes_no = models.CharField(max_length=20, blank=True, null=True)
    faskes = models.CharField(max_length=100, blank=True, null=True)
    placement = models.CharField(max_length=100, blank=True, null=True)
    tgl_out = models.DateField(blank=True, null=True)
    status_kerja = models.CharField(max_length=20, blank=True, null=True)
    foto = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.TextField()
    updated_at = models.TextField()
    created_by_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'hr_employee'
        verbose_name = 'hr_employee'
        verbose_name_plural = 'hr_employee'
    
    def __str__(self):
        return str(self.id)
