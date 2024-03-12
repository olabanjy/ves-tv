from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.defaults import page_not_found
from django.views.generic import View
from django.core.paginator import Paginator
from .models import *
from . import choices

import json
from django.http import JsonResponse
from users.decorators import allowed_users
from users.utils import fetch_active_user
from users.models import Profile, CampaignTracker
from users.choices import Roles as user_roles
from vendor.models import Channel
import string, random


# Create your views here.


def error404(request, exception):
    return page_not_found(request, exception, "errors/404.html")


def error500(request):
    return render(request, "errors/500.html")


class Homepage(View):
    def get(self, request):
        popular = (
            Content.objects.filter(
                verified=True, status=choices.VerificationStatus.Approved.value
            )
            .all()
            .order_by("watch_times")
        )

        paginator = Paginator(popular, 12)
        page = self.request.GET.get("page")
        contents = paginator.get_page(page)

        channels = Channel.objects.filter(verified=True)
        favorite_channel = channels.filter(admin_favorite=True)[:4]
        template = "core/index.html"

        context = {
            "contents": contents,
            "channels": channels,
            "favorite_channel": favorite_channel,
        }

        try:
            Visit.objects.create(request_body=json.dumps(dict(request.headers)))
        except Exception:
            pass

        return render(request, template, context)


@allowed_users
def channels(request):
    template = "core/channels.html"

    channels = Channel.objects.filter(verified=True)

    paginator = Paginator(channels, 12)
    page = request.GET.get("page")
    contents = paginator.get_page(page)

    context = {"channels": contents}

    return render(request, template, context)


@allowed_users
def channel_detail(request, channel_id):
    template = "core/channel_detail.html"

    the_channel = Channel.objects.filter(id=int(channel_id), verified=True).first()
    content_cat = ContentGenre.objects.all()

    channel_content = Content.objects.filter(
        channel=the_channel,
        verified=True,
        status=choices.VerificationStatus.Approved.value,
    )

    paginator = Paginator(channel_content, 12)
    page = request.GET.get("page")
    chan_contents = paginator.get_page(page)

    category_tab = request.GET.get("category", None)
    if category_tab:
        category = ContentCategory.objects.filter(name=category_tab).first()
        print(category)
        channel_content = channel_content.filter(category=category)

    context = {
        "the_channel": the_channel,
        "content_cat": content_cat,
        "channel_content": chan_contents,
    }

    return render(request, template, context)


@allowed_users
def vendor_home(request, vendor_code):
    template = "core/vendor_home.html"

    vendor_profile = Profile.objects.get(user_code=vendor_code)

    all_cats = ContentCategory.objects.all()

    vendor_qs = Content.objects.filter(vendor=vendor_profile)

    paginator = Paginator(vendor_qs, 12)
    page = request.GET.get("page")
    vendor_contents = paginator.get_page(page)

    vendor_channels = Channel.objects.filter(vendor=vendor_profile)

    context = {
        "vendor_qs": vendor_contents,
        "all_cats": all_cats,
        "vendor_code": vendor_code,
        "vendor_profile": vendor_profile,
        "vendor_channels": vendor_channels,
    }

    return render(request, template, context)


@allowed_users
def content_detail(request, slug=None):
    the_content = get_object_or_404(Content, slug=slug)

    other_contents = Content.objects.filter(
        verified=True, status=choices.VerificationStatus.Approved.value
    ).exclude(slug=the_content.slug)[:12]
    try:
        the_content.watch_times += 1
        the_content.save()

        # channel too
        if the_content.channel:
            the_content.channel.total_views += 1
            the_content.channel.save()

        active_user = fetch_active_user(request)
        if active_user:
            watched_content_qs = WatchedContent.objects.filter(
                user=active_user, content=the_content
            )
            if watched_content_qs.exists():
                watched_content = watched_content_qs.first()
                watched_content.count += 1
                watched_content.save()
            else:
                WatchedContent.objects.create(user=active_user, content=the_content)

    except Exception as e:
        print(e)
        pass

    template = "core/content_detail.html"

    context = {"the_content": the_content, "other_contents": other_contents}

    return render(request, template, context)


@allowed_users
def like_product(request):
    data = {}
    content_id = request.GET.get("content_id", None)

    try:
        the_content = Content.objects.get(pk=int(content_id))

        active_user = fetch_active_user(request)

        Likes.objects.get_or_create(msisdn=active_user, content=the_content)
        data.update({"status": True, "msg": "Content Liked!"})

    except KeyError:
        data.update({"status": False, "msg": "Error occured!"})

    except (
        ValueError,
        NameError,
        TypeError,
        ImportError,
        IndexError,
        AttributeError,
    ) as error:
        err_msg = str(error)
        data.update({"status": False, "msg": "Error occured!"})
        print(err_msg)

    return JsonResponse(data)


@allowed_users
def show_detail(request, slug=None):
    the_content = get_object_or_404(Content, slug=slug)
    try:
        the_content.watch_times += 1
        the_content.save()
        active_user = fetch_active_user(request)
        if active_user:
            watched_content_qs = WatchedContent.objects.filter(
                user=active_user, content=the_content
            )
            if watched_content_qs.exists():
                watched_content = watched_content_qs.first()
                watched_content.count += 1
                watched_content.save()
            else:
                WatchedContent.objects.create(user=active_user, content=the_content)
    except Exception as e:
        print(e)
        pass

    template = "core/show_details.html"

    context = {"the_content": the_content}

    return render(request, template, context)


@allowed_users
def episode_detail(request, content_slug=None, episode_slug=None):
    # the_content = Content.object.get(slug=slug)
    the_content = get_object_or_404(Content, slug=content_slug)
    the_episode = get_object_or_404(Episode, slug=episode_slug)
    other_episodes = (
        Episode.objects.filter(parent=the_content).exclude(slug=the_episode.slug).all()
    )
    try:
        the_content.watch_times += 1
        the_content.save()
        the_episode.watch_times += 1
        the_episode.save()

        active_user = fetch_active_user(request)
        if active_user:
            watched_content_qs = WatchedContent.objects.filter(
                user=active_user, content=the_content
            )
            if watched_content_qs.exists():
                watched_content = watched_content_qs.first()
                watched_content.count += 1
                watched_content.save()
            else:
                WatchedContent.objects.create(user=active_user, content=the_content)
    except Exception:
        pass

    template = "core/episode_detail.html"

    context = {
        "the_content": the_content,
        "the_episode": the_episode,
        "other_episodes": other_episodes,
    }

    return render(request, template, context)


def category(request, category_slug=None):
    the_category = ContentCategory.objects.filter(slug=category_slug).first()

    the_contents = Content.objects.filter(category=the_category, verified=True).all()

    paginator = Paginator(the_contents, 8)
    page = request.GET.get("page")
    contents = paginator.get_page(page)

    template = "core/category_content.html"

    context = {"contents": contents, "category": the_category.name}

    return render(request, template, context)


def genre(request, genre_slug=None):
    the_genre = ContentGenre.objects.filter(slug=genre_slug).first()

    the_contents = Content.objects.filter(genre=the_genre, verified=True).all()

    paginator = Paginator(the_contents, 8)
    page = request.GET.get("page")
    contents = paginator.get_page(page)

    template = "core/genre_content.html"

    context = {"contents": contents, "genre": the_genre.name}

    return render(request, template, context)


def getRequestInfo(request):
    theheaders = json.dumps(dict(request.headers))
    returnData = {"MSISDN": theheaders}
    return JsonResponse(returnData)


def echoView(request):
    return HttpResponse("YES, VES TV IS LIVE !!")


################


def awaiting_response(request):
    template = "core/awaiting_response.html"
    return render(request, template)


def onboarding(request):
    template = "core/subscribe_page.html"

    active_user = fetch_active_user(request)
    print(active_user)

    context = {"active_user": active_user}

    return render(request, template, context)


def inactive_account(request):
    template = "core/inactive_account.html"

    context = {}
    return render(request, template, context)


def vendor_landing_page(request):
    template = "core/vendor_landing.html"

    context = {}
    return render(request, template, context)


def campaign_url(request):
    partner = request.GET.get("partner", None)
    click_id = request.GET.get("clickid", None)
    print(partner, click_id)

    N = 7

    # using random.choices()
    # generating random strings
    res = "".join(random.choices(string.ascii_lowercase + string.digits, k=N))

    redirect_url = f"http://ng-app.com/CloudIntegrated/VESTV-24-No-23410220000022939-web?trxId={res}"

    if "Msisdn" in request.headers:
        msisdn = request.headers["Msisdn"]
        if msisdn.startswith("0") and len(msisdn) == 11:
            msisdn = msisdn.replace("0", "234", 1)

        # save the clickID and msisdn

        try:
            CampaignTracker.objects.filter(msisdn=msisdn).delete()
        except Exception as ex:
            print(ex)

        new_promo_hit = CampaignTracker.objects.create(msisdn=msisdn)
        if click_id:
            new_promo_hit.click_id = click_id
        if partner:
            new_promo_hit.partner = partner
        new_promo_hit.save()

    return redirect(redirect_url)
