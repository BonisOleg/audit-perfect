from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, RedirectView

from src.services.models import Service


class ServiceListView(ListView):
    model = Service
    template_name = "services/list.html"
    context_object_name = "services"

    def get_queryset(self):
        return Service.objects.filter(is_active=True).order_by("sort_order")

    def get(self, request, *args, **kwargs):
        request.current_nav = "services"
        return super().get(request, *args, **kwargs)


class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/detail.html"
    context_object_name = "service"
    slug_field = "slug"

    def get_queryset(self):
        return Service.objects.filter(is_active=True)

    def get(self, request, *args, **kwargs):
        request.current_nav = "services"
        return super().get(request, *args, **kwargs)


class CriticalityRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        service = get_object_or_404(Service, slug="viyskovyy-oblik", is_active=True)
        return service.get_absolute_url()
