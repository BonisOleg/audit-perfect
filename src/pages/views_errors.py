from django.shortcuts import render
from django.utils.translation import gettext as _


def page_not_found(request, exception):
    request.current_nav = ""
    return render(
        request,
        "pages/404.html",
        {
            "meta_title": _("Сторінку не знайдено — Аудит-Перфект"),
            "meta_description": _("Запитану сторінку не знайдено."),
        },
        status=404,
    )
