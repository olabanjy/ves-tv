from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from django.views.generic import View

from django.utils.text import slugify

from django.shortcuts import render, reverse, get_object_or_404, redirect
# Create your views here.

from users import choices as user_choices

from core.models import Content, WatchedContent, Likes, ContentGenre, ContentCategory
from datetime import datetime

from users.utils import clean_uuid_int

from core import choices as core_choices

from django.utils.dateparse import parse_duration








@login_required
def after_login(request):
    admin_profile = request.user.profile

    if admin_profile.role == user_choices.Roles.Vendor.value:
        return redirect("vendor:vendor-dashboard")
    elif admin_profile.role == user_choices.Roles.SuperAdmin.value or admin_profile.role == user_choices.Roles.SystemAdmin.value:
        return redirect("core:home")


@login_required
def vendor_dashboard(request):
    template = 'vendor/dashboard.html'

    today = datetime.now()

    my_contents_qs = Content.objects.filter(vendor=request.user.profile)

    top10contents = my_contents_qs.order_by("-watch_times")[:15]

    viewedContentThisMonth = WatchedContent.objects.filter(created_at__month=today.month, content__vendor=request.user.profile).order_by("-created_at")[:10]

    viewCount = WatchedContent.objects.filter(content__vendor=request.user.profile).count()
    print(viewCount)
    likeCount  = Likes.objects.filter(content__vendor=request.user.profile).count()

    genre_ids = []

    for cont  in my_contents_qs.order_by("-watch_times")[:50]:
        if cont.genre.id not in genre_ids:
            genre_ids.append(cont.genre.id)

    topGenres = ContentGenre.objects.filter(id__in=genre_ids)


    context = {
        "top10contents":top10contents,
        "viewedContentThisMonth":viewedContentThisMonth,
        "viewCount":viewCount,
        "likeCount":likeCount,
        "topGenres":topGenres
    }

    return render(request, template, context)


@login_required
def super_admin_dashboard(request):
    template = 'vendor/super-admin-dashboard.html'

    context = {}

    return render(request, template, context)


@login_required
def film_list(request):
    template = "vendor/film/list.html"

    film_cat = ContentCategory.objects.filter(slug__in=["movies", "short-videos"])
    my_films = Content.objects.filter(vendor=request.user.profile, category__in=film_cat )

    context ={
        "my_films":my_films
    }

    return render(request, template, context)

class CreateFilm(View):
    template = "vendor/film/add.html"


    def get(self, request, *args, **kwargs):

        genre_list = ContentGenre.objects.all()
        cat = ContentCategory.objects.filter(slug__in=["movies", "short-videos"])
        context = {
            "genre_list": genre_list,
            "cats": cat
        }
        return render(self.request, self.template, context)

    def post(self, request,  *args, **kwargs):
        video_title = request.POST.get("video_title")
        img_banner = request.FILES["img_banner"]
        img_poster_path = request.FILES["img_poster"]
        img_thumbnail = request.FILES["img_thumbnail"]
        img_detail_poster = request.FILES["img_detail_poster"]
        category = request.POST.get("category")
        genre = request.POST.get("genre")
        description = request.POST.get("description")
        video_language = request.POST.get("video_language")
        duration = request.POST.get("duration")
        video_trailer = request.FILES["video_trailer"]
        video_mp4 = request.FILES["video_mp4"]
        hiddentimedelta = request.POST.get("hiddentimedelta")


        today = datetime.now()

        if not hiddentimedelta:
            return redirect("vendor:vendor-add-film")

        content_slug = slugify(f"{video_title}{clean_uuid_int(4)}")

        the_genre = ContentGenre.objects.filter(name=genre).first()
        the_category = ContentCategory.objects.filter(name=category).first()

        new_content = Content.objects.create(
            slug = content_slug,
            title = video_title,
            category = the_category,
            genre = the_genre,
            description = description,
            language = video_language,
            img_banner = img_banner,
            img_poster = img_poster_path,

            img_detail_poster = img_detail_poster,

            img_thumbnail = img_thumbnail,
            trailer_mp4 = video_trailer,

            file_mp4 = video_mp4,
            upload_date = today.date(),
            timedelta = parse_duration(hiddentimedelta),
            status = core_choices.VerificationStatus.Uploading.value,
            vendor = self.request.user.profile
        )

        try:
            new_content.img_detail_banner = img_banner
            new_content.img_trailer = img_thumbnail
            new_content.trailer_webm = video_trailer
            new_content.file_webm = video_mp4
            new_content.save()
        except Exception:
            pass

        return redirect('vendor:vendor-film-list')




@login_required
def show_list(request):
    template = "vendor/show/list.html"

    context ={}

    return render(request, template, context)


class CreateShow(View):
    template = "vendor/show/add.html"


    def get(self, request, *args, **kwargs):
        context = {}
        return render(self.request, self.template, context)


