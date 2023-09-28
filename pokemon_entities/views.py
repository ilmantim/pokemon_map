import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils import timezone


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
    current_time = timezone.localtime(timezone.now())  # Get current local time in Moscow
    
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    
    for pokemon_entity in PokemonEntity.objects.filter(appeared_at__lte=current_time, disappeared_at__gte=current_time):
        
        if pokemon_entity.pokemon.image:
            image_url = request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        else:
            image_url = 'path/to/default/image.png'

        add_pokemon(
            folium_map, pokemon_entity.lat, 
            pokemon_entity.lon, image_url
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        if pokemon.image:
            image_url = request.build_absolute_uri(pokemon.image.url)
        else:
            image_url = 'path/to/default/image.png'

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': image_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    
    # Filter PokemonEntity instances related to the specific Pokemon
    pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon)
    
    for pokemon_entity in pokemon_entities:
        if pokemon_entity.pokemon and pokemon_entity.pokemon.image:
            image_url = request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        else:
            image_url = 'path/to/default/image.png'

        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon, image_url
        )
        
    # Create a dictionary with Pokemon details
    pokemon_details = {
        'pokemon_id': pokemon.id,
        'title_ru': pokemon.title,
        'img_url': request.build_absolute_uri(pokemon.image.url),
        'description': pokemon.description,
        'lat': pokemon_entity.lat,
        'lon': pokemon_entity.lon,
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_details,
    })
