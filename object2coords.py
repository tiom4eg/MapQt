import requests


# searchObject goes from keyPressEvent
def Object2Coords(searchObject):
    request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={searchObject}&format=json"
    response = requests.get(request)
    if response:
        json_response = response.json()
        geoObjects = json_response["response"]["GeoObjectCollection"]["featureMember"]
        geoObject = geoObjects[0]["GeoObject"]
        geoObjectCoords = geoObject["Point"]["pos"]
        return geoObjectCoords
    else:
        print(f"Request failed.")
        print(f"Request: {request}")
        print(f"HTTP status code: {response.status_code} {response.reason}")
