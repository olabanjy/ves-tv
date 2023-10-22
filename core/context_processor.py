##########
from .models import ContentGenre


def fetch_msisdn(request):
    if "Msisdn" in request.headers:
        msisdn = request.headers["Msisdn"]
        return {"msisdn": msisdn}
    else:
        return {"msisdn": "Anonymous User"}


def fetch_genres(request):
    genre_list = ContentGenre.objects.all()
    # for genre in ContentGenre.objects.all():
    #     genre_list.append(genre.name)

    return {"genre_list": genre_list}
