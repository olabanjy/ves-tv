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

from .models import Contracts, BankAccount

from .utils import create_and_save_contract



@login_required
def after_login(request):
    admin_profile = request.user.profile

    if admin_profile.role == user_choices.Roles.Vendor.value:
        return redirect("vendor:vendor-dashboard")
    elif admin_profile.role == user_choices.Roles.SuperAdmin.value or admin_profile.role == user_choices.Roles.SystemAdmin.value:
        return redirect("core:home")


@login_required
def vendor_dashboard(request):

    if not request.user.profile.onboarded:
        return redirect('vendor:profile_settings')
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


@login_required
def profile_settings(request):
    template = 'vendor/profile-settings.html'

    vendor_profile = request.user.profile
    vendor_contract, created = Contracts.objects.get_or_create(vendor=vendor_profile)
    vendor_bank, created = BankAccount.objects.get_or_create(vendor=vendor_profile)
    context = {
        "user_profile":vendor_profile,
        "contract":vendor_contract,
        "vendor_bank":vendor_bank
    }

    return render(request, template, context)


@login_required
def complete_onboarding(request):
    try:
        if request.method == "POST":
            data = request.POST

            first_name = data.get("first_name", None)
            last_name = data.get("last_name", None)
            company_name = data.get("company_name", None)
            vendor_country = data.get("vendor_country", None)
            state = data.get("state", None)
            address = data.get("address", None)
            company_banner = data.get("company_banner", None)
            contact_phone = data.get("contact_phone", None)

            ###
            account_number = data.get("account_number", None)
            account_name = data.get("account_name", None)
            account_bank = data.get("account_bank", None)



            vendor_profile = request.user.profile
            vendor_profile.first_name = first_name
            vendor_profile.last_name = last_name
            vendor_profile.company_name = company_name
            vendor_profile.state = state
            vendor_profile.contact_phone = contact_phone
            vendor_profile.nationality = vendor_country


            if company_banner:
                vendor_profile.company_banner = company_banner

            if address:
                vendor_profile.address = address

            vendor_profile.save()

            # create account
            vendor_bank, created = BankAccount.objects.get_or_create(vendor=vendor_profile)
            vendor_bank.account_number = account_number
            vendor_bank.account_name = account_name
            vendor_bank.account_bank = account_bank
            vendor_bank.save()
            # create contract

            if  not vendor_profile.onboarded :
                vendor_contract, created = Contracts.objects.get_or_create(vendor=vendor_profile)
                contract_data = {
                        'first_name':vendor_profile.first_name,
                        'last_name':vendor_profile.last_name,
                        'today':datetime.astimezone(datetime.today()) ,
                        'address_1':vendor_profile.state,
                        'address_2':vendor_profile.address,
                        'city':vendor_profile.state,
                        'state':vendor_profile.nationality,
                        "account_number":vendor_bank.account_number,
                        "account_name":vendor_bank.account_name,
                        "account_bank":vendor_bank.account_bank,

                }
                contract_filename = f"VES_TV_AGREEMENT_{vendor_profile.user_code}.pdf"
                create_and_save_contract('contracts/vendor_contract.html',contract_filename, vendor_contract.pk, contract_data)
            vendor_profile.onboarded = True
            vendor_profile.save()

    except Exception as e:
        print(e)

    return redirect('vendor:profile_settings')



@login_required
def submit_contract(request):
    try:
        if request.method == "POST":
            data = request.FILES
            contract_file = data["contract_sumbit"]
            vendor_profile = request.user.profile
            vendor_contract  = Contracts.objects.get(vendor=vendor_profile)
            vendor_contract.contract_file = contract_file

            # vendor_contract.signed = True
            vendor_contract.save()
    except Exception as e:
        print(e)
    return redirect('vendor:profile_settings')


