from django.shortcuts import HttpResponse, render
from django.views import View

from apps.account.templatetags.user_mention import user_mention
from apps.forum.models import Category

from .templatetags.convert_markdown import convert_markdown


class FrontpageView(View):
    template_name = "core/frontpage.html"

    def get(self, request):
        categories = Category.objects.filter(threads__isnull=False).distinct()
        context = {"categories": categories}
        return render(request, self.template_name, context)


def convert_markdown_to_html(request):
    input_param = request.POST.get("name", default="text")
    text = request.POST.get(input_param)
    html = user_mention(convert_markdown(text))
    return HttpResponse(html)
