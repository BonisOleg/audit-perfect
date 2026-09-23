from django.views.generic import TemplateView

from src.core.seo import apply_page_meta
from src.news.models import News
from src.pages.models import AboutPage, HomePage
from src.services.models import Service


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get(self, request, *args, **kwargs):
        request.current_nav = "home"
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = HomePage.load()
        ctx["page"] = page
        ctx["hero"] = page.hero_media()
        ctx["why_items"] = page.why_items
        ctx["services"] = Service.objects.filter(is_active=True).order_by("sort_order")
        ctx["latest_news"] = News.objects.filter(is_published=True)[:3]
        apply_page_meta(ctx, "home", page)
        return ctx


class AboutView(TemplateView):
    template_name = "pages/about.html"

    def get(self, request, *args, **kwargs):
        request.current_nav = "about"
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = AboutPage.load()
        ctx["page"] = page
        ctx["stat_items"] = page.stat_items
        ctx["team"] = page.members.filter(is_active=True).order_by("sort_order")
        ctx["cases"] = page.work_cases.filter(is_active=True).order_by("sort_order")
        ctx["certificates"] = page.certificates.filter(
            is_active=True,
        ).exclude(image="").order_by("sort_order", "id")
        apply_page_meta(ctx, "about", page)
        return ctx


class ContactsView(TemplateView):
    template_name = "pages/contacts.html"

    def get(self, request, *args, **kwargs):
        request.current_nav = "contacts"
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        apply_page_meta(ctx, "contacts")
        return ctx


class PolicyView(TemplateView):
    template_name = "pages/policy.html"

    def get(self, request, *args, **kwargs):
        request.current_nav = ""
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        apply_page_meta(ctx, "policy")
        return ctx
