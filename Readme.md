# Factory Maintenance System

ระบบจัดการการบำรุงรักษาเครื่องจักรในโรงงาน พัฒนาด้วย Django Framework สำหรับใช้ในการจัดการข้อมูลเครื่องจักร แผนการบำรุงรักษา และใบสั่งงาน

## 🚀 Features

- **จัดการข้อมูลเครื่องจักร** - เพิ่ม แก้ไข ลบ และดูรายละเอียดเครื่องจักร
- **จัดการหมวดหมู่เครื่องจักร** - จัดประเภทเครื่องจักรตามการใช้งาน
- **จัดการสถานที่** - กำหนดตำแหน่งที่ตั้งของเครื่องจักร
- **แผนการบำรุงรักษา** - สร้างและติดตามแผนการบำรุงรักษาตามช่วงเวลา
- **ใบสั่งงานบำรุงรักษา** - สร้างและจัดการใบสั่งงานจากแผนการบำรุงรักษา
- **ระบบผู้ใช้งาน** - Authentication และ Authorization
- **อัปโหลดรูปภาพ** - เก็บรูปภาพของเครื่องจักร
- **Dashboard** - หน้าแสดงสรุปข้อมูลสำคัญ

## 🛠️ เทคโนโลยีที่ใช้

- **Backend**: Django 5.2.5
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Image Processing**: Pillow
- **Web Server**: Waitress (Production)
- **Static Files**: WhiteNoise

## 📁 โครงสร้างโปรเจ็กต์

```
factory_maintenance/
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── db.sqlite3                    # SQLite database (dev)
├── README.md                     # โปรเจ็กต์ documentation
├── Day2-DjangoMinebea.md         # Training documentation
│
├── env/                          # Virtual environment
│   ├── Scripts/                  # Python executables
│   └── Lib/                      # Python packages
│
├── factory_maintenance/          # Main project directory
│   ├── __init__.py
│   ├── settings.py               # Django settings
│   ├── urls.py                   # Main URL configuration
│   ├── wsgi.py                   # WSGI configuration
│   └── asgi.py                   # ASGI configuration
│
├── maintenance/                  # Main application
│   ├── __init__.py
│   ├── admin.py                  # Django admin configuration
│   ├── apps.py                   # App configuration
│   ├── models.py                 # Database models
│   ├── views.py                  # View functions
│   ├── urls.py                   # App URL patterns
│   ├── forms.py                  # Django forms
│   ├── tests.py                  # Unit tests
│   ├── migrations/               # Database migrations
│   └── fixtures/                 # Initial data
│       └── initial_full.json     # Sample data
│
├── templates/                    # HTML templates
│   └── maintenance/
│       ├── base.html             # Base template
│       ├── dashboard.html        # Dashboard page
│       ├── login.html            # Login page
│       ├── machine_list.html     # Machine listing
│       ├── machine_detail.html   # Machine details
│       ├── machine_form.html     # Machine form
│       ├── plan_list.html        # Maintenance plan listing
│       ├── plan_form.html        # Maintenance plan form
│       ├── workorder_list.html   # Work order listing
│       └── workorder_form.html   # Work order form
│
├── static/                       # Static files (development)
│   └── maintenance/
│       ├── css/                  # CSS files
│       ├── js/                   # JavaScript files
│       ├── images/               # Static images
│       ├── fonts/                # Font files
│       └── bootstrap-icons/      # Bootstrap icons
│
├── staticfiles/                  # Collected static files (production)
├── media/                        # User uploaded files
│   └── machines/                 # Machine images
│
```

## 🗄️ ฐานข้อมูล Schema

### หลักๆ ประกอบด้วย 6 tables:

1. **MachineCategory** - ประเภทเครื่องจักร
2. **Location** - สถานที่ตั้ง
3. **Machine** - ข้อมูลเครื่องจักร
4. **MaintenancePlan** - แผนการบำรุงรักษา
5. **WorkOrder** - ใบสั่งงานบำรุงรักษา
6. **User** - ผู้ใช้งานระบบ (Django built-in)

## 🚀 การติดตั้งและรัน

### 1. Clone โปรเจ็กต์
```bash
git clone <repository-url>
cd factory_maintenance
```

### 2. สร้าง Virtual Environment
```bash
python -m venv env
```

### 3. เปิดใช้งาน Virtual Environment
```bash
# Windows
.\env\Scripts\activate

# macOS/Linux
source env/bin/activate
```

### 4. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 5. ตั้งค่าตัวแปรสภาพแวดล้อม
สร้างไฟล์ `.env` ในโฟลเดอร์หลัก:
```env
SECRET_KEY=your-secret-key-here
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=5432
```

### 6. ตั้งค่าฐานข้อมูล
```bash
# สร้าง migrations
python manage.py makemigrations

# รัน migrations
python manage.py migrate

# โหลดข้อมูลตัวอย่าง (optional)
python manage.py loaddata maintenance/fixtures/initial_full.json
```

### 7. สร้าง Superuser
```bash
python manage.py createsuperuser
```

### 8. รวบรวม Static Files (สำหรับ Production)
```bash
python manage.py collectstatic --noinput
```

### 9. รันเซิร์ฟเวอร์

#### Development Server:
```bash
python manage.py runserver
```

#### Production Server (Waitress):
```bash
python -m waitress --listen=0.0.0.0:8000 factory_maintenance.wsgi:application
```

## 🌐 การใช้งาน

### เข้าสู่ระบบ
- URL: `http://localhost:8000/login/`
- ใช้ username และ password ที่สร้างด้วย `createsuperuser`

### หน้าหลัก (Dashboard)
- URL: `http://localhost:8000/`
- แสดงสรุปข้อมูลเครื่องจักร, แผนการบำรุงรักษา, และใบสั่งงาน

### จัดการเครื่องจักร
- URL: `http://localhost:8000/machines/`
- เพิ่ม แก้ไข ลบ และดูรายละเอียดเครื่องจักร

### จัดการแผนการบำรุงรักษา
- URL: `http://localhost:8000/plans/`
- สร้างและจัดการแผนการบำรุงรักษาตามช่วงเวลา

### จัดการใบสั่งงาน
- URL: `http://localhost:8000/workorders/`
- สร้างและติดตามใบสั่งงานจากแผนการบำรุงรักษา

### Admin Panel
- URL: `http://localhost:8000/admin/`
- จัดการข้อมูลผ่าน Django Admin

## 🛡️ การปรับแต่งสำหรับ Production

### 1. ตั้งค่า Environment Variables
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=your-production-secret-key
```

### 2. ใช้ฐานข้อมูล PostgreSQL
- ตั้งค่าใน `.env` ตามตัวอย่างข้างบน
- ตรวจสอบว่า PostgreSQL service ทำงาน

### 3. ใช้ Web Server ที่เหมาะสม
- **Waitress** (รวมอยู่ในโปรเจ็กต์)
- **Gunicorn** (สำหรับ Linux)
- **nginx** (สำหรับ reverse proxy)

### 4. การจัดการ Static Files
- รัน `collectstatic` ก่อน deploy
- ตั้งค่า web server ให้ serve static files โดยตรง

## 🧪 การทดสอบ

```bash
# รัน unit tests
python manage.py test

# รัน specific test
python manage.py test maintenance.tests.TestMachineModel
```

## 🤝 การพัฒนา

### โครงสร้าง Code
- ใช้ Django MVT (Model-View-Template) pattern
- แยก logic ในแต่ละ app อย่างชัดเจน
- ใช้ Bootstrap สำหรับ responsive design

### การเพิ่มฟีเจอร์ใหม่
1. เพิ่ม model ใน `models.py`
2. สร้าง migration: `python manage.py makemigrations`
3. รัน migration: `python manage.py migrate`
4. เพิ่ม view ใน `views.py`
5. เพิ่ม URL pattern ใน `urls.py`
6. สร้าง template ใน `templates/maintenance/`

## 📞 การติดต่อและการสนับสนุน

- **ผู้พัฒนา**: Django Minebea Training Team
- **วันที่สร้าง**: สิงหาคม 2025
- **เวอร์ชัน**: 1.0.0

## 📝 License

โปรเจ็กต์นี้พัฒนาขึ้นเพื่อการฝึกอบรมและการศึกษา

---

**หมายเหตุ**: โปรเจ็กต์นี้เป็นส่วนหนึ่งของการฝึกอบรม Django Framework สำหรับระบบจัดการการบำรุงรักษาในโรงงาน
