from django.db import models

class Dept(models.Model):
    kode = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=100)
    parent = models.ForeignKey('GroupDept', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_dept'
    
    def __str__(self):
        return self.nama

class GroupDept(models.Model):
    kode = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=100)    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_group_dept'
    
    def __str__(self):
        return self.nama

class Jabatan(models.Model):
    kode = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_jabatan'
    
    def __str__(self):
        return self.nama

class Employee(models.Model):
    nik = models.CharField(max_length=50, unique=True)
    nama = models.CharField(max_length=200)
    dept = models.ForeignKey(Dept, on_delete=models.SET_NULL, null=True, blank=True)
    group_dept = models.ForeignKey(GroupDept, on_delete=models.SET_NULL, null=True, blank=True)
    jabatan = models.ForeignKey(Jabatan, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = 'hr_employee'
    
    def __str__(self):
        return f"{self.nik} - {self.nama}"
