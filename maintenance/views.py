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