from django.views.generic import DetailView, ListView

from src.news.models import News


class NewsListView(ListView):
    model = News
    template_name = "news/list.html"
    context_object_name = "articles"
    paginate_by = 9

    def get_queryset(self):
        return News.objects.filter(is_published=True)

    def get(self, request, *args, **kwargs):
        request.current_nav = "news"
        return super().get(request, *args, **kwargs)


class NewsDetailView(DetailView):
    model = News
    template_name = "news/detail.html"
    context_object_name = "article"
    slug_field = "slug"

    def get_queryset(self):
        return News.objects.filter(is_published=True)

    def get(self, request, *args, **kwargs):
        request.current_nav = "news"
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["related_news"] = (
            News.objects.filter(is_published=True)
            .exclude(pk=self.object.pk)
            .order_by("-published_at")[:3]
        )
        return ctx
