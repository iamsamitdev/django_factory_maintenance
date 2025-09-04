## Django MVC for Minebea
---
## ⚡ Day 2
## 🏭 ระบบซ่อมบำรุงโรงงาน (Factory Maintenance System)

โครงการนี้เป็นระบบซ่อมบำรุงสำหรับโรงงาน ที่ใช้ **Django 5.2 + PostgreSQL**  
รองรับการจัดการเครื่องจักร แผนซ่อมบำรุง ใบงานซ่อม และการอัปโหลดรูปภาพ  
ออกแบบเพื่อสอนผู้เริ่มต้นให้เข้าใจการพัฒนาเว็บแอปด้วย Python Django

---

## 🛠 Tech Stack

### Backend
- **Python 3.12+**
- **Django 5.2** (MTV framework)
- **Django Admin** สำหรับจัดการข้อมูล
- **Pillow** → ใช้งาน `ImageField` สำหรับอัปโหลดรูป
- **psycopg2-binary** → เชื่อมต่อ PostgreSQL

### Database
- **PostgreSQL** → เก็บข้อมูลเครื่องจักร, แผน PM, Work Order, รูปแนบ

### Frontend (UI Layer)
- **Django Templates** → สร้าง HTML UI
- **Bootstrap v5** → CSS framework
- **Custom CSS/JS** → styles.css, preview.js

### Static/Media
- **Static files** → เก็บ CSS/JS
- **Media files** → เก็บไฟล์อัปโหลด (รูปเครื่องจักร, ไฟล์แนบ)

### Authentication
- **Django Auth** → ระบบ Login/Logout/Register
- รองรับ **Groups/Permissions** สำหรับการกำหนดสิทธิ์

---

## 📋 ความต้องการระบบพื้นฐาน (System Requirements)

### ฟีเจอร์หลัก
1. **การจัดการเครื่องจักร (Machine Management)**
   - เพิ่ม/แก้ไข/ลบเครื่องจักร
   - อัปโหลดรูปภาพเครื่องจักร
   - จัดหมวดหมู่ (Category) และตำแหน่งติดตั้ง (Location)

2. **การจัดการแผนซ่อมบำรุง (Maintenance Plan)**
   - กำหนดรอบการซ่อมบำรุง (รายวัน, รายสัปดาห์, รายเดือน)
   - ระบบคำนวณ **วันครบกำหนดครั้งถัดไป**
   - แสดงเครื่องจักรที่ **ใกล้ถึงกำหนด** หรือ **เลยกำหนด**

3. **การจัดการใบงานซ่อม (Work Order Management)**
   - ออกใบงาน (Preventive, Corrective, Inspection)
   - กำหนดความสำคัญ (Low, Medium, High)
   - ระบุสถานะ (Open, In Progress, Done, Cancelled)
   - ระบุผู้แจ้งซ่อม / ผู้รับผิดชอบ
   - ใส่ **งานย่อย (Tasks)** ผ่าน Inline Form

4. **การแนบไฟล์ (Attachments)**
   - อัปโหลดรูปภาพหรือไฟล์แนบในเครื่องจักร/ใบงาน
   - แสดงรูปพรีวิวในหน้า UI

5. **Dashboard (สรุปภาพรวม)**
   - จำนวนเครื่องจักรทั้งหมด
   - จำนวนใบงานที่เปิดอยู่
   - แสดง **PM ที่ใกล้ถึงกำหนดใน 7 วัน**

---

### ฟีเจอร์เสริม (Optional)
- ระบบค้นหาและกรอง (Search/Filter)
- การกำหนดสิทธิ์การเข้าถึง (Technician vs Supervisor)
- Export ข้อมูลเป็น CSV/Excel
- พิมพ์ใบงานออกมาเป็นเอกสาร

---

## 🔧 Infrastructure & Deployment

- **Development** → `python manage.py runserver`
- **Production** → ใช้ Gunicorn/Uvicorn + Nginx
- **Static/Media** → ใช้ `collectstatic`, เก็บไฟล์บน server หรือ Cloud Storage (เช่น AWS S3)

### Step 0: เตรียมสภาพแวดล้อมและติดตั้ง
```bash 
# สร้างโฟลเดอร์โปรเจกต์
mkdir factory_maintenance
cd factory_maintenance

# สร้างและเปิดใช้งาน venv (Windows)
python -m venv env
env\Scripts\activate

# (macOS/Linux)
python3 -m venv env
source env/bin/activate

# ติดตั้งไลบรารีหลัก
pip install "Django==5.2.*" psycopg2-binary Pillow python-dotenv

# เช็ครายการติดตั้ง
pip list

# สร้างโปรเจกต์และแอป
django-admin startproject factory_maintenance .
python manage.py startapp maintenance
```
### Step 1: โครงสร้างโปรเจกต์ที่แนะนำ
```
factory_maintenance/            # root โปรเจกต์ (มี manage.py)
├── manage.py
├── requirements.txt            # (ทางเลือก) เก็บรายการไลบรารี
├── factory_maintenance/        # Django project package
│   ├── __init__.py
│   ├── settings.py             # ตั้งค่า DB, STATIC, MEDIA, TIME_ZONE ฯลฯ
│   ├── urls.py                 # รวม URL จากแอป
│   ├── wsgi.py
│   └── asgi.py
├── maintenance/                # Django app หลักของระบบซ่อมบำรุง
│   ├── __init__.py
│   ├── admin.py                # ลงทะเบียน Model ใช้งานใน Django admin
│   ├── apps.py
│   ├── forms.py                # ฟอร์มสำหรับ CRUD และ Inline ฟอร์ม
│   ├── models.py               # โครงสร้างตารางหลัก
│   ├── urls.py                 # URL ภายในแอป
│   ├── views.py                # CBV (List/Create/Update/Detail) + Dashboard
│   ├── templates/
│   │   └── maintenance/
│   │       ├── base.html       # เทมเพลตแม่ (Bootstrap 5)
│   │       ├── login.html       # หน้า Login
│   │       ├── dashboard.html  # สรุปสถานะระบบ
│   │       ├── machine_list.html
│   │       ├── machine_form.html
│   │       ├── machine_detail.html
│   │       ├── plan_list.html
│   │       ├── plan_form.html
│   │       ├── workorder_list.html
│   │       └── workorder_form.html
│   └── static/
│       └── maintenance/
│           ├── css/
│           │   └── styles.css  # ปรับแต่ง UI เพิ่มเติม
│           └── js/
│               └── preview.js  # สคริปต์พรีวิวรูป (ไม่ใส่ ; ตามที่อาจารย์ชอบ)
├── media/                      # โฟลเดอร์เก็บไฟล์อัปโหลด (dev)
└── static/                     # (ทางเลือก) ถ้าเก็บไฟล์รวมระดับโปรเจกต์

```
### Step 2: สร้างฐานข้อมูลใน PostgreSQL / SQLite 3
```bash
# เข้าสู่ psql
psql -U postgres

# สร้างฐานข้อมูล
CREATE DATABASE factory_maintenance;

# สร้างผู้ใช้และกำหนดรหัสผ่าน
CREATE USER maintenance_user WITH PASSWORD 'your_password';

# กำหนดสิทธิ์ให้ผู้ใช้
GRANT ALL PRIVILEGES ON DATABASE factory_maintenance TO maintenance_user;

# ออกจาก psql
\q
```

### Step 3: สร้างไฟล์ .env / .env.example และตั้งค่าตัวแปร
```bash
# สร้างไฟล์ .env
touch .env

# แก้ไขไฟล์ .env
nano .env
```

```env
# Django
SECRET_KEY=your_secret_key

# PostgreSQL
DB_NAME=factory_maintenance
DB_USER=postgres
DB_PASSWORD=123456
DB_HOST=localhost
DB_PORT=5432
```

### Step 4: ตั้งค่า settings.py (เชื่อม PostgreSQL + Static/Media + Timezone)
```python
# factory_maintenance/settings.py

import os
from dotenv import load_dotenv

# โหลดค่าจาก .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'maintenance',  # แอปของเรา
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],  # โฟลเดอร์เทมเพลตหลัก
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# === PostgreSQL ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'options': '-c timezone=Asia/Bangkok'
        },
    }
}

# === Internationalization / Timezone ===
LANGUAGE_CODE = 'th'
TIME_ZONE = 'Asia/Bangkok'
USE_I18N = True
USE_TZ = True

# === Static files (CSS, JavaScript, Images) ===
STATIC_URL = 'static/'

# === For dev mode
STATICFILES_DIRS = [Path.joinpath(BASE_DIR, 'static')]

# === For prod mode ===
if not DEBUG:
    STATIC_ROOT = Path.joinpath(BASE_DIR, 'staticfiles')

# === Media files (User uploads) ===
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# === Login ===
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
```
### Step 5: ออกแบบ Model (ข้อมูลหลักที่จำเป็น)
```python
# maintenance/models.py

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
```

### Step 6: สร้างและปรับใช้ Migration พร้อมสร้าง superuser
```bash
# สร้างไฟล์ migration
python manage.py makemigrations

# ผลลัพธ์ที่ได้
Migrations for 'maintenance':
  maintenance\migrations\0001_initial.py
    + Create model Location
    + Create model MachineCategory
    + Create model Machine
    + Create model MaintenancePlan
    + Create model WorkOrder
    + Create model Attachment
    + Create model WorkOrderTask

# ทำการ migrate
python manage.py migrate

# ผลลัพธ์ที่ได้
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, maintenance, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying maintenance.0001_initial... OK
  Applying sessions.0001_initial... OK

# สร้าง superuser
python manage.py createsuperuser

# กรอกข้อมูลผู้ใช้
Username (leave blank to use 'samit'): admin
Email address: admin@email.com
Password: 123456
Password (again): 123456
Bypass password validation and create user anyway? [y/N]: y
```

### Step 7: ลงทะเบียนใน Admin
```python
# maintenance/admin.py

from django.contrib import admin
from .models import MachineCategory, Location, Machine, MaintenancePlan, WorkOrder, WorkOrderTask, Attachment

@admin.register(MachineCategory)
class MachineCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'category', 'location', 'is_active']
    list_filter = ['category', 'location', 'is_active']
    search_fields = ['code', 'name', 'serial_no']

@admin.register(MaintenancePlan)
class MaintenancePlanAdmin(admin.ModelAdmin):
    list_display = ['machine', 'title', 'frequency_value', 'frequency_unit', 'last_done_date', 'next_due_date']
    list_filter = ['frequency_unit']
    search_fields = ['title', 'machine__code']

class WorkOrderTaskInline(admin.TabularInline):
    model = WorkOrderTask
    extra = 1

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ['code', 'wo_type', 'priority', 'status', 'machine', 'reported_at', 'due_date']
    list_filter = ['wo_type', 'priority', 'status']
    search_fields = ['code', 'machine__code', 'summary']
    inlines = [WorkOrderTaskInline]

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['machine', 'workorder', 'uploaded_at']
```

### Step 8: เตรียมข้อมูลเริ่มต้น (Seeder / Initial Data)
```bash
# สร้างโฟลเดอร์และไฟล์
mkdir -p maintenance/fixtures
touch maintenance/fixtures/initial_full.json
```

```json
[
  { "model": "maintenance.machinecategory", "pk": 1, "fields": { "name": "การตัด/ขึ้นรูปโลหะ", "description": "เครื่องตัด/พับ/ปั๊ม" } },
  { "model": "maintenance.machinecategory", "pk": 2, "fields": { "name": "งานเชื่อม", "description": "เชื่อมไฟฟ้า/CO2/TIG" } },
  { "model": "maintenance.machinecategory", "pk": 3, "fields": { "name": "งานกลึง/กัด", "description": "CNC/Manual Lathe/Mill" } },
  { "model": "maintenance.machinecategory", "pk": 4, "fields": { "name": "ลำเลียง", "description": "สายพาน/โรลเลอร์" } },
  { "model": "maintenance.machinecategory", "pk": 5, "fields": { "name": "อัด/ฉีด", "description": "ไฮดรอลิก/นิวเมติก" } },
  { "model": "maintenance.machinecategory", "pk": 6, "fields": { "name": "หุ่นยนต์", "description": "แขนกล/หยิบจับ" } },
  { "model": "maintenance.machinecategory", "pk": 7, "fields": { "name": "ตรวจสอบคุณภาพ", "description": "เครื่องมือวัด/ทดสอบ" } },
  { "model": "maintenance.machinecategory", "pk": 8, "fields": { "name": "บรรจุภัณฑ์", "description": "แพ็กกิ้ง/ซีล" } },
  { "model": "maintenance.machinecategory", "pk": 9, "fields": { "name": "ทำความสะอาด", "description": "ล้าง/อบ/เป่า" } },
  { "model": "maintenance.machinecategory", "pk": 10, "fields": { "name": "สาธารณูปโภค", "description": "คอมเพรสเซอร์/ชิลเลอร์/บอยเลอร์" } },


  { "model": "maintenance.location", "pk": 1, "fields": { "name": "โรงงาน 1 - ไลน์ A", "note": "การผลิตชิ้นส่วนโลหะ" } },
  { "model": "maintenance.location", "pk": 2, "fields": { "name": "โรงงาน 1 - ไลน์ B", "note": "เชื่อม/ประกอบ" } },
  { "model": "maintenance.location", "pk": 3, "fields": { "name": "โรงงาน 2 - ไลน์ A", "note": "CNC Cell" } },
  { "model": "maintenance.location", "pk": 4, "fields": { "name": "โรงงาน 2 - ไลน์ B", "note": "บรรจุภัณฑ์" } },
  { "model": "maintenance.location", "pk": 5, "fields": { "name": "คลังสินค้า", "note": "รับ-จ่ายวัตถุดิบ" } },
  { "model": "maintenance.location", "pk": 6, "fields": { "name": "ห้องตรวจสอบ", "note": "QC Lab" } },
  { "model": "maintenance.location", "pk": 7, "fields": { "name": "ยูทิลิตี้", "note": "คอมเพรสเซอร์/ชิลเลอร์" } },
  { "model": "maintenance.location", "pk": 8, "fields": { "name": "ซ่อมบำรุง", "note": "Maintenance Shop" } },
  { "model": "maintenance.location", "pk": 9, "fields": { "name": "โหลดดิ้ง", "note": "ท่าขนถ่ายสินค้า" } },
  { "model": "maintenance.location", "pk": 10, "fields": { "name": "สำนักงาน", "note": "ออฟฟิศ" } },


  { "model": "maintenance.machine", "pk": 1, "fields": { "code": "MCH-001", "name": "เครื่องตัดเลเซอร์", "category": 1, "location": 1, "serial_no": "LX-2020-001", "purchase_date": "2022-01-15", "image": null, "is_active": true } },
  { "model": "maintenance.machine", "pk": 2, "fields": { "code": "MCH-002", "name": "เครื่องพับโลหะ", "category": 1, "location": 1, "serial_no": "PB-2019-002", "purchase_date": "2019-11-20", "image": null, "is_active": true } },
  { "model": "maintenance.machine", "pk": 3, "fields": { "code": "MCH-003", "name": "เครื่องเชื่อม CO2", "category": 2, "location": 2, "serial_no": "CO2-2021-003", "purchase_date": "2021-05-10", "image": null, "is_active": true } },
  { "model": "maintenance.machine", "pk": 4, "fields": { "code": "MCH-004", "name": "CNC Lathe", "category": 3, "location": 3, "serial_no": "CNC-L-2020-004", "purchase_date": "2020-07-05", "image": null, "is_active": true } },
  { "model": "maintenance.machine", "pk": 5, "fields": { "code": "MCH-005", "name": "CNC Milling", "category": 3, "location": 3, "serial_no": "CNC-M-2018-005", "purchase_date": "2018-03-28", "image": null, "is_active": true } },
  { "model": "maintenance.machine", "pk": 6, "fields": { "code": "MCH-006", "name": "สายพานลำเลียง A", "category": 4, "location": 1, "serial_no": "CV-2020-006", "purchase_date": "2020-09-12", "image": null, "is_active": true } },
  { "model": "maintenance.machine", "pk": 7, "fields": { "code": "MCH-007", "name": "เครื่องอัดไฮดรอลิก", "category": 5, "location": 2, "serial_no": "HY-2017-007", "purchase_date": "2017-12-01", "image": null, "is_active": true } },
  { "model": "maintenance.machine", "pk": 8, "fields": { "code": "MCH-008", "name": "หุ่นยนต์หยิบจับ", "category": 6, "location": 2, "serial_no": "RB-2023-008", "purchase_date": "2023-04-22", "image": null, "is_active": true } },
  { "model": "maintenance.machine", "pk": 9, "fields": { "code": "MCH-009", "name": "เครื่อง X-Ray ตรวจสอบ", "category": 7, "location": 6, "serial_no": "XR-2019-009", "purchase_date": "2019-02-18", "image": null, "is_active": true } },
  { "model": "maintenance.machine", "pk": 10, "fields": { "code": "MCH-010", "name": "Air Compressor #1", "category": 10, "location": 7, "serial_no": "AC-2016-010", "purchase_date": "2016-06-30", "image": null, "is_active": true } },


  { "model": "maintenance.maintenanceplan", "pk": 1, "fields": { "machine": 1, "title": "ทำความสะอาดเลนส์", "description": "เช็ดทำความสะอาดเลนส์เลเซอร์", "frequency_value": 30, "frequency_unit": "DAYS", "last_done_date": "2025-07-01", "next_due_date": "2025-07-31" } },
  { "model": "maintenance.maintenanceplan", "pk": 2, "fields": { "machine": 2, "title": "หล่อลื่นแกนพับ", "description": "ตรวจและเติมจาระบี", "frequency_value": 2, "frequency_unit": "MONTHS", "last_done_date": "2025-06-15", "next_due_date": "2025-08-14" } },
  { "model": "maintenance.maintenanceplan", "pk": 3, "fields": { "machine": 3, "title": "ตรวจหัวเชื่อม", "description": "ตรวจหัวปืน/สายไฟ/แก๊ส", "frequency_value": 2, "frequency_unit": "WEEKS", "last_done_date": "2025-08-01", "next_due_date": "2025-08-15" } },
  { "model": "maintenance.maintenanceplan", "pk": 4, "fields": { "machine": 4, "title": "เปลี่ยนน้ำมันสไลด์", "description": "เช็กระดับและเปลี่ยน", "frequency_value": 1, "frequency_unit": "MONTHS", "last_done_date": "2025-07-10", "next_due_date": "2025-08-09" } },
  { "model": "maintenance.maintenanceplan", "pk": 5, "fields": { "machine": 5, "title": "ตั้งศูนย์เครื่อง", "description": "calibrate ปีละ 2 ครั้ง", "frequency_value": 6, "frequency_unit": "MONTHS", "last_done_date": "2025-03-01", "next_due_date": "2025-08-28" } },
  { "model": "maintenance.maintenanceplan", "pk": 6, "fields": { "machine": 6, "title": "เช็กลูกปืนโรลเลอร์", "description": "ฟังเสียง/ตรวจระยะคลอน", "frequency_value": 14, "frequency_unit": "DAYS", "last_done_date": "2025-08-05", "next_due_date": "2025-08-19" } },
  { "model": "maintenance.maintenanceplan", "pk": 7, "fields": { "machine": 7, "title": "ตรวจซีลไฮดรอลิก", "description": "รั่วซึม/แรงดัน", "frequency_value": 1, "frequency_unit": "MONTHS", "last_done_date": "2025-07-20", "next_due_date": "2025-08-19" } },
  { "model": "maintenance.maintenanceplan", "pk": 8, "fields": { "machine": 8, "title": "รีเซ็ตจุดรับชิ้นงาน", "description": "re-teach จุดหยิบ/วาง", "frequency_value": 3, "frequency_unit": "MONTHS", "last_done_date": "2025-06-01", "next_due_date": "2025-08-30" } },
  { "model": "maintenance.maintenanceplan", "pk": 9, "fields": { "machine": 9, "title": "Calibrate X-Ray", "description": "สอบเทียบค่าความเข้ม", "frequency_value": 1, "frequency_unit": "MONTHS", "last_done_date": "2025-07-25", "next_due_date": "2025-08-24" } },
  { "model": "maintenance.maintenanceplan", "pk": 10, "fields": { "machine": 10, "title": "ถ่ายน้ำคอนเดนเสท", "description": "ไล่น้ำ/ทำความสะอาดกรอง", "frequency_value": 7, "frequency_unit": "DAYS", "last_done_date": "2025-08-13", "next_due_date": "2025-08-20" } },


  { "model": "maintenance.workorder", "pk": 1, "fields": { "code": "WO-0001", "wo_type": "PM", "priority": "MED", "status": "OPEN", "machine": 1, "plan": 1, "reported_by": 1, "assigned_to": null, "reported_at": "2025-08-15T08:00:00Z", "due_date": "2025-08-31", "started_at": null, "finished_at": null, "summary": "PM ทำความสะอาดเลนส์", "notes": "" } },
  { "model": "maintenance.workorder", "pk": 2, "fields": { "code": "WO-0002", "wo_type": "CM", "priority": "HIGH", "status": "IN_PROGRESS", "machine": 3, "plan": null, "reported_by": 1, "assigned_to": 1, "reported_at": "2025-08-16T02:30:00Z", "due_date": "2025-08-20", "started_at": "2025-08-16T03:00:00Z", "finished_at": null, "summary": "หัวเชื่อม CO2 ไฟไม่ออก", "notes": "ตรวจสายดิน/แก๊ส" } },
  { "model": "maintenance.workorder", "pk": 3, "fields": { "code": "WO-0003", "wo_type": "INS", "priority": "LOW", "status": "OPEN", "machine": 6, "plan": 6, "reported_by": 1, "assigned_to": null, "reported_at": "2025-08-10T10:00:00Z", "due_date": "2025-08-25", "started_at": null, "finished_at": null, "summary": "ตรวจเสียงลูกปืน", "notes": "" } },
  { "model": "maintenance.workorder", "pk": 4, "fields": { "code": "WO-0004", "wo_type": "PM", "priority": "MED", "status": "DONE", "machine": 4, "plan": 4, "reported_by": 1, "assigned_to": 1, "reported_at": "2025-08-01T01:00:00Z", "due_date": "2025-08-09", "started_at": "2025-08-08T02:00:00Z", "finished_at": "2025-08-08T05:00:00Z", "summary": "เปลี่ยนน้ำมันสไลด์", "notes": "ค่าโอเค" } },
  { "model": "maintenance.workorder", "pk": 5, "fields": { "code": "WO-0005", "wo_type": "CM", "priority": "HIGH", "status": "OPEN", "machine": 10, "plan": null, "reported_by": 1, "assigned_to": null, "reported_at": "2025-08-17T04:00:00Z", "due_date": "2025-08-19", "started_at": null, "finished_at": null, "summary": "คอมเพรสเซอร์ดับบ่อย", "notes": "สงสัยโอเวอร์ความร้อน" } },
  { "model": "maintenance.workorder", "pk": 6, "fields": { "code": "WO-0006", "wo_type": "PM", "priority": "LOW", "status": "OPEN", "machine": 2, "plan": 2, "reported_by": 1, "assigned_to": null, "reported_at": "2025-08-05T06:00:00Z", "due_date": "2025-08-14", "started_at": null, "finished_at": null, "summary": "หล่อลื่นแกนพับ", "notes": "" } },
  { "model": "maintenance.workorder", "pk": 7, "fields": { "code": "WO-0007", "wo_type": "INS", "priority": "MED", "status": "OPEN", "machine": 9, "plan": 9, "reported_by": 1, "assigned_to": null, "reported_at": "2025-08-12T07:00:00Z", "due_date": "2025-08-24", "started_at": null, "finished_at": null, "summary": "Calibrate X-Ray", "notes": "" } },
  { "model": "maintenance.workorder", "pk": 8, "fields": { "code": "WO-0008", "wo_type": "CM", "priority": "MED", "status": "IN_PROGRESS", "machine": 6, "plan": null, "reported_by": 1, "assigned_to": 1, "reported_at": "2025-08-18T01:30:00Z", "due_date": "2025-08-22", "started_at": "2025-08-18T02:00:00Z", "finished_at": null, "summary": "สายพานลื่น", "notes": "อาจต้องเปลี่ยนสายพาน" } },
  { "model": "maintenance.workorder", "pk": 9, "fields": { "code": "WO-0009", "wo_type": "PM", "priority": "LOW", "status": "DONE", "machine": 5, "plan": 5, "reported_by": 1, "assigned_to": 1, "reported_at": "2025-07-30T03:00:00Z", "due_date": "2025-08-28", "started_at": "2025-08-01T02:00:00Z", "finished_at": "2025-08-01T05:00:00Z", "summary": "ตั้งศูนย์เครื่อง CNC Mill", "notes": "" } },
  { "model": "maintenance.workorder", "pk": 10, "fields": { "code": "WO-0010", "wo_type": "PM", "priority": "MED", "status": "OPEN", "machine": 8, "plan": 8, "reported_by": 1, "assigned_to": null, "reported_at": "2025-08-10T12:00:00Z", "due_date": "2025-08-30", "started_at": null, "finished_at": null, "summary": "รีเซ็ตจุดรับชิ้นงานหุ่นยนต์", "notes": "" } },


  { "model": "maintenance.workordertask", "pk": 1, "fields": { "workorder": 1, "title": "ถอดฝาครอบ/เช็ดเลนส์", "is_done": false } },
  { "model": "maintenance.workordertask", "pk": 2, "fields": { "workorder": 2, "title": "ตรวจสายไฟ/หัวปืน", "is_done": true } },
  { "model": "maintenance.workordertask", "pk": 3, "fields": { "workorder": 3, "title": "ฟังเสียงลูกปืน", "is_done": false } },
  { "model": "maintenance.workordertask", "pk": 4, "fields": { "workorder": 4, "title": "ระบายน้ำมันเก่า", "is_done": true } },
  { "model": "maintenance.workordertask", "pk": 5, "fields": { "workorder": 5, "title": "ตรวจพัดลม/ตะแกรงกรอง", "is_done": false } },
  { "model": "maintenance.workordertask", "pk": 6, "fields": { "workorder": 6, "title": "จาระบีแกน X/Y", "is_done": false } },
  { "model": "maintenance.workordertask", "pk": 7, "fields": { "workorder": 7, "title": "สอบเทียบค่าความเข้ม", "is_done": false } },
  { "model": "maintenance.workordertask", "pk": 8, "fields": { "workorder": 8, "title": "ตั้งความตึงสายพาน", "is_done": false } },
  { "model": "maintenance.workordertask", "pk": 9, "fields": { "workorder": 9, "title": "เช็กสแตนดาร์ดบล็อก", "is_done": true } },
  { "model": "maintenance.workordertask", "pk": 10, "fields": { "workorder": 10, "title": "Teach จุดหยิบ/วาง ใหม่", "is_done": false } },


  { "model": "maintenance.attachment", "pk": 1, "fields": { "machine": 1, "workorder": null, "file": null, "uploaded_at": "2025-08-10T00:00:00Z" } },
  { "model": "maintenance.attachment", "pk": 2, "fields": { "machine": 2, "workorder": null, "file": null, "uploaded_at": "2025-08-11T00:00:00Z" } },
  { "model": "maintenance.attachment", "pk": 3, "fields": { "machine": 3, "workorder": null, "file": null, "uploaded_at": "2025-08-12T00:00:00Z" } },
  { "model": "maintenance.attachment", "pk": 4, "fields": { "machine": 4, "workorder": null, "file": null, "uploaded_at": "2025-08-13T00:00:00Z" } },
  { "model": "maintenance.attachment", "pk": 5, "fields": { "machine": 5, "workorder": null, "file": null, "uploaded_at": "2025-08-14T00:00:00Z" } },
  { "model": "maintenance.attachment", "pk": 6, "fields": { "machine": null, "workorder": 2, "file": null, "uploaded_at": "2025-08-16T00:00:00Z" } },
  { "model": "maintenance.attachment", "pk": 7, "fields": { "machine": null, "workorder": 4, "file": null, "uploaded_at": "2025-08-08T06:00:00Z" } },
  { "model": "maintenance.attachment", "pk": 8, "fields": { "machine": null, "workorder": 5, "file": null, "uploaded_at": "2025-08-17T05:00:00Z" } },
  { "model": "maintenance.attachment", "pk": 9, "fields": { "machine": null, "workorder": 8, "file": null, "uploaded_at": "2025-08-18T03:00:00Z" } },
  { "model": "maintenance.attachment", "pk": 10, "fields": { "machine": null, "workorder": 10, "file": null, "uploaded_at": "2025-08-10T13:00:00Z" } }
]
```
```bash
# โหลดข้อมูล
python manage.py loaddata initial_full.json
```

### Step 9: ฟอร์มสำหรับ CRUD + Inline Formset (งานย่อยใน WO)
```python
# maintenance/forms.py

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

```

### Step 10: URL รวม
```python
# maintenance/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),

    path('machines/', views.MachineListView.as_view(), name='machine_list'),
    path('machines/create/', views.MachineCreateView.as_view(), name='machine_create'),
    path('machines/<int:pk>/', views.MachineDetailView.as_view(), name='machine_detail'),
    path('machines/<int:pk>/edit/', views.MachineUpdateView.as_view(), name='machine_edit'),

    path('plans/', views.PlanListView.as_view(), name='plan_list'),
    path('plans/create/', views.PlanCreateView.as_view(), name='plan_create'),
    path('plans/<int:pk>/edit/', views.PlanUpdateView.as_view(), name='plan_edit'),

    path('workorders/', views.WorkOrderListView.as_view(), name='workorder_list'),
    path('workorders/create/', views.WorkOrderCreateView.as_view(), name='workorder_create'),
    path('workorders/<int:pk>/edit/', views.WorkOrderUpdateView.as_view(), name='workorder_edit'),
]
```
```python
# factory_maintenance/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from maintenance.forms import BootstrapAuthenticationForm

urlpatterns = [
    path('admin/', admin.site.urls),

    # ใช้ login/logout สำเร็จรูปของ Django
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='maintenance/login.html',
            authentication_form=BootstrapAuthenticationForm
        ),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


    path('', include('maintenance.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Step 11: Views (ใช้ Generic Class-Based Views)
```python
# maintenance/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Machine, MaintenancePlan, WorkOrder
from .forms import MachineForm, MaintenancePlanForm, WorkOrderForm, WorkOrderTaskFormSet

class DashboardView(LoginRequiredMixin, TemplateView):
    """
    หน้าแดชบอร์ดหลัก แสดงภาพรวมของระบบบำรุงรักษา
    ประกอบด้วย จำนวนเครื่องจักรทั้งหมด, Work Order ที่เปิดอยู่, 
    และแผนบำรุงรักษาที่ใกล้ครบกำหนด (7 วัน)
    """
    template_name = 'maintenance/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['machine_count'] = Machine.objects.count()
        ctx['wo_open'] = WorkOrder.objects.filter(status=WorkOrder.STATUS_OPEN).count()
        ctx['due_soon'] = MaintenancePlan.due_within(days=7)  # PM ใกล้ถึงกำหนด 7 วัน
        return ctx


# ===== Machines =====
class MachineListView(LoginRequiredMixin, ListView):
    """
    หน้าแสดงรายการเครื่องจักรทั้งหมด
    รองรับการค้นหาตามชื่อหรือรหัสเครื่องจักร
    แสดงผลแบบ pagination (10 รายการต่อหน้า)
    """
    model = Machine
    template_name = 'maintenance/machine_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('category', 'location').order_by('code')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(code__icontains=q)
        return qs


class MachineCreateView(LoginRequiredMixin, CreateView):
    """
    หน้าเพิ่มเครื่องจักรใหม่
    ใช้ MachineForm สำหรับรับข้อมูล
    หลังบันทึกสำเร็จจะกลับไปหน้ารายการเครื่องจักร
    """
    model = Machine
    form_class = MachineForm
    template_name = 'maintenance/machine_form.html'
    success_url = reverse_lazy('machine_list')


class MachineUpdateView(LoginRequiredMixin, UpdateView):
    """
    หน้าแก้ไขข้อมูลเครื่องจักร
    ใช้ MachineForm เดียวกันกับการเพิ่มใหม่
    หลังบันทึกสำเร็จจะกลับไปหน้ารายการเครื่องจักร
    """
    model = Machine
    form_class = MachineForm
    template_name = 'maintenance/machine_form.html'
    success_url = reverse_lazy('machine_list')


class MachineDetailView(LoginRequiredMixin, DetailView):
    """
    หน้าแสดงรายละเอียดเครื่องจักร
    แสดงข้อมูลเครื่องจักรแบบละเอียด รวมรูปภาพ
    พร้อมลิงก์ไปยังแผนบำรุงรักษาและ Work Order ที่เกี่ยวข้อง
    """
    model = Machine
    template_name = 'maintenance/machine_detail.html'


# ===== Plans =====
class PlanListView(LoginRequiredMixin, ListView):
    """
    หน้าแสดงรายการแผนการบำรุงรักษา
    เรียงลำดับตามวันครบกำหนด (next_due_date)
    แสดงผลแบบ pagination และรวมข้อมูลเครื่องจักรที่เกี่ยวข้อง
    """
    model = MaintenancePlan
    template_name = 'maintenance/plan_list.html'
    paginate_by = 10

    def get_queryset(self):
        return MaintenancePlan.objects.select_related('machine').order_by('next_due_date')


class PlanCreateView(LoginRequiredMixin, CreateView):
    """
    หน้าสร้างแผนการบำรุงรักษาใหม่
    คำนวณวันครบกำหนดครั้งถัดไปอัตโนมัติตามความถี่ที่กำหนด
    หลังบันทึกสำเร็จจะกลับไปหน้ารายการแผน
    """
    model = MaintenancePlan
    form_class = MaintenancePlanForm
    template_name = 'maintenance/plan_form.html'
    success_url = reverse_lazy('plan_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.next_due_date = obj.compute_next_due()
        obj.save()
        return redirect(self.success_url)


class PlanUpdateView(LoginRequiredMixin, UpdateView):
    """
    หน้าแก้ไขแผนการบำรุงรักษา
    คำนวณวันครบกำหนดครั้งถัดไปใหม่ตามวันที่ทำครั้งล่าสุด (last_done_date)
    หลังบันทึกสำเร็จจะกลับไปหน้ารายการแผน
    """
    model = MaintenancePlan
    form_class = MaintenancePlanForm
    template_name = 'maintenance/plan_form.html'
    success_url = reverse_lazy('plan_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.next_due_date = obj.compute_next_due(from_date=obj.last_done_date)
        obj.save()
        return redirect(self.success_url)


# ===== WorkOrders (+ Inline tasks) =====
class WorkOrderListView(LoginRequiredMixin, ListView):
    """
    หน้าแสดงรายการใบสั่งงานบำรุงรักษา
    เรียงลำดับตามวันที่รายงาน (ล่าสุดก่อน)
    รวมข้อมูลเครื่องจักรและแผนที่เกี่ยวข้อง
    """
    model = WorkOrder
    template_name = 'maintenance/workorder_list.html'
    paginate_by = 10

    def get_queryset(self):
        return WorkOrder.objects.select_related('machine', 'plan').order_by('-reported_at')


class WorkOrderCreateView(LoginRequiredMixin, CreateView):
    """
    หน้าสร้างใบสั่งงานบำรุงรักษาใหม่
    รวมการจัดการ Work Order Tasks แบบ inline formset
    สามารถเพิ่มรายการงานย่อยหลายๆ งานในหน้าเดียวกัน
    """
    model = WorkOrder
    form_class = WorkOrderForm
    template_name = 'maintenance/workorder_form.html'
    success_url = reverse_lazy('workorder_list')

    def get(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = WorkOrderTaskFormSet()
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = WorkOrderTaskFormSet(self.request.POST)
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form, 'formset': formset})


class WorkOrderUpdateView(LoginRequiredMixin, UpdateView):
    """
    หน้าแก้ไขใบสั่งงานบำรุงรักษา
    รวมการจัดการ Work Order Tasks แบบ inline formset
    สามารถเพิ่ม/ลบ/แก้ไขรายการงานย่อยได้ในหน้าเดียวกัน
    """
    model = WorkOrder
    form_class = WorkOrderForm
    template_name = 'maintenance/workorder_form.html'
    success_url = reverse_lazy('workorder_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = WorkOrderTaskFormSet(instance=self.object)
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = WorkOrderTaskFormSet(self.request.POST, instance=self.object)
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form, 'formset': formset})

```
### Step 11: เทมเพลต (Bootstrap 5 + โครง UI หลัก)
### Step 11.1 templates/maintenance/base.html
```html

{% load static %}
<!doctype html>
<html lang="th">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Factory Maintenance{% endblock %}</title>
    <link href="{% static 'maintenance/css/bootstrap.min.css' %}" rel="stylesheet">
    <link href="{% static 'maintenance/css/styles.css' %}" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    {% block extra_head %}{% endblock %}
  </head>
  <body>

    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="{% url 'dashboard' %}">
                <i class="fas fa-cogs me-2"></i>Minebea Maintenance
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'dashboard' %}">
                            <i class="fas fa-tachometer-alt me-1"></i>Dashboard
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'machine_list' %}">
                            <i class="fas fa-cogs me-1"></i>Machines
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'plan_list' %}">
                            <i class="fas fa-calendar-check me-1"></i>Plans
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'workorder_list' %}">
                            <i class="fas fa-clipboard-list me-1"></i>Work Orders
                        </a>
                    </li>
                </ul>
                
                <!-- User Info and Logout -->
                {% if user.is_authenticated %}
                <ul class="navbar-nav">
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle d-flex align-items-center" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <div class="user-avatar me-2">
                                <i class="fas fa-user-circle fa-lg"></i>
                            </div>
                            <div class="user-info mt-2">
                                <div class="user-name">{{ user.get_full_name|default:user.username }}</div>
                                <small class="user-role text-muted">
                                    {% if user.is_superuser %}
                                        <i class="fas fa-crown me-1"></i>Admin
                                    {% elif user.is_staff %}
                                        <i class="fas fa-user-tie me-1"></i>Staff
                                    {% else %}
                                        <i class="fas fa-user me-1"></i>User
                                    {% endif %}
                                </small>
                            </div>
                        </a>
                        <ul class="dropdown-menu dropdown-menu-end shadow">
                            <li>
                                <a class="dropdown-item" href="#">
                                    <i class="fas fa-user me-2"></i>โปรไฟล์
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item" href="#">
                                    <i class="fas fa-cog me-2"></i>ตั้งค่า
                                </a>
                            </li>
                            <li><hr class="dropdown-divider"></li>
                            <li>
                                <form method="post" action="{% url 'logout' %}" class="d-inline">
                                    {% csrf_token %}
                                    <button type="submit" class="dropdown-item text-danger border-0 bg-transparent w-100 text-start" onclick="return confirm('คุณต้องการออกจากระบบหรือไม่?')">
                                        <i class="fas fa-sign-out-alt me-2"></i>ออกจากระบบ
                                    </button>
                                </form>
                            </li>
                        </ul>
                    </li>
                </ul>
                {% else %}
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'login' %}">
                            <i class="fas fa-sign-in-alt me-1"></i>เข้าสู่ระบบ
                        </a>
                    </li>
                </ul>
                {% endif %}
            </div>
        </div>
    </nav>

    <main class="container">
      {% block content %}{% endblock %}
    </main>

    <script src="{% static 'maintenance/js/bootstrap.bundle.min.js' %}"></script>
    {% block extra_footer %}{% endblock %}
    <script src="{% static 'maintenance/js/preview.js' %}"></script>
    
    <style>
        .errorlist {
            color: red;
            list-style-type: none;
            padding: 0;
        }
        .user-info {
            text-align: left;
            line-height: 1.2;
        }
        
        .user-name {
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        .user-role {
            font-size: 0.75rem;
            display: block;
        }
        
        .dropdown-toggle::after {
            margin-left: 0.5rem;
        }
        
        .dropdown-menu {
            border: none;
            border-radius: 8px;
            min-width: 200px;
        }
        
        .dropdown-item {
            padding: 0.7rem 1rem;
            transition: all 0.3s ease;
        }
        
        .dropdown-item:hover {
            background-color: rgba(0, 123, 255, 0.1);
            transform: translateX(2px);
        }
        
        .dropdown-item.text-danger:hover {
            background-color: rgba(220, 53, 69, 0.1);
            color: #dc3545 !important;
        }
        
        /* Logout button styling */
        .dropdown-item.border-0 {
            padding: 0.7rem 1rem;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .dropdown-item.border-0:hover {
            background-color: rgba(220, 53, 69, 0.1);
            transform: translateX(2px);
        }
        
        .navbar-brand {
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        
        .nav-link {
            transition: all 0.3s ease;
        }
        
        .nav-link:hover {
            transform: translateY(-1px);
        }
        
        @media (max-width: 768px) {
            .user-info {
                display: none;
            }
        }
    </style>
  </body>
</html>
```
### 11.2 Dashboard ตัวอย่าง templates/maintenance/dashboard.html
```html
{% extends 'maintenance/base.html' %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<!-- Summary Cards -->
<div class="row g-3 mb-4">
  <div class="col-md-3">
    <div class="card shadow-sm border-primary">
      <div class="card-body text-center">
        <i class="fas fa-cogs fa-2x text-primary mb-2"></i>
        <div class="fs-1 fw-bold text-primary">{{ machine_count }}</div>
        <div class="text-muted">เครื่องจักรทั้งหมด</div>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card shadow-sm border-warning">
      <div class="card-body text-center">
        <i class="fas fa-clipboard-list fa-2x text-warning mb-2"></i>
        <div class="fs-1 fw-bold text-warning">{{ wo_open }}</div>
        <div class="text-muted">Work Orders เปิด</div>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card shadow-sm border-success">
      <div class="card-body text-center">
        <i class="fas fa-check-circle fa-2x text-success mb-2"></i>
        <div class="fs-1 fw-bold text-success">{{ due_soon|length }}</div>
        <div class="text-muted">PM ใกล้ครบกำหนด</div>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card shadow-sm border-info">
      <div class="card-body text-center">
        <i class="fas fa-chart-line fa-2x text-info mb-2"></i>
        <div class="fs-1 fw-bold text-info">95%</div>
        <div class="text-muted">ประสิทธิภาพระบบ</div>
      </div>
    </div>
  </div>
</div>

<!-- Charts Section -->
<div class="row g-3 mb-4">
  <!-- Bar Chart - Work Orders by Type -->
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-header bg-primary text-white">
        <h6 class="mb-0"><i class="fas fa-chart-bar me-2"></i>Work Orders ตามประเภท</h6>
      </div>
      <div class="card-body">
        <canvas id="workOrderChart" height="200"></canvas>
      </div>
    </div>
  </div>
  
  <!-- Pie Chart - Machine Status -->
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-header bg-success text-white">
        <h6 class="mb-0"><i class="fas fa-chart-pie me-2"></i>สถานะเครื่องจักร</h6>
      </div>
      <div class="card-body">
        <canvas id="machineStatusChart" height="200"></canvas>
      </div>
    </div>
  </div>
</div>

<div class="row g-3 mb-4">
  <!-- Line Chart - Maintenance Trend -->
  <div class="col-md-8">
    <div class="card shadow-sm">
      <div class="card-header bg-info text-white">
        <h6 class="mb-0"><i class="fas fa-chart-line me-2"></i>แนวโน้มการบำรุงรักษา (6 เดือนล่าสุด)</h6>
      </div>
      <div class="card-body">
        <canvas id="maintenanceTrendChart" height="150"></canvas>
      </div>
    </div>
  </div>
  
  <!-- Doughnut Chart - Priority Distribution -->
  <div class="col-md-4">
    <div class="card shadow-sm">
      <div class="card-header bg-warning text-white">
        <h6 class="mb-0"><i class="fas fa-exclamation-triangle me-2"></i>ระดับความสำคัญ</h6>
      </div>
      <div class="card-body">
        <canvas id="priorityChart" height="200"></canvas>
      </div>
    </div>
  </div>
</div>

<!-- PM Due Soon Table -->
<div class="card shadow-sm">
  <div class="card-header bg-warning text-white">
    <h6 class="mb-0"><i class="fas fa-clock me-2"></i>PM ใกล้ถึงกำหนด (7 วัน)</h6>
  </div>
  <div class="card-body">
    <div class="table-responsive">
      <table class="table table-hover align-middle">
        <thead class="table-light">
          <tr>
            <th><i class="fas fa-cog me-2"></i>เครื่องจักร</th>
            <th><i class="fas fa-clipboard me-2"></i>แผน</th>
            <th><i class="fas fa-calendar me-2"></i>กำหนด</th>
            <th><i class="fas fa-exclamation-circle me-2"></i>สถานะ</th>
          </tr>
        </thead>
        <tbody>
          {% for p in due_soon %}
            <tr>
              <td>
                <strong>{{ p.machine.code }}</strong><br>
                <small class="text-muted">{{ p.machine.name }}</small>
              </td>
              <td>{{ p.title }}</td>
              <td>
                <span class="badge bg-warning text-dark">
                  <i class="fas fa-calendar-alt me-1"></i>{{ p.next_due_date }}
                </span>
              </td>
              <td>
                <span class="badge bg-danger">
                  <i class="fas fa-exclamation-triangle me-1"></i>ใกล้ครบกำหนด
                </span>
              </td>
            </tr>
          {% empty %}
            <tr>
              <td colspan="4" class="text-center text-muted py-4">
                <i class="fas fa-check-circle fa-2x mb-2"></i><br>
                ไม่มี PM ที่ใกล้ครบกำหนด
              </td>
            </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // Chart.js default configuration
    Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
    Chart.defaults.font.size = 12;
    
    // Work Orders by Type - Bar Chart
    const ctx1 = document.getElementById('workOrderChart').getContext('2d');
    new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: ['Preventive', 'Corrective', 'Inspection'],
            datasets: [{
                label: 'จำนวน Work Orders',
                data: [25, 15, 8],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(75, 192, 192, 0.8)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 5
                    }
                }
            }
        }
    });

    // Machine Status - Pie Chart
    const ctx2 = document.getElementById('machineStatusChart').getContext('2d');
    new Chart(ctx2, {
        type: 'pie',
        data: {
            labels: ['ใช้งานปกติ', 'ต้องบำรุงรักษา', 'เสีย/หยุดใช้'],
            datasets: [{
                data: [{{ machine_count|default:0 }}, {{ due_soon|length|default:0 }}, 2],
                backgroundColor: [
                    'rgba(40, 167, 69, 0.8)',
                    'rgba(255, 193, 7, 0.8)',
                    'rgba(220, 53, 69, 0.8)'
                ],
                borderColor: [
                    'rgba(40, 167, 69, 1)',
                    'rgba(255, 193, 7, 1)',
                    'rgba(220, 53, 69, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    // Maintenance Trend - Line Chart
    const ctx3 = document.getElementById('maintenanceTrendChart').getContext('2d');
    new Chart(ctx3, {
        type: 'line',
        data: {
            labels: ['มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม'],
            datasets: [{
                label: 'PM ที่ทำเสร็จ',
                data: [12, 19, 15, 18, 22, 16],
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }, {
                label: 'CM ที่ทำเสร็จ',
                data: [8, 12, 10, 15, 9, 11],
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 5
                    }
                }
            }
        }
    });

    // Priority Distribution - Doughnut Chart
    const ctx4 = document.getElementById('priorityChart').getContext('2d');
    new Chart(ctx4, {
        type: 'doughnut',
        data: {
            labels: ['สูง', 'ปานกลาง', 'ต่ำ'],
            datasets: [{
                data: [8, {{ wo_open|default:0 }}, 15],
                backgroundColor: [
                    'rgba(220, 53, 69, 0.8)',
                    'rgba(255, 193, 7, 0.8)',
                    'rgba(40, 167, 69, 0.8)'
                ],
                borderColor: [
                    'rgba(220, 53, 69, 1)',
                    'rgba(255, 193, 7, 1)',
                    'rgba(40, 167, 69, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
});
</script>

<style>
.card {
    border-radius: 10px;
    border: none;
}

.card-header {
    border-radius: 10px 10px 0 0 !important;
    font-weight: 600;
}

.table th {
    font-weight: 600;
    border-top: none;
}

.badge {
    font-size: 0.8em;
}

@media (max-width: 768px) {
    .fs-1 {
        font-size: 2rem !important;
    }
}
</style>
{% endblock %}

{% block extra_footer %}
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
{% endblock %}
```
### 11.3 รายการเครื่องจักร templates/maintenance/machine_list.html
```html
{% extends 'maintenance/base.html' %}

{% block title %}Machines{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
  <h3 class="mb-0">Machines</h3>
  <a href="{% url 'machine_create' %}" class="btn btn-primary btn-sm">+ Add Machine</a>
</div>

<form class="row g-2 mb-3">
  <div class="col-auto">
    <input name="q" class="form-control form-control-sm" placeholder="ค้นหา code หรือชื่อ" value="{{ request.GET.q }}">
  </div>
  <div class="col-auto">
    <button class="btn btn-outline-secondary btn-sm">ค้นหา</button>
  </div>
</form>

<table class="table table-hover align-middle">
  <thead><tr><th>Code</th><th>Name</th><th>Category</th><th>Location</th><th></th></tr></thead>
  <tbody>
    {% for m in object_list %}
      <tr>
        <td>{{ m.code }}</td>
        <td><a href="{% url 'machine_detail' m.pk %}">{{ m.name }}</a></td>
        <td>{{ m.category.name }}</td>
        <td>{{ m.location }}</td>
        <td><a href="{% url 'machine_edit' m.pk %}" class="btn btn-sm btn-outline-primary">Edit</a></td>
      </tr>
    {% empty %}
      <tr><td colspan="5" class="text-muted">ยังไม่มีข้อมูล</td></tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
```
### 11.4 ฟอร์มเครื่องจักร machine_form.html (อัปโหลดรูป) templates/maintenance/machine_form.html
```html
{% extends 'maintenance/base.html' %}

{% block title %}เพิ่มเครื่องจักรใหม่{% endblock %}

{% block content %}
<h3 class="mb-3">Machine</h3>
<form method="post" enctype="multipart/form-data" class="card card-body shadow-sm">
  {% csrf_token %}
  {{ form.as_p }}
  <div class="mb-3">
    <img id="imgPreview" class="img-thumbnail" style="max-height:200px" alt="">
  </div>
  <button class="btn btn-primary">Save</button>
  <a href="{% url 'machine_list' %}" class="btn btn-secondary">Back</a>
</form>
{% endblock %}
```

### 11.5 รายละเอียดเครื่องจักร machine_detail.html template/maintenance/machine_detail.html
```html
{% extends 'maintenance/base.html' %}

{% block title %}Machine Detail{% endblock %}

{% block content %}
<h3 class="mb-3">{{ object.code }} - {{ object.name }}</h3>
<div class="row g-3">
  <div class="col-md-4">
    {% if object.image %}
      <img src="{{ object.image.url }}" class="img-fluid rounded border">
    {% else %}
      <div class="text-muted">No image</div>
    {% endif %}
  </div>
  <div class="col-md-8">
    <dl class="row">
      <dt class="col-sm-3">Category</dt><dd class="col-sm-9">{{ object.category }}</dd>
      <dt class="col-sm-3">Location</dt><dd class="col-sm-9">{{ object.location }}</dd>
      <dt class="col-sm-3">Serial</dt><dd class="col-sm-9">{{ object.serial_no|default:'-' }}</dd>
      <dt class="col-sm-3">Purchased</dt><dd class="col-sm-9">{{ object.purchase_date|date:'Y-m-d' }}</dd>
    </dl>
  </div>
</div>

<h5 class="mt-4">Maintenance Plans</h5>
<table class="table table-sm">
  <thead><tr><th>Title</th><th>Freq</th><th>Last Done</th><th>Next Due</th></tr></thead>
  <tbody>
    {% for p in object.plans.all %}
      <tr>
        <td>{{ p.title }}</td>
        <td>{{ p.frequency_value }} {{ p.get_frequency_unit_display }}</td>
        <td>{{ p.last_done_date|default:'-' }}</td>
        <td><span class="badge text-bg-warning">{{ p.next_due_date }}</span></td>
      </tr>
    {% empty %}
      <tr><td colspan="4" class="text-muted">ยังไม่มีแผน PM</td></tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
```

### 11.6 ใบงาน (workorder_list.html, workorder_form.html)
templates/maintenance/workorder_list.html
```html
{% extends 'maintenance/base.html' %}

{% block title %}Work Orders{% endblock %}

{% block content %}

<div class="d-flex justify-content-between align-items-center mb-3">
  <h3 class="mb-0">Work Orders</h3>
  <a href="{% url 'workorder_create' %}" class="btn btn-primary btn-sm">+ Add Work Order</a>
</div>

<table class="table table-hover align-middle">
  <thead>
    <tr>
      <th>Code</th>
      <th>Machine</th>
      <th>Type</th>
      <th>Priority</th>
      <th>Status</th>
      <th>Reported</th>
      <th>Due Date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    {% for wo in object_list %}
      <tr>
        <td>{{ wo.code }}</td>
        <td>{{ wo.machine.code }} - {{ wo.machine.name }}</td>
        <td>{{ wo.get_wo_type_display }}</td>
        <td>
          {% if wo.priority == "HIGH" %}
            <span class="badge bg-danger">{{ wo.get_priority_display }}</span>
          {% elif wo.priority == "MED" %}
            <span class="badge bg-warning text-dark">{{ wo.get_priority_display }}</span>
          {% else %}
            <span class="badge bg-success">{{ wo.get_priority_display }}</span>
          {% endif %}
        </td>
        <td>
          {% if wo.status == "OPEN" %}
            <span class="badge bg-secondary">{{ wo.get_status_display }}</span>
          {% elif wo.status == "IN_PROGRESS" %}
            <span class="badge bg-info text-dark">{{ wo.get_status_display }}</span>
          {% elif wo.status == "DONE" %}
            <span class="badge bg-success">{{ wo.get_status_display }}</span>
          {% else %}
            <span class="badge bg-dark">{{ wo.get_status_display }}</span>
          {% endif %}
        </td>
        <td>{{ wo.reported_at|date:"Y-m-d H:i" }}</td>
        <td>{{ wo.due_date|default:"-" }}</td>
        <td>
          <a href="{% url 'workorder_edit' wo.pk %}" class="btn btn-sm btn-outline-primary">Edit</a>
        </td>
      </tr>
    {% empty %}
      <tr>
        <td colspan="8" class="text-muted">ยังไม่มีใบงานซ่อม</td>
      </tr>
    {% endfor %}
  </tbody>
</table>

{% endblock %}
```

templates/maintenance/workorder_form.html
```html
{% extends 'maintenance/base.html' %}

{% block title %}Work Order{% endblock %}

{% block content %}
<h3 class="mb-3">Work Order</h3>
<form method="post" class="card card-body shadow-sm">
  {% csrf_token %}
  {{ form.as_p }}

  <h6 class="mt-3">Tasks</h6>
  {{ formset.management_form }}
  <table class="table table-sm">
    <thead><tr><th>Title</th><th>Done?</th><th>Delete</th></tr></thead>
    <tbody>
      {% for f in formset %}
        <tr>
          <td>{{ f.title }}</td>
          <td>{{ f.is_done }}</td>
          <td>{% if f.can_delete %}{{ f.DELETE }}{% endif %}</td>
        </tr>
      {% endfor %}
    </tbody>
  </table>

  <button class="btn btn-primary">Save</button>
  <a href="{% url 'workorder_list' %}" class="btn btn-secondary">Back</a>
</form>
{% endblock %}
```

รายการ PM plan_list.html
templates/maintenance/plan_list.html
```html
{% extends 'maintenance/base.html' %}

{% block title %}Maintenance Plans{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
  <h3 class="mb-0">Maintenance Plans</h3>
  <a href="{% url 'plan_create' %}" class="btn btn-primary btn-sm">+ Add Plan</a>
</div>

<table class="table table-hover align-middle">
  <thead>
    <tr>
      <th>Machine</th>
      <th>Title</th>
      <th>Frequency</th>
      <th>Last Done</th>
      <th>Next Due</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    {% for p in object_list %}
      <tr>
        <td>{{ p.machine.code }} - {{ p.machine.name }}</td>
        <td>{{ p.title }}</td>
        <td>{{ p.frequency_value }} {{ p.get_frequency_unit_display }}</td>
        <td>{{ p.last_done_date|default:"-" }}</td>
        <td>
          {% if p.next_due_date %}
            <span class="badge text-bg-warning">{{ p.next_due_date }}</span>
          {% else %}
            <span class="text-muted">N/A</span>
          {% endif %}
        </td>
        <td>
          <a href="{% url 'plan_edit' p.pk %}" class="btn btn-sm btn-outline-primary">Edit</a>
        </td>
      </tr>
    {% empty %}
      <tr>
        <td colspan="6" class="text-muted">ยังไม่มีแผนซ่อมบำรุง</td>
      </tr>
    {% endfor %}
  </tbody>
</table>

{% endblock %}
```

รายการ ฟอร์มแผน templates/maintenance/plan_form.html
```html
{% extends 'maintenance/base.html' %}

{% block title %}Plan Form{% endblock %}

{% block content %}

<h3 class="mb-3">Maintenance Plan</h3>

<form method="post" class="card card-body shadow-sm">
  {% csrf_token %}
  {{ form.as_p }}

  <button class="btn btn-primary">Save</button>
  <a href="{% url 'plan_list' %}" class="btn btn-secondary">Back</a>
</form>

{% endblock %}

```

### 11.7 หน้าล็อกอิน template/maintenance/login.html
```html
{% extends "maintenance/base.html" %}

{% block title %}Login{% endblock %}

{% load static %}

{% block content %}
<div class="container-fluid vh-100">
  <div class="row h-100">
    <!-- Left Column - Image -->
    <div class="col-md-6 d-flex align-items-center justify-content-center">
      <div class="text-center">
        <img src="{% static 'maintenance/images/bglogin.webp' %}" 
             alt="Factory Maintenance" 
             class="img-fluid rounded shadow" 
             style="max-width: 80%; height: auto;">
        <h4 class="mt-4 text-muted">Factory Maintenance System</h4>
        <p class="text-muted">ระบบจัดการการบำรุงรักษาเครื่องจักร</p>
      </div>
    </div>
    
    <!-- Right Column - Login Form -->
    <div class="col-md-6 d-flex align-items-center justify-content-center">
      <div class="w-100" style="max-width: 400px;">
        <div class="card shadow">
          <div class="card-body p-5">
            <h3 class="card-title text-center mb-4">เข้าสู่ระบบ</h3>
            <form method="post">
                {% csrf_token %}
                {{ form.as_p }}
            <button class="btn btn-primary w-100">Login</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
    
  label {
    padding: 0.5rem 0;
  }

  .form-control {
    border-radius: 8px;
    border: 2px solid #e9ecef;
    padding: 12px 15px;
    transition: border-color 0.3s ease;
  }
  
  .form-control:focus {
    border-color: #007bff;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
  }
  
  .btn-primary {
    border-radius: 8px;
    font-weight: 500;
    letter-spacing: 0.5px;
  }
  
  .card {
    border: none;
    border-radius: 15px;
  }
  
</style>
{% endblock %}
```
### Step 12: เตรียมสำหรับการ Deploy
```bash
# สร้างไฟล์ requirements.txt
pip freeze > requirements.txt

# อัปเกรด pip
pip install --upgrade pip

# ติดตั้ง dependencies
pip install -r requirements.txt

# ติดตั้ง Whitenoise
pip install whitenoise

# ติดตั้ง Gunicorn สำหรับการรันใน production (linux)
pip install gunicorn

# ติดตั้ง Waitress สำหรับการรันใน production (windows)
pip install waitress
```

```python
# แก้ไขไฟล์ settings.py

DEBUG = False
ALLOWED_HOSTS = ["*","yourdomain.com"]  # เพิ่ม IP ถ้าจำเป็น
CSRF_TRUSTED_ORIGINS = ["*","https://yourdomain.com", "https://www.yourdomain.com"]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # เพิ่มบรรทัดนี้
    ...
]

```
```bash
# เตรียมฐานข้อมูล + เก็บ static
python manage.py migrate
python manage.py collectstatic --noinput
```
### Step 13: ทดสอบรันโหมด production
```bash
# เริ่มต้น Gunicorn บน Linux
python -m gunicorn factory_maintenance.wsgi:application --host 0.0.0.0 --port 8000

# เริ่มต้น Waitress บน Windows
python -m waitress --listen=0.0.0.0:8000 factory_maintenance.wsgi:application
```