from django.shortcuts import render


def page_not_found(request, exception):
    request.current_nav = ""
    return render(
        request,
        "pages/404.html",
        {
            "meta_title": "Сторінку не знайдено — Аудит-Перфект",
            "meta_description": "Запитану сторінку не знайдено.",
        },
        status=404,
    )
