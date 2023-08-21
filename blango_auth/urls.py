from django.urls import path, include

from django_registration.backends.activation.views import RegistrationView

from blango_auth.forms import BlangoRegistrationForm
from blango_auth.views import profile

app_name = "blango_auth"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("profile/", profile, name="profile"),
    path(
      "register/",
      RegistrationView.as_view(form_class=BlangoRegistrationForm),
      name="django_registration_register"
    ),
    
]