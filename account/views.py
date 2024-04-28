from django.contrib.auth import views, logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import FormView
from account.forms import RegistrationForm, LoginForm


class LogoutUserView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy("home"))


class LoginView(views.LoginView):
    form_class = LoginForm
    success_url = reverse_lazy("home")


class RegistrationView(FormView):
    """
    View for customer registration.
    """

    form_class = RegistrationForm
    template_name = "registration/registation.html"
    success_url = reverse_lazy("account:login")

    def form_valid(self, form):
        if form.is_valid():
            form.save(commit=True)
        return super().form_valid(form)
