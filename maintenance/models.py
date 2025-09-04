from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta, date

class MachineCategory(models.Model):
    """
    ประเภทของเครื่องจักร เช่น เครื่องกลึง เครื่องมิลลิ่ง เครื่องฉีด ฯลฯ
    ใช้สำหรับจัดหมวดหมู่เครื่องจักรเพื่อการจัดการที่ง่ายขึ้น
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Machine categories'

    def __str__(self):
        return self.name


class Location(models.Model):
    """
    สถานที่ตั้งของเครื่องจักร เช่น โรงงาน A, โรงงาน B, แผนก Production ฯลฯ
    ช่วยในการติดตามและค้นหาเครื่องจักรตามสถานที่
    """
    name = models.CharField(max_length=100, unique=True)
    note = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Machine(models.Model):
    """
    ข้อมูลเครื่องจักร ประกอบด้วยรหัส ชื่อ ประเภท สถานที่ หมายเลขเครื่อง วันที่ซื้อ
    เป็นข้อมูลหลักที่ใช้ในการจัดการการบำรุงรักษา
    สามารถเก็บรูปภาพของเครื่องจักรได้ และมีสถานะการใช้งาน
    """
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(MachineCategory, on_delete=models.PROTECT, related_name='machines')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='machines')
    serial_no = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='machines/', null=True, blank=True)  # ต้องมี Pillow
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.code} - {self.name}'


class MaintenancePlan(models.Model):
    """
    แผนการบำรุงรักษาตามกำหนด (Preventive Maintenance Plan)
    กำหนดความถี่ของการบำรุงรักษา เช่น ทุก 30 วัน, ทุก 3 เดือน
    คำนวณวันครบกำหนดการบำรุงรักษาครั้งถัดไปอัตโนมัติ
    ใช้สำหรับสร้าง Work Order แบบ Preventive Maintenance
    """
    UNIT_DAYS = 'DAYS'
    UNIT_WEEKS = 'WEEKS'
    UNIT_MONTHS = 'MONTHS'
    UNIT_CHOICES = [
        (UNIT_DAYS, 'Days'),
        (UNIT_WEEKS, 'Weeks'),
        (UNIT_MONTHS, 'Months'),
    ]

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='plans')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    frequency_value = models.PositiveIntegerField(default=30)  # จำนวน
    frequency_unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default=UNIT_DAYS)
    last_done_date = models.DateField(null=True, blank=True)
    next_due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.machine.code} - {self.title}'

    def compute_next_due(self, from_date=None):
        base = from_date or self.last_done_date or date.today()
        if self.frequency_unit == self.UNIT_DAYS:
            return base + timedelta(days=self.frequency_value)
        if self.frequency_unit == self.UNIT_WEEKS:
            return base + timedelta(weeks=self.frequency_value)
        # MONTHS (แบบง่าย ๆ คิดเป็น 30 วันต่อเดือน)
        return base + timedelta(days=30 * self.frequency_value)

    def save(self, *args, **kwargs):
        if not self.next_due_date:
            self.next_due_date = self.compute_next_due()
        super().save(*args, **kwargs)

    @classmethod
    def due_within(cls, days=7):
        today = date.today()
        return cls.objects.filter(next_due_date__lte=today + timedelta(days=days)).order_by('next_due_date')


class WorkOrder(models.Model):
    """
    ใบสั่งงานบำรุงรักษา (Work Order) 
    ใช้สำหรับติดตามงานบำรุงรักษาทุกประเภท ได้แก่:
    - PM (Preventive): งานบำรุงรักษาตามแผน
    - CM (Corrective): งานแก้ไขเมื่อเครื่องเสีย  
    - INS (Inspection): งานตรวจสอบ
    
    มีระบบ Priority, Status, กำหนดผู้รับผิดชอบ และติดตามเวลาการทำงาน
    """
    TYPE_PM = 'PM'          # Preventive
    TYPE_CM = 'CM'          # Corrective (แจ้งเสีย)
    TYPE_INS = 'INS'        # Inspection
    TYPE_CHOICES = [
        (TYPE_PM, 'Preventive'),
        (TYPE_CM, 'Corrective'),
        (TYPE_INS, 'Inspection'),
    ]

    PRIORITY_LOW = 'LOW'
    PRIORITY_MED = 'MED'
    PRIORITY_HIGH = 'HIGH'
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MED, 'Medium'),
        (PRIORITY_HIGH, 'High'),
    ]

    STATUS_OPEN = 'OPEN'
    STATUS_INPROG = 'IN_PROGRESS'
    STATUS_DONE = 'DONE'
    STATUS_CANCEL = 'CANCELLED'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_INPROG, 'In progress'),
        (STATUS_DONE, 'Done'),
        (STATUS_CANCEL, 'Cancelled'),
    ]

    code = models.CharField(max_length=20, unique=True)
    wo_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_PM)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MED)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)

    machine = models.ForeignKey(Machine, on_delete=models.PROTECT, related_name='workorders')
    plan = models.ForeignKey(MaintenancePlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='workorders')

    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='reported_workorders')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_workorders')

    reported_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    summary = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'WO-{self.code} ({self.get_wo_type_display()})'


class WorkOrderTask(models.Model):
    """
    รายการงานย่อยในใบสั่งงาน (Work Order Tasks)
    แต่ละ Work Order สามารถมีหลายงานย่อย เช่น ตรวจเช็ค เปลี่ยนน้ำมัน ทำความสะอาด
    ช่วยให้การทำงานเป็นระบบและติดตามความคืบหน้าได้ชัดเจน
    """
    workorder = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Attachment(models.Model):
    """
    ไฟล์แนบรูปภาพ สำหรับเก็บหลักฐาน เช่น
    - รูปภาพเครื่องจักร (เชื่อมโยงกับ Machine)
    - รูปภาพผลงานที่ทำ หรือความเสียหาย (เชื่อมโยงกับ Work Order)
    
    ช่วยในการบันทึกหลักฐานและการตรวจสอบย้อนหลัง
    """
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, null=True, blank=True, related_name='attachments')
    workorder = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, null=True, blank=True, related_name='attachments')
    file = models.ImageField(upload_to='attachments/', null=True, blank=True)  # ใช้ ImageField เพื่อพรีวิวง่าย
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.machine or self.workorder
        return f'Attachment for {target}'
