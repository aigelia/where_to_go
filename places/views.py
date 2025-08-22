from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from places.models import Place


def get_geojson():
    features = []
    for place in Place.objects.all():
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.lng, place.lat]
            },
            "properties": {
                "title": place.title,
                "placeId": f"place_{place.id}",
                "detailsUrl": reverse("place-detail", args=[place.id])
            }
        })

    return {
        "type": "FeatureCollection",
        "features": features
    }


def index(request):
    places_geojson = get_geojson()
    context = {
        "places_geojson": places_geojson,
    }
    return render(request, "index.html", context)


def get_place_data(request, place_id):
    place_obj = get_object_or_404(
        Place.objects.prefetch_related('images'),
        id=place_id
    )
    serialized_place = {
        "title": place_obj.title,
        "imgs": [img.image.url for img in place_obj.images.all()],
        "description_long": place_obj.short_description,
        "description_short": place_obj.long_description,
        "coordinates": {
            "lng": str(place_obj.lng),
            "lat": str(place_obj.lat)
        }
    }

    return JsonResponse(
        serialized_place,
        json_dumps_params={"ensure_ascii": False, "indent": 4},
        content_type="application/json; charset=utf-8"
    )
