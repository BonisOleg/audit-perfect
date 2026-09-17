from django.views.generic import TemplateView

from src.core.models import SiteBlock
from src.news.models import News
from src.services.models import Service
from src.team.models import Case, TeamMember


def _blocks(page: str) -> dict[str, SiteBlock]:
    return {
        b.key: b
        for b in SiteBlock.objects.filter(page=page, is_visible=True)
    }


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get(self, request, *args, **kwargs):
        request.current_nav = "home"
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["blocks"] = _blocks("home")
        ctx["services"] = Service.objects.filter(is_active=True).order_by("sort_order")
        ctx["latest_news"] = News.objects.filter(is_published=True)[:3]
        ctx["meta_title"] = "Аудит-Перфект — аудит, облік і супровід бізнесу"
        ctx["meta_description"] = (
            "Супроводжуємо бізнес у звітності, перевірках "
            "і призначенні статусу критично важливого підприємства."
        )
        return ctx


class AboutView(TemplateView):
    template_name = "pages/about.html"

    def get(self, request, *args, **kwargs):
        request.current_nav = "about"
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["blocks"] = _blocks("about")
        ctx["team"] = TeamMember.objects.filter(is_active=True).order_by("sort_order")
        ctx["cases"] = Case.objects.filter(is_active=True).order_by("sort_order")
        ctx["meta_title"] = "Про нас — Аудит-Перфект"
        ctx["meta_description"] = (
            "ПП «АФ «Аудит-Перфект»»: аудит, облік, ТЦ, КІК, військовий облік "
            "та юридичний супровід з 2007 року."
        )
        return ctx


class ContactsView(TemplateView):
    template_name = "pages/contacts.html"

    def get(self, request, *args, **kwargs):
        request.current_nav = "contacts"
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["meta_title"] = "Контакти — Аудит-Перфект"
        ctx["meta_description"] = (
            "Телефон, email, адреса офісу Аудит-Перфект у Києві, "
            "графік роботи та як дістатися."
        )
        return ctx


class PolicyView(TemplateView):
    template_name = "pages/policy.html"

    def get(self, request, *args, **kwargs):
        request.current_nav = ""
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["meta_title"] = "Політика конфіденційності — Аудит-Перфект"
        ctx["meta_description"] = (
            "Як Аудит-Перфект обробляє персональні дані відвідувачів сайту."
        )
        return ctx
