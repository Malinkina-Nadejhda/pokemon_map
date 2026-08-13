import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    current_time = localtime()
    active_pokemons = PokemonEntity.objects.filter(
        appeared_at__lte=current_time,
        disappeared_at__gte=current_time,
    )

    for entity in active_pokemons:
        if entity.lat and entity.lon and entity.pokemon and entity.pokemon.image:
            img_url = request.build_absolute_uri(entity.pokemon.image.url)
            add_pokemon(
                folium_map,
                entity.lat,
                entity.lon,
                img_url
            )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        if pokemon.image:
            img_url = request.build_absolute_uri(pokemon.image.url)
        else:
            img_url = None
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for entity in requested_pokemon.pokemonentity_set.all():
        if entity.lat and entity.lon and requested_pokemon.image:
            img_url = request.build_absolute_uri(requested_pokemon.image.url)
            add_pokemon(
                folium_map,
                entity.lat,
                entity.lon,
                img_url
            )
    if requested_pokemon.previous_evolution:
        ancestor = requested_pokemon.previous_evolution
        ancestor_data = {
            "pokemon_id": ancestor.id,
            "title_ru": ancestor.title,
            "img_url": request.build_absolute_uri(ancestor.image.url),
        }
    else:
        ancestor_data = None
    pokemon_data = {
        "pokemon_id": requested_pokemon.id,
        "title_ru": requested_pokemon.title,
        "title_en": requested_pokemon.title_eng or "",
        "title_jpn": requested_pokemon.title_jpn or "",
        "img_url": request.build_absolute_uri(requested_pokemon.image.url),
        "description": requested_pokemon.description or "",
        "previous_evolution":ancestor_data,
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_data
    })
