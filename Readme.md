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

### Backend & Framework
- **Backend**: Django 5.2.5
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Web Server**: Gunicorn + Nginx (Production) / Django Dev Server (Development)
- **Static Files**: WhiteNoise + Nginx
- **Image Processing**: Pillow

### Frontend & UI
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Icons**: Bootstrap Icons
- **Responsive Design**: Mobile-first approach

### Containerization & Deployment
- **Docker**: Container platform
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Reverse proxy and static file server
- **Environment Management**: .env files for configuration

### Development & Production
- **Development**: Django runserver, SQLite
- **Production**: Gunicorn, PostgreSQL, Docker containers
- **Static Collection**: Automatic via entrypoint script

## 📁 โครงสร้างโปรเจ็กต์

```
factory_maintenance/
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── db.sqlite3                    # SQLite database (dev)
├── README.md                     # โปรเจ็กต์ documentation
├── README-Docker.md              # Docker deployment documentation
├── Day2-DjangoMinebea.md         # Training documentation
│
├── 🐳 Docker Files               # Docker configuration
├── Dockerfile                    # Docker image build instructions
├── docker-compose.yml            # Docker services orchestration
├── .dockerignore                 # Files to exclude from Docker build
├── nginx.conf                    # Nginx reverse proxy configuration
├── entrypoint.sh                 # Container startup script
├── .env                          # Environment variables (create from .env.example)
├── .env.example                  # Environment variables template
│
├── env/                          # Virtual environment (local development)
│   ├── Scripts/                  # Python executables
│   └── Lib/                      # Python packages
│
├── volumes/                      # Docker persistent data
│   ├── postgres_data/            # PostgreSQL database files
│   ├── static_volume/            # Collected static files
│   └── media_volume/             # User uploaded files
│
├── factory_maintenance/          # Main project directory
│   ├── __init__.py
│   ├── settings.py               # Django settings (reads from .env)
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
│   │   ├── __init__.py
│   │   └── 0001_initial.py       # Initial database schema
│   └── fixtures/                 # Initial data
│       └── initial_full.json     # Sample data for loaddata
│
├── templates/                    # HTML templates
│   └── maintenance/
│       ├── base.html             # Base template with Bootstrap
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
│       │   ├── styles.css        # Custom styles
│       │   └── bootstrap.min.css # Bootstrap CSS
│       ├── js/                   # JavaScript files
│       │   ├── scripts.js        # Custom scripts
│       │   └── bootstrap.min.js  # Bootstrap JS
│       ├── images/               # Static images
│       ├── fonts/                # Font files
│       └── bootstrap-icons/      # Bootstrap icons
│
├── staticfiles/                  # Collected static files (production)
│   └── maintenance/              # Auto-generated by collectstatic
├── media/                        # User uploaded files (development)
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

## 🐳 Docker Deployment (แนะนำ)

### Quick Start with Docker
```bash
# 1. Clone project
git clone <repository-url>
cd factory_maintenance

# 2. Copy environment file
cp .env.example .env

# 3. Edit .env with your settings
nano .env

# 4. Start with Docker Compose
docker compose up --build -d

# 5. Access application
# Development: http://localhost:8000
# Production (with Nginx): docker compose --profile production up --build -d
# Production access: http://localhost:8080
```

### Docker Files
- **Dockerfile**: กำหนด Django container image
- **docker-compose.yml**: จัดการ services (web, db, nginx)
- **nginx.conf**: Reverse proxy configuration
- **entrypoint.sh**: Startup script (migrate, collectstatic, loaddata)
- **.dockerignore**: ไฟล์ที่ไม่ต้องใส่ใน Docker image

### Environment Variables (.env)
```env
# Django
SECRET_KEY=your-secret-key
DEBUG=False
DJANGO_SETTINGS_MODULE=factory_maintenance.settings

# Database
DB_NAME=factory_maintenance
DB_USER=maintenance_user
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432

# Superuser (auto-created)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@minebea.com
DJANGO_SUPERUSER_PASSWORD=admin123
```

### Docker Commands
```bash
# Development mode
docker compose up --build -d

# Production mode (with Nginx)
docker compose --profile production up --build -d

# View logs
docker compose logs -f web
docker compose logs -f nginx

# Stop and cleanup
docker compose down -v
```

📖 **สำหรับรายละเอียด Docker deployment ดูที่**: [README-Docker.md](README-Docker.md)

---

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

### 🐳 Docker Production (แนะนำ)
```bash
# 1. ใช้ production profile
docker compose --profile production up --build -d

# 2. เข้าผ่าน Nginx (port 8080)
# http://yourdomain.com:8080

# 3. Static files จะถูก serve โดย Nginx
# 4. Database เก็บใน volumes/postgres_data/
```

### 🔧 Manual Deployment

#### 1. ตั้งค่า Environment Variables
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=your-production-secret-key
```

#### 2. ใช้ฐานข้อมูล PostgreSQL
- ตั้งค่าใน `.env` ตามตัวอย่างข้างบน
- ตรวจสอบว่า PostgreSQL service ทำงาน

#### 3. ใช้ Web Server ที่เหมาะสม
- **Docker + Nginx** (แนะนำ - รวมอยู่ในโปรเจ็กต์)
- **Gunicorn** (สำหรับ Linux manual deployment)
- **Waitress** (สำหรับ Windows manual deployment)

#### 4. การจัดการ Static Files
```bash
# Docker: ทำอัตโนมัติใน entrypoint.sh
# Manual: รัน collectstatic ก่อน deploy
python manage.py collectstatic --noinput
```

### 🚀 Production Deployment Options

#### ตัวเลือกที่ 1: Docker (แนะนำ)
```bash
# Complete production setup
docker compose --profile production up --build -d
```

#### ตัวเลือกที่ 2: Manual Deployment
```bash
# Traditional deployment
python -m gunicorn factory_maintenance.wsgi:application
```

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
- **วันที่อัปเดต**: กันยายน 2025
- **เวอร์ชัน**: 1.1.0 (Docker Ready)
- **Repository**: [GitHub Repository](https://github.com/iamsamitdev/django_factory_maintenance)

## 📚 เอกสารเพิ่มเติม

- **Docker Deployment**: [README-Docker.md](README-Docker.md)
- **Training Materials**: [Day2-DjangoMinebea.md](Day2-DjangoMinebea.md)
- **Django Documentation**: [docs.djangoproject.com](https://docs.djangoproject.com/)
- **Docker Documentation**: [docs.docker.com](https://docs.docker.com/)

## 📝 License

โปรเจ็กต์นี้พัฒนาขึ้นเพื่อการฝึกอบรมและการศึกษา

---

**หมายเหตุ**: โปรเจ็กต์นี้เป็นส่วนหนึ่งของการฝึกอบรม Django Framework สำหรับระบบจัดการการบำรุงรักษาในโรงงาน

**🐳 Docker Ready**: โปรเจ็กต์นี้พร้อมใช้งานบน Docker containers สำหรับ development และ production deployment
