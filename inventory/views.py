from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from inventory.models import InventoryModel, OSModel, FactoryModel
from CIMS.utils import StaffProfileRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

class InventoryListView(LoginRequiredMixin, ListView):
    model = InventoryModel
    template_name = 'invetory_all.html'
    context_object_name = 'inventory'
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get("paginate_by", self.paginate_by)

    # def get_context_data(self, **kwargs):
    #     context = {'inventory': InventoryModel.objects.all()}
    #     return context


class InventoryCreateView(LoginRequiredMixin, StaffProfileRequiredMixin, CreateView):
    model = InventoryModel
    template_name = 'inventory_create.html'
    fields = ['username', 'type_name', 'factory_name', 'model_name', 'op_system', 'cpu_capacity',
              'ram_capacity', 'ssd_capacity', 'serial_number', 'status', 'price_buy', 'price_today', 'comment']
    success_url = reverse_lazy('inventory_list')


class InventoryDetailsView(LoginRequiredMixin, DetailView):
    model = InventoryModel
    template_name = 'inventory_details.html'


class InvetoryUpdateView(StaffProfileRequiredMixin, UpdateView):
    model = InventoryModel
    template_name = 'inventory_update.html'
    fields = ['username', 'type_name', 'factory_name', 'model_name', 'op_system', 'cpu_capacity',
              'ram_capacity', 'ssd_capacity', 'serial_number', 'status', 'price_buy', 'price_today', 'comment']


class OSFListView(LoginRequiredMixin, ListView):
    model = OSModel
    template_name = 'systems.html'

    def get_context_data(self):
        context = super(OSFListView, self).get_context_data()
        context['os_list'] = OSModel.objects.all()
        context['factory_list'] = FactoryModel.objects.all()
        return context


class OSCreateView(LoginRequiredMixin, StaffProfileRequiredMixin, CreateView):
    model = OSModel
    template_name = 'os_create.html'
    fields = '__all__'
    success_url = reverse_lazy('system_list')


class OSDeleteView(LoginRequiredMixin,StaffProfileRequiredMixin,DeleteView):
    model = OSModel
    success_url = reverse_lazy('system_list')
class FactoryCreateView(LoginRequiredMixin, StaffProfileRequiredMixin, CreateView):
    model = FactoryModel
    template_name = 'factory_create.html'
    fields = '__all__'
    success_url = reverse_lazy('inventory_list')

class FactoryDeleteView(LoginRequiredMixin,StaffProfileRequiredMixin,DeleteView):
    model = FactoryModel
    success_url = reverse_lazy('system_list')