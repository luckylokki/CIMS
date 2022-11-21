from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from staff.models import CustomUserModel
from django.contrib.admin.views.decorators import staff_member_required

from .forms import SignUpForm, SignInForm, UserProfileEdit, UserPasswordChange


@login_required()
def user_profile(request: HttpRequest) -> HttpResponse:
    return render(request, 'user_settings.html')


class Users_list(LoginRequiredMixin, TemplateView):
    template_name = 'users_list.html'

    def get_context_data(self, **kwargs):
        context = {'users': CustomUserModel.objects.all()}
        return context


# @login_required()
# def user_profile(request: HttpRequest) -> HttpResponse:
#     return render(request, 'user_profileS.html')


def signin_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return HttpResponseRedirect(reverse_lazy('inventory_list'))
            # return render(request, 'user_settings.html')
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'form': form})


def signup_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.create_user()
            return HttpResponseRedirect(reverse_lazy('users_list'))
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required()
def signout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect(reverse_lazy("signin"))


@login_required()
def deactivate_user_view(request: HttpRequest) -> HttpResponse:
    request.user.is_active = False
    request.user.save()
    logout(request)
    return HttpResponseRedirect(reverse_lazy("signin"))


@login_required()
def user_profile_edit(request: HttpRequest) -> HttpResponse:
    profile = request.user
    if request.method == 'POST':
        form = UserProfileEdit(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect(reverse_lazy('user_profile'))
    else:
        first_name = profile.first_name
        last_name = profile.last_name
        email = profile.email
        slack = profile.slack
        form = UserProfileEdit({"first_name": first_name, "last_name": last_name, "email": email,
                                "slack": slack})
    return render(request, 'user_profile_edit.html', {'form': form})


@login_required()
def change_profile_password(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        # if request.POST.get("form_type") == 'formadd':
        form = UserPasswordChange(request.POST, instance=request.user)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect(reverse_lazy('user_profile'))
    else:
        form = UserPasswordChange()
    return render(request, 'user_password_change.html', {'form': form})


@login_required()
@staff_member_required()
def deactivate_user(request: HttpRequest, pk):
    """Deactivate some user view"""
    delu = get_object_or_404(CustomUserModel, pk=pk)
    delu.is_active = False
    delu.save()
    return HttpResponseRedirect(reverse_lazy("users_list"))


@login_required()
@staff_member_required()
def activate_user(request: HttpRequest, pk):
    """Activate some user view"""
    actu = get_object_or_404(CustomUserModel, pk=pk)
    actu.is_active = True
    actu.save()
    return HttpResponseRedirect(reverse_lazy("users_list"))


@login_required()
@staff_member_required()
def mnotstaff_user(request: HttpRequest, pk):
    """Activate some user view"""
    mnstaff = get_object_or_404(CustomUserModel, pk=pk)
    mnstaff.is_staff = False
    mnstaff.save()
    return HttpResponseRedirect(reverse_lazy("users_list"))


@login_required()
@staff_member_required()
def mstaff_user(request: HttpRequest, pk):
    """Activate some user view"""
    mstaff = get_object_or_404(CustomUserModel, pk=pk)
    mstaff.is_staff = True
    mstaff.save()
    return HttpResponseRedirect(reverse_lazy("users_list"))
