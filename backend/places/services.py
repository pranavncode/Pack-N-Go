
import httpx
from django.core.cache import cache

BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"


def search_destinations(query: str):
    query = query.strip()
    cache_key = f"geocoding:v1:{query.lower()}"

    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        response = httpx.get(
            BASE_URL,
            params={
                "name": query,
                "count": 10,
                "language": "en",
                "format": "json",
            },
            timeout=10.0,
        )
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPError as exc:
        raise RuntimeError("Geocoding provider is unavailable.") from exc

    results = []
    for place in data.get("results", []):
        results.append({
            "name": place.get("name"),
            "country": place.get("country"),
            "region": place.get("admin1"),
            "latitude": place.get("latitude"),
            "longitude": place.get("longitude"),
            "timezone": place.get("timezone"),
        })

    cache.set(cache_key, results, timeout=3600)
    return results

import httpx
from django.core.cache import cache

BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"


def search_destinations(place: str, state: str):
    place = place.strip()
    state = state.strip()

    cache_key = f"geocoding:india:v1:{place.casefold()}:{state.casefold()}"
    cached = cache.get(cache_key)

    if cached is not None:
        return cached

    try:
        response = httpx.get(
            BASE_URL,
            params={
                "name": f"{place}, {state}",
                "count": 10,
                "language": "en",
                "format": "json",
                "countryCode": "IN",
            },
            timeout=10.0,
        )
        response.raise_for_status()
        data = response.json()

    except httpx.HTTPError as exc:
        raise RuntimeError(
            "Indian destination search is temporarily unavailable."
        ) from exc

    
    results = data.get("results", [])

    # Only accept results from India and the requested state.
    matches = [
        item for item in results
        if item.get("country_code") == "IN"
        and (item.get("admin1") or "").casefold() == state.casefold()
    ]

    # Prefer an exact place-name match.
    exact_matches = [
        item for item in matches
        if (item.get("name") or "").strip().casefold()
        == place.strip().casefold()
    ]

    selected = exact_matches if exact_matches else matches

    # Do not arbitrarily choose between multiple exact matches.
    if len(selected) > 1:
        return [
            {
                "name": item.get("name"),
                "state": item.get("admin1"),
                "country": "India",
                "latitude": item.get("latitude"),
                "longitude": item.get("longitude"),
                "timezone": item.get("timezone"),
            }
            for item in selected
        ]

    output = [
        {
            "name": item.get("name"),
            "state": item.get("admin1"),
            "country": "India",
            "latitude": item.get("latitude"),
            "longitude": item.get("longitude"),
            "timezone": item.get("timezone"),
        }
        for item in selected
    ]

    cache.set(cache_key, output, timeout=3600)
    return output

