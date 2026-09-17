from django.urls import path

from src.pages import views

app_name = "pages"

urlpatterns = [
    path("pro-nas/", views.AboutView.as_view(), name="about"),
    path("kontakty/", views.ContactsView.as_view(), name="contacts"),
    path(
        "polityka-konfidentsiynosti/",
        views.PolicyView.as_view(),
        name="policy",
    ),
]
