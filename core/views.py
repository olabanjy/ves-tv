from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.defaults import page_not_found
from django.views.generic import View
from django.core.paginator import Paginator
from .models import *
from users.models import Subscribtion

# Create your views here.


def error404(request, exception):
    return page_not_found(request, exception, "errors/404.html")


def error500(request):
    return render(request, "errors/500.html")


class Homepage(View):
    def get(self, request):
        # check sub status
        sub_qs = Subscribtion.objects.filter(user=request.user.profile, sub_active=True)
        if not sub_qs.exists():
            return redirect("users:inactive_account")

        featured = Content.objects.filter(featured=True, verified=True).first()
        popular = Content.objects.filter(verified=True).all().order_by("watch_times")

        paginator = Paginator(popular, 8)
        page = self.request.GET.get("page")
        contents = paginator.get_page(page)

        template = "core/index.html"

        context = {"featured": featured, "contents": contents}

        return render(request, template, context)


@login_required
def content_detail(request, slug=None):
    # the_content = Content.object.get(slug=slug)
    sub_qs = Subscribtion.objects.filter(user=request.user.profile, sub_active=True)
    if not sub_qs.exists():
        return redirect("users:inactive_account")
    the_content = get_object_or_404(Content, slug=slug)

    template = "core/content_detail.html"

    context = {"the_content": the_content}

    return render(request, template, context)


@login_required
def episode_detail(request, content_slug=None, episode_slug=None):
    # the_content = Content.object.get(slug=slug)
    the_content = get_object_or_404(Content, slug=content_slug)
    the_episode = get_object_or_404(Episode, slug=episode_slug)

    template = "core/episode_detail.html"

    context = {"the_content": the_content}

    return render(request, template, context)


@login_required
def category(request, category_slug=None):
    print(category_slug)
    the_category = ContentCategory.objects.filter(slug=category_slug).first()
    print(the_category)
    the_contents = Content.objects.filter(category=the_category, verified=True).all()

    paginator = Paginator(the_contents, 8)
    page = request.GET.get("page")
    contents = paginator.get_page(page)

    template = "core/category_content.html"

    context = {"the_contents": contents}

    return render(request, template, context)
