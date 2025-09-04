from django import forms
from django.forms import inlineformset_factory
from .models import Machine, MaintenancePlan, WorkOrder, WorkOrderTask, Attachment
from django.contrib.auth.forms import AuthenticationForm

class BootstrapAuthenticationForm(AuthenticationForm):
    """
    ฟอร์มสำหรับเข้าสู่ระบบ
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ชื่อผู้ใช้'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'รหัสผ่าน'
        })
    )

class MachineForm(forms.ModelForm):
    """
    ฟอร์มสำหรับเพิ่ม/แก้ไขข้อมูลเครื่องจักร
    ประกอบด้วยข้อมูลพื้นฐานของเครื่องจักร เช่น รหัส ชื่อ ประเภท สถานที่ 
    หมายเลขเครื่อง วันที่ซื้อ รูปภาพ และสถานะการใช้งาน
    """
    class Meta:
        model = Machine
        fields = ['code', 'name', 'category', 'location', 'serial_no', 'purchase_date', 'image', 'is_active']

class MaintenancePlanForm(forms.ModelForm):
    """
    ฟอร์มสำหรับสร้าง/แก้ไขแผนการบำรุงรักษาตามกำหนด
    กำหนดความถี่การบำรุงรักษา เช่น ทุก 30 วัน, ทุก 3 เดือน
    ระบบจะคำนวณวันครบกำหนดครั้งถัดไปอัตโนมัติ
    """
    class Meta:
        model = MaintenancePlan
        fields = ['machine', 'title', 'description', 'frequency_value', 'frequency_unit', 'last_done_date']

class WorkOrderForm(forms.ModelForm):
    """
    ฟอร์มสำหรับสร้าง/แก้ไขใบสั่งงานบำรุงรักษา
    ครอบคลุมงานทุกประเภท PM (ตามแผน), CM (แก้ไขเสีย), INS (ตรวจสอบ)
    รวมการกำหนด Priority, Status, ผู้รับผิดชอบ และกำหนดเวลา
    """
    class Meta:
        model = WorkOrder
        fields = ['code', 'wo_type', 'priority', 'status', 'machine', 'plan',
                  'due_date', 'started_at', 'finished_at', 'summary', 'notes']

# Inline FormSet สำหรับการจัดการ Work Order Tasks
# ใช้สำหรับเพิ่ม/ลบ/แก้ไขรายการงานย่อยใน Work Order แบบ dynamic
# สามารถเพิ่มงานใหม่ (extra=1) และลบงานที่ไม่ต้องการ (can_delete=True)
WorkOrderTaskFormSet = inlineformset_factory(
    WorkOrder, WorkOrderTask,
    fields=['title', 'is_done'],
    extra=1, can_delete=True
)

class AttachmentForm(forms.ModelForm):
    """
    ฟอร์มสำหรับอัปโหลดไฟล์แนบรูปภาพ
    สามารถแนบกับเครื่องจักร (Machine) หรือใบสั่งงาน (WorkOrder)
    ใช้สำหรับเก็บหลักฐาน รูปผลงาน หรือรูปความเสียหาย
    """
    class Meta:
        model = Attachment
        fields = ['machine', 'workorder', 'file']