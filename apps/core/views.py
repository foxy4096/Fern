from django.shortcuts import HttpResponse, render
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Q

from apps.account.templatetags.user_mention import user_mention
from apps.forum.models import Category, Thread, Post
from apps.account.models import User

from .templatetags.convert_markdown import convert_markdown
from .utils import paginate, is_htmx


class FrontpageView(View):
    template_name = "core/frontpage.html"

    def get(self, request):
        categories = Category.objects.filter(parent__isnull=True).prefetch_related(
            "subcategories", "threads"
        )
        context = {"categories": categories}
        return render(request, self.template_name, context)


def convert_markdown_to_html(request):
    input_param = request.POST.get("name", default="text")
    text = request.POST.get(input_param)
    html = user_mention(convert_markdown(text))
    return HttpResponse(html)


class HomeView(TemplateView):
    template_name = "core/home.html"


def search(request):
    query = request.GET.get("q", "")
    type_filter = request.GET.get("type", "threads")
    results = []
    if query and type_filter:
        if type_filter == "threads":
            results = (
                Thread.objects.filter(
                    Q(title__icontains=query)
                    | Q(created_at__icontains=query)
                    | Q(creator__username__icontains=query)
                )
                .select_related("category")
                .prefetch_related("posts")
                .order_by("-created_at")
            )
        elif type_filter == "posts":
            results = (
                Post.objects.filter(
                    Q(thread__title__icontains=query) | Q(body__icontains=query)
                )
                .select_related("thread", "thread__category")
                .order_by("-created_at")
            )
        elif type_filter == "users":
            results = (
                User.objects.filter(username__icontains=query)
                .select_related("userprofile")
                .prefetch_related("posts")
                .order_by("-date_joined")
            )
        elif type_filter == "categories":
            results = (
                Category.objects.filter(name__icontains=query)
                .prefetch_related("threads")
                .order_by("name")
            )
    results = paginate(request, results, 10)
    context = {"query": query, "type_filter": type_filter, "results": results}
    if is_htmx(request):
        return render(request, "core/islands/search_results.html", context)
    else:
        return render(request, "core/search.html", context)

