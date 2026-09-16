#!/usr/bin/env python3
"""Збирає Карта_сайту_АудитПерфект.pdf з актуальної карти v0.6."""

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = Path(__file__).with_name("Карта_сайту_АудитПерфект.pdf")
FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

RED = HexColor("#EC423C")
BLUE = HexColor("#002FA7")
INK = HexColor("#1A1A1A")
MUTED = HexColor("#5C6370")
LINE = HexColor("#D8DCE6")
WASH = HexColor("#F3F5FB")

pdfmetrics.registerFont(TTFont("Body", FONT_REG))
pdfmetrics.registerFont(TTFont("BodyBold", FONT_BOLD))


def style(name, **kwargs):
    base = dict(fontName="Body", textColor=INK, alignment=TA_LEFT, leading=16)
    base.update(kwargs)
    return ParagraphStyle(name, **base)


H1 = style("h1", fontName="BodyBold", fontSize=20, leading=24, textColor=BLUE)
H2 = style("h2", fontName="BodyBold", fontSize=13, leading=18, textColor=BLUE, spaceBefore=12)
H3 = style("h3", fontName="BodyBold", fontSize=11, leading=15, textColor=INK, spaceBefore=8)
P = style("p", fontSize=10, leading=14)
META = style("meta", fontSize=9, leading=13, textColor=MUTED)
TH = style("th", fontName="BodyBold", fontSize=9, leading=12, textColor=white)
TD = style("td", fontSize=9, leading=12, textColor=INK)


def p(text, st=P):
    return Paragraph(text, st)


def table(rows, col_widths):
    data = [[Paragraph(str(cell), TH) for cell in rows[0]]]
    data += [[Paragraph(str(cell), TD) for cell in row] for row in rows[1:]]
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, WASH]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("GRID", (0, 0), (-1, -1), 0.4, LINE),
            ]
        )
    )
    return t


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(RED)
    canvas.rect(0, A4[1] - 8 * mm, A4[0], 8 * mm, fill=1, stroke=0)
    canvas.setFillColor(BLUE)
    canvas.rect(0, 0, A4[0], 10 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Body", 8)
    canvas.drawString(18 * mm, 4 * mm, "Аудит-Перфект  ·  Карта сайту v0.6  ·  Правки 1")
    canvas.drawRightString(A4[0] - 18 * mm, 4 * mm, str(doc.page))
    canvas.restoreState()


def build():
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="Карта сайту — Аудит-Перфект",
        author="Аудит-Перфект",
    )
    w = A4[0] - 36 * mm
    story = [
        p("Карта сайту — Аудит-Перфект", H1),
        p("Версія 0.6  ·  16.09.2026  ·  українська  ·  палітра #EC423C · #FFFFFF · #002FA7", META),
        p(
            "Форм заявок немає. Шапка sticky. CTA — телефон. Бренд: Аудит-Перфект + "
            "«Аудиторська фірма». Display: Onest."
        ),
        p("Меню", H2),
        p(
            "<b>Шапка:</b> Аудит-Перфект · Головна · Про нас · "
            "Послуги · Новини · Контакти · телефон"
        ),
        p("У «Послуги» — випадаючий список <b>7</b> напрямків."),
        p(
            "<b>Підвал:</b> розділи, контакти, політика. На головній — кредит PrometeyLabs "
            "(corporate-website-v2, nofollow)."
        ),
        p("Дерево сторінок", H2),
    ]

    tree_rows = [
        ["URL", "Сторінка"],
        ["/", "Головна"],
        ["/pro-nas/", "Про нас"],
        ["/poslugy/", "Послуги"],
        ["/poslugy/audytorski/", "Аудиторські послуги"],
        ["/poslugy/buhgalterski/", "Бухгалтерські послуги"],
        ["/poslugy/transfertne-tsinoutvorennya/", "Трансфертне ціноутворення"],
        ["/poslugy/kik/", "КІК"],
        ["/poslugy/viyskovyy-oblik/", "Військовий облік"],
        ["/poslugy/yurydychni/", "Юридичні послуги"],
        ["/poslugy/kadrovyy-suprovid/", "Кадровий супровід"],
        ["/novyny/", "Новини"],
        ["/novyny/&lt;slug&gt;/", "Стаття"],
        ["/kontakty/", "Контакти"],
        ["/polityka-konfidentsiynosti/", "Політика конфіденційності"],
    ]
    story += [table(tree_rows, [w * 0.52, w * 0.48]), Spacer(1, 4 * mm)]
    story += [
        p(
            "<b>301:</b> /poslugy/pryznachennya-krytychnosti/ → /poslugy/viyskovyy-oblik/. "
            "Окремої сторінки критичності немає."
        ),
        p("1. Головна  /", H3),
    ]
    story.append(
        table(
            [
                ["Блок", "Зміст"],
                ["Банер", "головний слоган і телефон у шапці"],
                [
                    "Послуги",
                    "7 карток: Аудит · Бухгалтерія · Трансфертне · КІК · "
                    "Військовий облік · Юридичні · Кадровий",
                ],
                [
                    "Переваги",
                    "3 тези: Одна команда · Статус критичності · Супровід перевірок",
                ],
                ["Новини", "три останні статті"],
                ["Контакт", "телефон і електронна пошта"],
            ],
            [w * 0.28, w * 0.72],
        )
    )
    story += [
        Spacer(1, 3 * mm),
        p(
            "<b>Слоган:</b> «Супроводжуємо бізнес у звітності, перевірках і призначенні "
            "статусу критично важливого підприємства.»"
        ),
        PageBreak(),
        p("2. Про нас  /pro-nas/", H3),
    ]
    story.append(
        table(
            [
                ["Блок", "Що на сторінці"],
                ["Про компанію", "текст «Хто ми» з Правик 1"],
                ["Метрики", "19 / 500 / 25 / 50"],
                ["Команда", "8 осіб + фото (WebP у static)"],
                [
                    "Сертифікати",
                    "Реєстр №3975 + лінк; свідоцтво; ACCA. Адвокатське — пізніше",
                ],
                ["Кейси", "картки виконаних робіт"],
            ],
            [w * 0.28, w * 0.72],
        )
    )
    story += [
        p("3. Послуги  /poslugy/", H3),
        p("На сторінці напрямку: опис, склад списком, для кого, телефон."),
    ]
    story.append(
        table(
            [
                ["#", "Назва", "URL"],
                ["1", "Аудиторські послуги", "/poslugy/audytorski/"],
                ["2", "Бухгалтерські послуги", "/poslugy/buhgalterski/"],
                ["3", "Трансфертне ціноутворення", "/poslugy/transfertne-tsinoutvorennya/"],
                ["4", "КІК", "/poslugy/kik/"],
                ["5", "Військовий облік", "/poslugy/viyskovyy-oblik/"],
                ["6", "Юридичні послуги", "/poslugy/yurydychni/"],
                ["7", "Кадровий супровід", "/poslugy/kadrovyy-suprovid/"],
            ],
            [w * 0.08, w * 0.40, w * 0.52],
        )
    )
    story += [
        Spacer(1, 3 * mm),
        p(
            "<b>Військовий облік — склад:</b> статус критичного підприємства · ведення ВО · "
            "супровід перевірок ТЦК та СП · аудит ВО."
        ),
        p("4. Новини  /novyny/", H3),
        p("Стрічка статей, пагінація, «Поділитися» на статті."),
        p("5. Контакти  /kontakty/", H3),
        p("Адреса, телефони, email, карта. Поки плейсхолдери."),
        p("Службові", H3),
        p("Політика конфіденційності · 404 · sitemap.xml · robots.txt"),
        p("CMS", H2),
        p("SiteSettings · SiteBlock · Service (7) · News · Case · Team. Lead немає."),
    ]

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(OUT)


if __name__ == "__main__":
    build()
