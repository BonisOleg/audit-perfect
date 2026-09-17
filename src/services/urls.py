from django.urls import path

from src.services import views

app_name = "services"

urlpatterns = [
    path("", views.ServiceListView.as_view(), name="list"),
    path(
        "pryznachennya-krytychnosti/",
        views.CriticalityRedirectView.as_view(),
        name="criticality-redirect",
    ),
    path("<slug:slug>/", views.ServiceDetailView.as_view(), name="detail"),
]
