"""User App URL Configuration"""

from django.urls import path
from staff.views import user_profile, activate_user, Users_list, signin_view, signout_view,signup_view, deactivate_user_view, user_profile_edit, change_profile_password, deactivate_user, mnotstaff_user,mstaff_user
from django.conf import settings



urlpatterns = [
    # path(settings.LOGIN_URL, UsersListView.as_view(), name='user_profile'),
    path(settings.LOGIN_URL, user_profile, name='user_profile'),
    path('', signin_view, name='signin'),
    path('signout/', signout_view, name='signout'),
    path('signup/', signup_view, name='signup'),
    path('profile/deactivate/', deactivate_user_view, name='deactivate'),# self deactivation
    path('profile/edit/', user_profile_edit, name='edit_profile'),# self profile edit
    path('profile/change_password/', change_profile_password, name='change_password'),# self password change
    path('profile/<int:pk>/deactivate', deactivate_user, name='deactivate_user'),# deactivate other staff user
    path('profile/<int:pk>/activate', activate_user, name='activate_user'),# activate other staff user
    path('profile/<int:pk>/mnstaff', mnotstaff_user, name='mnotstaff_user'),  # make not staff other user
    path('profile/<int:pk>/mstaff', mstaff_user, name='mstaff_user'),  # make staff other user
    path('users_lists/', Users_list.as_view(), name='users_list')

]
