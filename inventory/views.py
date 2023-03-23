from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from inventory.models import InventoryModel, OSModel, FactoryModel, HistoryData, MainDomain
from CIMS.utils import StaffProfileRequiredMixin


class DomainCreateView(LoginRequiredMixin, StaffProfileRequiredMixin, CreateView):
    '''Inventory item CreateView implementation'''
    model = MainDomain
    template_name = 'domain_create.html'
    fields = ['domain_name']
    success_url = reverse_lazy('inventory_list')
class InventoryListView(LoginRequiredMixin, ListView):
    '''Inventory ListView implementation'''
    model = InventoryModel
    template_name = 'invetory_all.html'
    context_object_name = 'inventory'
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get("paginate_by", self.paginate_by)


class InventoryCreateView(LoginRequiredMixin, StaffProfileRequiredMixin, CreateView):
    '''Inventory item CreateView implementation'''
    model = InventoryModel
    template_name = 'inventory_create.html'
    fields = ['username', 'type_name', 'factory_name', 'model_name', 'op_system', 'cpu_capacity',
              'ram_capacity', 'ssd_capacity', 'serial_number', 'status', 'price_buy', 'price_today', 'comment']
    success_url = reverse_lazy('inventory_list')


class InventoryDetailsView(LoginRequiredMixin, DetailView):
    '''Inventory item DetailView implementation'''
    model = InventoryModel
    template_name = 'inventory_details.html'
    def get_context_data(self, **kwargs):
        """
        This has been overridden to add `history` to the template context,
        now you can use {{ history }} within the template
        """
        context = super().get_context_data(**kwargs)
        context['history'] = HistoryData.objects.all().order_by('-pk')
        return context


class InvetoryUpdateView(StaffProfileRequiredMixin, UpdateView):
    '''Inventory item UpdateView implementation'''
    model = InventoryModel
    template_name = 'inventory_update.html'
    fields = ['username', 'type_name', 'factory_name', 'model_name', 'op_system', 'cpu_capacity',
              'ram_capacity', 'ssd_capacity', 'serial_number', 'status', 'price_buy', 'price_today', 'comment']


class OSFListView(LoginRequiredMixin, ListView):
    '''OS and Factory ListView implementation'''
    model = OSModel
    template_name = 'systems.html'

    def get_context_data(self):
        context = super(OSFListView, self).get_context_data()
        context['os_list'] = OSModel.objects.all()
        context['factory_list'] = FactoryModel.objects.all()
        return context


class OSCreateView(LoginRequiredMixin, StaffProfileRequiredMixin, CreateView):
    '''Operation System CreateView implementation'''
    model = OSModel
    template_name = 'os_create.html'
    fields = '__all__'
    success_url = reverse_lazy('system_list')


class OSDeleteView(LoginRequiredMixin,StaffProfileRequiredMixin,DeleteView):
    '''Operation System DeleteView implementation'''
    model = OSModel
    success_url = reverse_lazy('system_list')
class FactoryCreateView(LoginRequiredMixin, StaffProfileRequiredMixin, CreateView):
    '''Factory CreateViee implementation'''
    model = FactoryModel
    template_name = 'factory_create.html'
    fields = '__all__'
    success_url = reverse_lazy('system_list')

class FactoryDeleteView(LoginRequiredMixin,StaffProfileRequiredMixin,DeleteView):
    '''Factory DeleteView implementation'''
    model = FactoryModel
    success_url = reverse_lazy('system_list')