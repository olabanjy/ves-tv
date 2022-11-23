from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.defaults import page_not_found
from django.views.generic import View
from django.core.paginator import Paginator
from .models import *

import json
from django.http import JsonResponse
from users.decorators import allowed_users

# Create your views here.


def error404(request, exception):
    return page_not_found(request, exception, "errors/404.html")


def error500(request):
    return render(request, "errors/500.html")


class Homepage(View):
    def get(self, request):
        # check sub status
        featured = Content.objects.filter(featured=True, verified=True).first()
        featured2 = Content.objects.filter(featured=True, verified=True).last()

        popular = Content.objects.filter(verified=True).all().order_by("watch_times")

        paginator = Paginator(popular, 15)
        page = self.request.GET.get("page")
        contents = paginator.get_page(page)

        template = "core/index.html"

        context = {"featured": featured, "featured2": featured2, "contents": contents}

        return render(request, template, context)


@allowed_users
def content_detail(request, slug=None):

    the_content = get_object_or_404(Content, slug=slug)

    other_contents = Content.objects.filter(verified=True).exclude(
        slug=the_content.slug
    )

    template = "core/movie_detail.html"

    context = {"the_content": the_content, "other_contents": other_contents}

    return render(request, template, context)


@allowed_users
def show_detail(request, slug=None):
    # the_content = Content.object.get(slug=slug)

    the_content = get_object_or_404(Content, slug=slug)

    template = "core/show_details.html"

    context = {"the_content": the_content}

    return render(request, template, context)


def episode_detail(request, content_slug=None, episode_slug=None):
    # the_content = Content.object.get(slug=slug)
    the_content = get_object_or_404(Content, slug=content_slug)
    the_episode = get_object_or_404(Episode, slug=episode_slug)
    other_episodes = (
        Episode.objects.filter(parent=the_content).exclude(slug=the_episode.slug).all()
    )
    print(other_episodes)

    template = "core/episode_detail.html"

    context = {
        "the_content": the_content,
        "the_episode": the_episode,
        "other_episodes": other_episodes,
    }

    return render(request, template, context)


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


def getRequestInfo(request):

    theheaders = json.dumps(dict(request.headers))
    print(theheaders)
    print(type(theheaders))
    returnData = {"MSISDN": theheaders}
    # print(returnData)
    return JsonResponse(returnData)


def echoView(request):
    return HttpResponse("YES, VES TV IS LIVE !!")
