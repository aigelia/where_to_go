from django.db.models.expressions import result
from django.shortcuts import render

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
