import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils import timezone
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
    current_time = timezone.localtime(timezone.now())  
    
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    
    for pokemon_entity in PokemonEntity.objects.filter(appeared_at__lte=current_time, disappeared_at__gte=current_time):
        
        image_url = get_pokemon_entity_image_url(pokemon_entity, request)

        add_pokemon(
            folium_map, pokemon_entity.lat, 
            pokemon_entity.lon, image_url
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        if pokemon.image:
            image_url = request.build_absolute_uri(pokemon.image.url)
        else:
            image_url = DEFAULT_IMAGE_URL

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': image_url,
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    
    pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon)
    
    for pokemon_entity in pokemon_entities:
        image_url = get_pokemon_entity_image_url(pokemon_entity, request)

        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon, image_url
        )
        
    pokemon_details = {
        'pokemon_id': pokemon.id,
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'img_url': request.build_absolute_uri(pokemon.image.url),
        'description': pokemon.description,

    }

    if pokemon.previous_evolution:
        evolution_data = {
            'title_ru': pokemon.previous_evolution.title_ru,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': request.build_absolute_uri(pokemon.previous_evolution.image.url),
        }
        pokemon_details['previous_evolution'] = evolution_data
    
    next_evolutions = pokemon.next_evolutions.first()
    
    if next_evolutions:
        evolution_data = {
            'title_ru': next_evolutions.title_ru,
            'pokemon_id': next_evolutions.id,
            'img_url': request.build_absolute_uri(next_evolutions.image.url),
        }
        pokemon_details['next_evolution'] = evolution_data

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_details,
    })


def get_pokemon_entity_image_url(pokemon_entity, request):
    if pokemon_entity.pokemon.image:
        image_url = request.build_absolute_uri(pokemon_entity.pokemon.image.url)
    else:
        image_url = DEFAULT_IMAGE_URL
    return image_url


