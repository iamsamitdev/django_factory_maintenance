from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
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

# เพิ่ม static files และ media files สำหรับทั้ง development และ production
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# สำหรับ production - เพิ่มการให้บริการไฟล์ media โดยตรง
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]