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
