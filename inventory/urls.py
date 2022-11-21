"""User App URL Configuration"""

from django.urls import path
from django.conf import settings
from inventory.views import InventoryCreateView, InventoryListView, InventoryDetailsView, InvetoryUpdateView, \
    OSCreateView, FactoryCreateView, OSFListView, OSDeleteView, FactoryDeleteView

urlpatterns = [
    path('inventory_create/', InventoryCreateView.as_view(), name='inventory_create'),
    path('inventory_list/', InventoryListView.as_view(), name='inventory_list'),
    path('inventory_laptops_list/', InventoryListView.as_view(template_name='inventory_laptops_list.html'),
         name='inventory_laptops_list'),
    path('inventory_mobiles_list/', InventoryListView.as_view(template_name='inventory_mobiles_list.html'),
         name='inventory_mobiles_list'),
    path('inventory_monitors_list/', InventoryListView.as_view(template_name='inventory_monitors_list.html'),
         name='inventory_monitors_list'),
    path('inventory_others_list/', InventoryListView.as_view(template_name='inventory_others_list.html'),
         name='inventory_others_list'),
    path('inventory/<int:pk>/details', InventoryDetailsView.as_view(), name='inventory_details'),
    path('inventory/<int:pk>/update', InvetoryUpdateView.as_view(), name='inventory_update'),
    path('os_create/', OSCreateView.as_view(), name='os_create'),
    path('os_delete/<int:pk>', OSDeleteView.as_view(), name='os_delete'),
    path('factory_create/', FactoryCreateView.as_view(), name='factory_create'),
    path('factory_delete/<int:pk>', FactoryDeleteView.as_view(), name='factory_delete'),
    path('system_list/', OSFListView.as_view(), name='system_list'),
]
