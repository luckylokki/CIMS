# from django import forms
# from .models import InventoryModel, OSModel, FactoryModel
#
#
# class InventoryForm(forms.ModelForm):
#     class Meta:
#         model = InventoryModel
#         fields = ['username', 'type_name', 'factory_name', 'model_name', 'op_system', 'cpu_capacity',
#                   'ram_capacity', 'ssd_capacity', 'serial_number', 'status', 'price_buy', 'price_today', 'comment']
#
#
# class OSystemForm(forms.ModelForm):
#     class Meta:
#         model = OSModel
#         fields = ['op_system']
#
#         def clean_op_system(self):
#             op_system = self.cleaned_data.get('op_system')
#             if (op_system == ""):
#                 raise forms.ValidationError('This field cannot be left blank')
#             for instance in OSModel.objects.all():
#                 if (instance.op_system == op_system):
#                     raise forms.ValidationError('The serial number is already exist')
#                 return op_system
#             return op_system
#
#
# class FactoryNameForm(forms.ModelForm):
#     class Meta:
#         model = FactoryModel
#         fields = ['factory_name']
#
#         def clean_factory_name(self):
#             factory_name = self.cleaned_data.get('factory_name')
#             if (factory_name == ""):
#                 raise forms.ValidationError('This field cannot be left blank')
#             for instance in FactoryModel.objects.all():
#                 if (instance.factory_name == factory_name):
#                     raise forms.ValidationError('The serial number is already exist')
#             return factory_name
