from django.db import models
from django.contrib.auth.models import User


class Division(models.Model):
    kode = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_division'
        verbose_name = 'Division'
        verbose_name_plural = 'Divisions'

    def __str__(self):
        return self.nama

class Dept(models.Model):
    kode = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=100)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True)  # parent_group → division
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_dept'
        verbose_name = 'Department'
        verbose_name_plural = 'Department'

    def __str__(self):
        return self.nama

class Section(models.Model):
    kode = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=100)
    dept = models.ForeignKey(Dept, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Departemen')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_section'
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

    def __str__(self):
        return f"{self.kode} - {self.nama}"

class Jabatan(models.Model):
    kode = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=100)
    tugas_utama = models.TextField(blank=True, null=True, verbose_name='Tugas Utama')
    level = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_jabatan'
        verbose_name = 'Jabatan'
        verbose_name_plural = 'Jabatan'

    def __str__(self):
        return self.nama

class Agama(models.Model):
    kode = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_agama'
        verbose_name = 'Agama'
        verbose_name_plural = 'Agama'
    
    def __str__(self):
        return f"{self.kode} - {self.nama}"


class Pendidikan(models.Model):
    kode = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=50, unique=True)
    urutan = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_pendidikan'
        verbose_name = 'Pendidikan'
        verbose_name_plural = 'Pendidikan'
    
    def __str__(self):
        return f"{self.kode} - {self.nama}"


class StatusKaryawan(models.Model):
    kode = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_status_karyawan'
        verbose_name = 'Status'
        verbose_name_plural = 'Status'
    
    def __str__(self):
        return f"{self.kode} - {self.nama}"


class PosisiKaryawan(models.Model):
    kode = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_posisi_karyawan'
        verbose_name = 'Posisi'
        verbose_name_plural = 'Posisi'
    
    def __str__(self):
        return f"{self.kode} - {self.nama}"

class Employee(models.Model):
    # Gender Choices
    GENDER_CHOICES = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ]

    # Marital Status Choices
    MARITAL_CHOICES = [
        ('BELUM KAWIN', 'Belum Kawin'),
        ('KAWIN', 'Kawin'),
        ('CERAI HIDUP', 'Cerai Hidup'),
        ('CERAI MATI', 'Cerai Mati'),
    ]

    # Religion Choices
    RELIGION_CHOICES = [
        ('ISLAM', 'Islam'),
        ('KRISTEN', 'Kristen'),
        ('KATOLIK', 'Katolik'),
        ('HINDU', 'Hindu'),
        ('BUDDHA', 'Buddha'),
        ('KONGHUCU', 'Konghucu'),
    ]

    # Blood Type Choices
    BLOOD_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ]

    # Education Choices
    EDUCATION_CHOICES = [
        ('SD', 'SD'),
        ('SMP', 'SMP'),
        ('SMA', 'SMA'),
        ('D1', 'D1'),
        ('D2', 'D2'),
        ('D3', 'D3'),
        ('S1', 'S1'),
        ('S2', 'S2'),
        ('S3', 'S3'),
    ]

    # Employee Status Choices
    EMPLOYEE_STATUS_CHOICES = [
        ('KONTRAK', 'Kontrak'),
        ('TETAP', 'Tetap'),
        ('OUTSOURCHING', 'Outsouching'),
        ('PROBATION', 'Probation'),
        ('HARIAN LEPAS', 'Harian Lepas'),
    ]

    # Working Status Choices
    WORKING_STATUS_CHOICES = [
        ('AKTIF', 'Aktif'),
        ('NONAKTIF', 'Nonaktif'),
        ('RESIGN', 'Resign'),
    ]

    # PTKP Choices
    PTKP_CHOICES = [
        ('TK/0', 'TK/0'),
        ('TK/1', 'TK/1'),
        ('TK/2', 'TK/2'),
        ('TK/3', 'TK/3'),
        ('K/0', 'K/0'),
        ('K/1', 'K/1'),
        ('K/2', 'K/2'),
        ('K/3', 'K/3'),
    ]

    # Tax Status Choices
    TAX_STATUS_CHOICES = [
        ('TUNGGAL', 'Tunggal'),
        ('KAWIN', 'Kawin'),
    ]

    # ========== Identity & Personal (REQUIRED) ==========
    nik = models.CharField(max_length=50, unique=True, verbose_name='NIK Karyawan')
    nama = models.CharField(max_length=200, verbose_name='Nama Lengkap')

    # ========== Identity & Personal (OPTIONAL) ==========
    sex = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True, verbose_name='Jenis Kelamin')
    tgl_lahir = models.DateField(blank=True, null=True, verbose_name='Tanggal Lahir')
    tempat_lahir = models.CharField(max_length=100, blank=True, null=True, verbose_name='Tempat Lahir')
    no_ktp = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name='No KTP')
    no_kk = models.CharField(max_length=20, blank=True, null=True, verbose_name='No KK')
    no_hp = models.CharField(max_length=15, blank=True, null=True, verbose_name='No HP')

    # ========== Address ==========
    alamat = models.TextField(blank=True, null=True, verbose_name='Alamat')
    kelurahan = models.CharField(max_length=100, blank=True, null=True, verbose_name='Kelurahan')
    kecamatan = models.CharField(max_length=100, blank=True, null=True, verbose_name='Kecamatan')
    kabupaten_kota = models.CharField(max_length=100, blank=True, null=True, verbose_name='Kabupaten/Kota')
    kode_pos = models.CharField(max_length=10, blank=True, null=True, verbose_name='Kode Pos')
    provinsi = models.CharField(max_length=100, blank=True, null=True, verbose_name='Provinsi')

    # ========== Family & Personal ==========
    status_kawin = models.CharField(max_length=20, choices=MARITAL_CHOICES, blank=True, null=True, verbose_name='Status Kawin')
    tanggungan = models.IntegerField(default=0, blank=True, null=True, verbose_name='Jumlah Tanggungan')
    agama = models.ForeignKey(Agama, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Agama')
    tinggi_badan = models.IntegerField(blank=True, null=True, verbose_name='Tinggi Badan (cm)')
    berat_badan = models.IntegerField(blank=True, null=True, verbose_name='Berat Badan (kg)')
    gol_darah = models.CharField(max_length=2, choices=BLOOD_CHOICES, blank=True, null=True, verbose_name='Gol Darah')
    pendidikan = models.ForeignKey(Pendidikan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Pendidikan')

    # ========== Employment ==========
    tgl_rekrut = models.DateField(blank=True, null=True, verbose_name='Tanggal Rekrut')
    status_karyawan = models.ForeignKey(StatusKaryawan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Status Karyawan')
    tgl_kartetap = models.DateField(blank=True, null=True, verbose_name='Tanggal Karyawan Tetap')
    posisi_karyawan = models.ForeignKey(PosisiKaryawan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Posisi Karyawan')
    no_kartu_kpk = models.CharField(max_length=50, blank=True, null=True, verbose_name='No Kartu KPK')

    # ========== Organization (Relasi) ==========
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Divisi')
    dept = models.ForeignKey(Dept, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Departemen')
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Section')
    jabatan = models.ForeignKey(Jabatan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Jabatan')

    # ========== Contract & Salary ==========
    kontrak_ke = models.IntegerField(default=1, blank=True, null=True, verbose_name='Kontrak Ke-')
    kontrak_berakhir = models.DateField(blank=True, null=True, verbose_name='Kontrak Berakhir')
    kode_gaji = models.CharField(max_length=50, blank=True, null=True, verbose_name='Kode Gaji')
    no_rek_bank = models.CharField(max_length=30, blank=True, null=True, verbose_name='No Rekening Bank')
    kode_bank = models.CharField(max_length=10, blank=True, null=True, verbose_name='Kode Bank')
    nama_bank = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nama Bank')

    # ========== Tax & BPJS ==========
    status_ptkp = models.CharField(max_length=10, choices=PTKP_CHOICES, blank=True, null=True, verbose_name='Status PTKP')
    no_npwp = models.CharField(max_length=20, blank=True, null=True, verbose_name='No NPWP')
    status_pajak = models.CharField(max_length=20, choices=TAX_STATUS_CHOICES, blank=True, null=True, verbose_name='Status Pajak')

    bpjs_tk = models.BooleanField(default=True, blank=True, null=True, verbose_name='BPJS TK Aktif')
    bpjs_tk_ditanggung = models.BooleanField(default=False, blank=True, null=True, verbose_name='BPJS TK Ditanggung Perusahaan')
    bpjs_tk_no = models.CharField(max_length=20, blank=True, null=True, verbose_name='No BPJS TK')

    bpjs_kes = models.BooleanField(default=True, blank=True, null=True, verbose_name='BPJS Kesehatan Aktif')
    bpjs_kes_ditanggung = models.BooleanField(default=False, blank=True, null=True, verbose_name='BPJS Kesehatan Ditanggung Perusahaan')
    bpjs_kes_no = models.CharField(max_length=20, blank=True, null=True, verbose_name='No BPJS Kesehatan')

    # ========== Others ==========
    faskes = models.CharField(max_length=100, blank=True, null=True, verbose_name='Faskes')
    placement = models.CharField(max_length=100, blank=True, null=True, verbose_name='Penempatan')
    tgl_out = models.DateField(blank=True, null=True, verbose_name='Tanggal Keluar')
    status_kerja = models.CharField(max_length=20, default='AKTIF', choices=WORKING_STATUS_CHOICES, blank=True, null=True, verbose_name='Status Kerja')
    foto = models.ImageField(upload_to='employee_photos/', blank=True, null=True, verbose_name='Foto')

    # ========== Audit Fields ==========
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