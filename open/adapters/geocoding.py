import httpx

async def geocode_city(city: str):
    url = 'https://geocoding-api.open-meteo.com/v1/search'
    params = {'name': city, 'count': 1, 'language': 'en', 'format': 'json'}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        if not data.get('results'):
            return None
        top = data['results'][0]
        return {
            'name': top.get('name'),
            'lat': top.get('latitude'),
            'lon': top.get('longitude'),
            'country': top.get('country'),
        }
