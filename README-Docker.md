# Factory Maintenance System - Docker Deployment

Django-based Factory Maintenance System สำหรับการจัดการเครื่องจักรในโรงงาน Minebea

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### 1. Clone & Setup
```bash
git clone <repository-url>
cd django_factory_maintenance

# Copy environment file (if .env.example exists)
cp .env.example .env

# Edit .env file with your settings
nano .env
```

### 2. Configure Environment Variables
The project uses `.env` file for configuration. Docker Compose automatically reads this file.

**Key variables in `.env`:**
```bash
# Django Configuration
SECRET_KEY="your-secret-key-here"
DEBUG=False
DJANGO_SETTINGS_MODULE=factory_maintenance.settings

# PostgreSQL Database
DB_NAME=factory_maintenance
DB_USER=maintenance_user
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432

# Timezone & Localization (Thailand - Minebea)
TZ=Asia/Bangkok
LANGUAGE_CODE=th

# Superuser (Auto-created on first run)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@minebea.com
DJANGO_SUPERUSER_PASSWORD=admin123

# Security Settings
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

**Environment Variable Flow:**
```
.env file → docker compose.yml → Container Environment → Django Settings
```

### 2. Build & Run
```bash
# Build and start all services (reads .env automatically)
docker compose up --build -d

# Or specify custom env file
docker compose --env-file .env.production up --build -d

# Check logs
docker compose logs -f

# Check running containers
docker compose ps
```

### 3. Access Application

#### Development Mode (without Nginx)
```bash
docker compose up --build -d
```
- **Web App**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Database**: localhost:5432

#### Production Mode (with Nginx)
```bash
docker compose --profile production up --build -d
```
- **Web App**: http://localhost:8080 (via Nginx)
- **Admin Panel**: http://localhost:8080/admin
- **Direct Django**: http://localhost:8000 (bypass Nginx)
- **Database**: localhost:5432

**Default Login:**
- Username: `admin`
- Password: `admin123`

## 🏗 Architecture

### Services
1. **web** - Django application (Gunicorn)
2. **db** - PostgreSQL database
3. **nginx** - Reverse proxy (production only)

### Tech Stack
- **Backend**: Python 3.12 + Django 5.2
- **Database**: PostgreSQL 16
- **Web Server**: Gunicorn + Nginx
- **Frontend**: Bootstrap 5 + Django Templates
- **File Upload**: Pillow for image processing

### Volume Structure
```
volumes/
├── postgres_data/     # Database files
├── static_volume/     # Static files (CSS, JS, Images)
└── media_volume/      # User uploaded files
```

### Static Files & Media Handling
- **Static files** are automatically collected at container startup
- **Nginx** serves static files efficiently in production mode
- **Media files** are handled through volume mounts
- All volumes are stored in the project's `volumes/` directory

## 📁 Features
- เครื่องจักร (Machine Management)
- แผนซ่อมบำรุง (Maintenance Plans)
- ใบงานซ่อม (Work Orders)
- การแนบไฟล์ (File Attachments)
- Dashboard & Reports
- ระบบ Authentication

## 🔧 Development Commands

```bash
# Start development environment
docker compose up

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser (if not auto-created)
docker compose exec web python manage.py createsuperuser

# Load initial data
docker compose exec web python manage.py loaddata initial_full.json

# Collect static files
docker compose exec web python manage.py collectstatic

# Access Django shell
docker compose exec web python manage.py shell

# View environment variables in container
docker compose exec web env | grep DB_
docker compose exec web env | grep DJANGO_

# View logs
docker compose logs web
docker compose logs db
```

## 🧹 Cleanup & Management Commands

### Complete Cleanup (Remove Everything)
```bash
# ลบทุกสิ่งอย่างใน profile นี้
docker compose --profile production down -v --rmi all

# หรือลบเฉพาะข้อมูลข้างใน
sudo rm -rf volumes/postgres_data/*
sudo rm -rf volumes/static_volume/*

# เริ่มพร้อม nginx profile
docker compose --profile production up --build -d

# เข้าใช้งานผ่าน nginx
# http://157.230.39.181:8080
```

### Selective Cleanup
```bash
# Stop and remove containers only (keep volumes)
docker compose --profile production down

# Remove containers and volumes (keep images)
docker compose --profile production down -v

# Remove everything including images
docker compose --profile production down -v --rmi all

# Clean up unused Docker resources
docker system prune -a
```

### Container Management
```bash
# Restart specific service
docker compose restart web
docker compose restart nginx

# View real-time logs
docker compose logs -f web
docker compose logs -f nginx

# Execute commands in running container
docker compose exec web python manage.py collectstatic --noinput
docker compose exec web python manage.py migrate

# Check container resource usage
docker stats
```

## 🌍 Environment Configuration

### Multiple Environment Files
```bash
# Development
docker compose --env-file .env.development up

# Staging  
docker compose --env-file .env.staging up

# Production
docker compose --env-file .env.production up
```

### Environment Variable Precedence
1. **Shell environment** (highest priority)
2. **`.env` file** 
3. **docker compose.yml defaults** (lowest priority)

### Sensitive Data Management
```bash
# For production, use secrets or secure vault
echo "DB_PASSWORD=secure_password" >> .env
chmod 600 .env  # Restrict file permissions

# Or use Docker secrets
docker compose --env-file /secure/path/.env up
```

## 🏭 Production Deployment

### Using Nginx (recommended)
```bash
# Start with nginx profile (builds and starts all services)
docker compose --profile production up --build -d

# Check status
docker compose --profile production ps

# View logs
docker compose logs nginx
docker compose logs web

# SSL Setup (manual)
# Update nginx.conf for SSL certificates
```

### Access Points
- **Via Nginx (Recommended)**: http://157.230.39.181:8080
- **Direct Django**: http://157.230.39.181:8000
- **Admin Panel**: http://157.230.39.181:8080/admin

### Environment Variables
Key variables in `.env`:
- `DEBUG=False` (Production mode)
- `SECRET_KEY=<strong-secret>` (Change in production)
- `DB_PASSWORD=<secure-password>` (Strong database password)
- `ALLOWED_HOSTS=yourdomain.com` (Your domain)
- `CSRF_TRUSTED_ORIGINS=https://yourdomain.com` (HTTPS URLs)

### Production .env Example
```bash
# Production Configuration
DEBUG=False
SECRET_KEY="prod-secret-key-very-long-and-secure-12345"
DB_PASSWORD="very_secure_database_password"
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Database (External or managed)
DB_HOST=production-db-server.com
DB_USER=prod_maintenance_user
DB_PASSWORD=super_secure_password

# Admin User (Optional - for initial setup only)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com
DJANGO_SUPERUSER_PASSWORD=secure_admin_password
```

## 📊 Database Backup & Restore

```bash
# Backup
docker compose exec db pg_dump -U maintenance_user factory_maintenance > backup.sql

# Restore
docker compose exec -T db psql -U maintenance_user factory_maintenance < backup.sql
```

## 🔍 Troubleshooting

### Common Issues
1. **Database connection errors**
   - Check if PostgreSQL is running: `docker compose ps`
   - Check logs: `docker compose logs db`
   - Verify DB environment variables: `docker compose exec web env | grep DB_`

2. **Static files not loading (CSS/JS)**
   - Verify static files are collected: `docker compose exec web ls -la /app/staticfiles/`
   - Check Nginx is serving static files: `curl -I http://localhost:8080/static/maintenance/css/styles.css`
   - Restart containers: `docker compose --profile production down && docker compose --profile production up -d`
   - Static files are automatically collected at container startup via `entrypoint.sh`

3. **Nginx not accessible (port 8080)**
   - Ensure you're using the production profile: `docker compose --profile production up -d`
   - Check Nginx logs: `docker compose logs nginx`
   - Verify port is not in use: `netstat -tulpn | grep 8080`

4. **Permission errors with media files**
   - Check media folder permissions: `ls -la volumes/media_volume/`
   - Ensure proper volume mounting in docker compose.yml

5. **Environment variable not working**
   - Check `.env` file syntax (no spaces around `=`)
   - Verify variable names match in docker compose.yml
   - Restart containers after .env changes: `docker compose down && docker compose up`

5. **Superuser not created automatically**
   - Check environment variables: `docker compose exec web env | grep DJANGO_SUPERUSER`
   - Create manually: `docker compose exec web python manage.py createsuperuser`

### Health Checks
```bash
# Check service health
docker compose ps

# Test database connection
docker compose exec web python manage.py dbshell

# Check Django status
curl http://localhost:8000/
```

## 📝 Data Structure

### Models
- `MachineCategory` - หมวดหมู่เครื่องจักร
- `Location` - สถานที่ติดตั้ง
- `Machine` - เครื่องจักร
- `MaintenancePlan` - แผนซ่อมบำรุง
- `WorkOrder` - ใบงานซ่อม
- `WorkOrderTask` - งานย่อยในใบงาน
- `Attachment` - ไฟล์แนบ

### Default Data
- Initial categories และ locations
- Sample machines และ maintenance plans
- User permissions และ groups

---

**Created for:** Minebea Factory Maintenance System  
**Version:** 1.0.0  
**Framework:** Django 5.2 + PostgreSQL
