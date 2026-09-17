from src.core.models import SiteSettings


def apply_page_meta(ctx: dict, page: str, page_obj=None) -> None:
    site = ctx.get("site") or SiteSettings.load()
    title = ""
    description = ""
    if page_obj is not None:
        title = (getattr(page_obj, "meta_title", "") or "").strip()
        description = (getattr(page_obj, "meta_description", "") or "").strip()
    if not title or not description:
        fallback_title, fallback_description = site.meta_for(page)
        title = title or fallback_title
        description = description or fallback_description
    ctx["meta_title"] = title
    ctx["meta_description"] = description
