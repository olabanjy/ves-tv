from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from datetime import datetime

from core.models import Content, WatchedContent, Likes, Visit
from users.models import UserSubscribtion, UserProfile, Profile
from users import choices as ums_choices
from vendor.models import Channel, Contracts

from django.shortcuts import get_object_or_404


from django.shortcuts import render, redirect

# Create your views here.


@login_required
def super_admin_dashboard(request):
    template = "vendor/admin/super_admin_dashboard.html"

    today = datetime.now()

    my_contents_qs = Content.objects.all()

    top10contents = my_contents_qs.order_by("-watch_times")[:15]

    activeSubscribtion = UserSubscribtion.objects.filter(sub_active=True).count()

    allUsers = UserProfile.objects.count()

    viewedContentThisMonth = WatchedContent.objects.filter(
        created_at__month=today.month
    ).order_by("-created_at")[:10]

    viewCount = WatchedContent.objects.all().count()

    likeCount = Likes.objects.filter(content__vendor=request.user.profile).count()

    visits = Visit.objects.count()

    topChannel = Channel.objects.all().order_by("-total_views")[:20]

    context = {
        "viewedContentThisMonth": viewedContentThisMonth,
        "likeCount": likeCount,
        "viewCount": viewCount,
        "top10contents": top10contents,
        "activeSubscribtion": activeSubscribtion,
        "allUsers": allUsers,
        "visits": visits,
        "topChannel": topChannel,
    }

    return render(request, template, context)


@login_required
def user_list(request):
    template = "vendor/admin/users.html"

    allUsers = UserProfile.objects.all()

    context = {
        "allUsers": allUsers,
    }

    return render(request, template, context)


@login_required
def user_subs(request):
    template = "vendor/admin/user_subscribtion.html"

    allSub = UserSubscribtion.objects.all()

    context = {
        "allSub": allSub,
    }

    return render(request, template, context)


@login_required
def all_contents(request):
    template = "vendor/admin/content_list.html"

    all_contents = Content.objects.all()

    context = {
        "all_contents": all_contents,
    }

    return render(request, template, context)


@login_required
def all_vendors(request):
    template = "vendor/admin/vendors.html"

    all_vendors = Profile.objects.filter(role=ums_choices.Roles.Vendor.value).all()

    context = {
        "all_vendors": all_vendors,
    }

    return render(request, template, context)


@login_required
def approve_content(request, id):
    try:
        the_content = get_object_or_404(Content, pk=id)
        the_content.verified = True
        the_content.save()
    except Exception as ex:
        print(ex)

    return redirect("vendor:content-list")


@login_required
def approve_vendor(request, id):
    try:
        the_vendor = get_object_or_404(Profile, pk=id)
        the_vendor.verified = True
        the_vendor.onboarded = True
        the_vendor.save()

        the_vendor.vendor_contracts.signed = True
        the_vendor.vendor_contracts.save()

    except Exception as ex:
        print(ex)

    return redirect("vendor:vendor-list")
