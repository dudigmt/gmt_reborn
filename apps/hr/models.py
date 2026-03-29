from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    # Personal Data
    nik = models.CharField(max_length=50, unique=True, verbose_name='NIK Karyawan')
    nama = models.CharField(max_length=200, verbose_name='Nama Lengkap')
    sex = models.CharField(max_length=10, choices=[('L', 'Laki-laki'), ('P', 'Perempuan')], verbose_name='Jenis Kelamin')
    tgl_lahir = models.DateField(verbose_name='Tanggal Lahir')
    tempat_lahir = models.CharField(max_length=100, verbose_name='Tempat Lahir')
    
    # Identity Documents
    no_ktp = models.CharField(max_length=20, unique=True, verbose_name='No KTP')
    no_kk = models.CharField(max_length=20, blank=True, null=True, verbose_name='No KK')
    no_hp = models.CharField(max_length=15, verbose_name='No HP')
    
    # Address
    alamat = models.TextField(verbose_name='Alamat')
    kelurahan = models.CharField(max_length=100, verbose_name='Kelurahan')
    kecamatan = models.CharField(max_length=100, verbose_name='Kecamatan')
    kabupaten_kota = models.CharField(max_length=100, verbose_name='Kabupaten/Kota')
    kode_pos = models.CharField(max_length=10, verbose_name='Kode Pos')
    provinsi = models.CharField(max_length=100, verbose_name='Provinsi')
    
    # Family & Personal
    status_kawin = models.CharField(max_length=20, choices=[
        ('BELUM KAWIN', 'Belum Kawin'),
        ('KAWIN', 'Kawin'),
        ('CERAI HIDUP', 'Cerai Hidup'),
        ('CERAI MATI', 'Cerai Mati')
    ], verbose_name='Status Kawin')
    tanggungan = models.IntegerField(default=0, verbose_name='Jumlah Tanggungan')
    agama = models.CharField(max_length=20, choices=[
        ('ISLAM', 'Islam'),
        ('KRISTEN', 'Kristen'),
        ('KATOLIK', 'Katolik'),
        ('HINDU', 'Hindu'),
        ('BUDDHA', 'Buddha'),
        ('KONGHUCU', 'Konghucu')
    ], verbose_name='Agama')
    tinggi_badan = models.IntegerField(blank=True, null=True, verbose_name='Tinggi Badan (cm)')
    berat_badan = models.IntegerField(blank=True, null=True, verbose_name='Berat Badan (kg)')
    gol_darah = models.CharField(max_length=2, blank=True, null=True, choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], verbose_name='Gol Darah')
    pendidikan = models.CharField(max_length=50, choices=[
        ('SD', 'SD'), ('SMP', 'SMP'), ('SMA', 'SMA'), ('D1', 'D1'), 
        ('D2', 'D2'), ('D3', 'D3'), ('S1', 'S1'), ('S2', 'S2'), ('S3', 'S3')
    ], verbose_name='Pendidikan')
    
    # Employment Data
    tgl_rekrut = models.DateField(verbose_name='Tanggal Rekrut')
    status_karyawan = models.CharField(max_length=20, choices=[
        ('KONTRAK', 'Kontrak'),
        ('TETAP', 'Tetap'),
        ('PROBATION', 'Probation'),
        ('HARIAN LEPAS', 'Harian Lepas')
    ], verbose_name='Status Karyawan')
    tgl_kartetap = models.DateField(blank=True, null=True, verbose_name='Tanggal Karyawan Tetap')
    
    # Position & Organization
    posisi_karyawan = models.CharField(max_length=100, verbose_name='Posisi Karyawan')
    no_kartu_kpk = models.CharField(max_length=50, blank=True, null=True, verbose_name='No Kartu KPK')
    group = models.CharField(max_length=50, verbose_name='Group')
    dept = models.CharField(max_length=50, verbose_name='Departemen')
    jabatan = models.CharField(max_length=100, verbose_name='Jabatan')
    
    # Contract
    kontrak_ke = models.IntegerField(default=1, verbose_name='Kontrak Ke-')
    kontrak_berakhir = models.DateField(blank=True, null=True, verbose_name='Kontrak Berakhir')
    
    # Salary & Bank
    kode_gaji = models.CharField(max_length=50, verbose_name='Kode Gaji')
    no_rek_bank = models.CharField(max_length=30, verbose_name='No Rekening Bank')
    kode_bank = models.CharField(max_length=10, verbose_name='Kode Bank')
    nama_bank = models.CharField(max_length=100, verbose_name='Nama Bank')
    
    # Tax (Pajak)
    status_ptkp = models.CharField(max_length=10, choices=[
        ('TK/0', 'TK/0'), ('TK/1', 'TK/1'), ('TK/2', 'TK/2'), ('TK/3', 'TK/3'),
        ('K/0', 'K/0'), ('K/1', 'K/1'), ('K/2', 'K/2'), ('K/3', 'K/3')
    ], verbose_name='Status PTKP')
    no_npwp = models.CharField(max_length=20, blank=True, null=True, verbose_name='No NPWP')
    status_pajak = models.CharField(max_length=20, choices=[('TUNGGAL', 'Tunggal'), ('KAWIN', 'Kawin')], verbose_name='Status Pajak')
    
    # BPJS
    bpjs_tk = models.BooleanField(default=True, verbose_name='BPJS TK Aktif')
    bpjs_tk_ditanggung = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='BPJS TK Ditanggung Perusahaan')
    bpjs_tk_no = models.CharField(max_length=20, blank=True, null=True, verbose_name='No BPJS TK')
    bpjs_kes = models.BooleanField(default=True, verbose_name='BPJS Kesehatan Aktif')
    bpjs_kes_ditanggung = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='BPJS Kesehatan Ditanggung Perusahaan')
    bpjs_kes_no = models.CharField(max_length=20, blank=True, null=True, verbose_name='No BPJS Kesehatan')
    
    # Other
    faskes = models.CharField(max_length=100, blank=True, null=True, verbose_name='Faskes')
    placement = models.CharField(max_length=100, verbose_name='Placement')
    tgl_out = models.DateField(blank=True, null=True, verbose_name='Tanggal Keluar')
    status_kerja = models.CharField(max_length=20, default='AKTIF', choices=[('AKTIF', 'Aktif'), ('NONAKTIF', 'Nonaktif'), ('RESIGN', 'Resign')], verbose_name='Status Kerja')
    foto = models.ImageField(upload_to='employee_photos/', blank=True, null=True, verbose_name='Foto')
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees_created')
    
    class Meta:
        db_table = 'hr_employee'
        verbose_name = 'Karyawan'
        verbose_name_plural = 'Data Karyawan'
        ordering = ['nik']
    
    def __str__(self):
        return f"{self.nik} - {self.nama}"