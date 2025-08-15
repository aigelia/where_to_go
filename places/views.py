from django.db.models.expressions import result
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

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
                "detailsUrl": "Заглушка"
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


def place(request, place_id):
    place_obj = get_object_or_404(Place, id=place_id)
    return HttpResponse(place_obj.title)
