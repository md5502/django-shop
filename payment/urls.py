from django.urls import path

from .views import go_to_gateway_view

app_name = "payment"

urlpatterns = [
    path("go-to/", go_to_gateway_view, name="go_to_gateway_view"),
]
