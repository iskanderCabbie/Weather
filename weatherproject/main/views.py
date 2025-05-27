import requests
from django.shortcuts import render
from .models import CitySearch
from django.http import JsonResponse
from django.db.models import Count

def history_api(request):
    # Аггрегация: сколько раз вводили каждый город всеми пользователями
    data = (
        CitySearch.objects.values("name")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    return JsonResponse(list(data), safe=False)


def user_history_api(request):
    # История для текущей сессии (пользователя)
    session_key = request.session.session_key
    if not session_key:
        return JsonResponse([], safe=False)

    data = (
        CitySearch.objects.filter(session_key=session_key)
        .values("name")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    return JsonResponse(list(data), safe=False)

def weather_view(request):
    city = request.GET.get('city')
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    if not city or not latitude or not longitude:
        city = request.COOKIES.get('last_city_name')
        latitude = request.COOKIES.get('last_city_latitude')
        longitude = request.COOKIES.get('last_city_longitude')

    weather_data = None

    if city and latitude and longitude:
        try:
            response = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current_weather": True
                }
            )
            weather_data = response.json()

            # Получаем session_key пользователя
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            # Сохраняем поиск с привязкой к сессии
            CitySearch.objects.create(name=city, session_key=session_key)

        except Exception as e:
            print("Ошибка при получении погоды:", e)

    context = {
        "weather": weather_data,
        "last_city": city,
        "city": city,
    }

    response = render(request, "weather.html", context)

    if request.GET.get('city') and request.GET.get('latitude') and request.GET.get('longitude'):
        response.set_cookie("last_city_name", city, max_age=3600*24*7)
        response.set_cookie("last_city_latitude", latitude, max_age=3600*24*7)
        response.set_cookie("last_city_longitude", longitude, max_age=3600*24*7)

    return response