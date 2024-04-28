from django.urls import path
from account.views import RegistrationView, LoginView, LogoutUserView

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
]
