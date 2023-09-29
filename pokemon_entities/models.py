from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True) 
    title_jp = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='pokemons', null=True, blank=True)
    description = models.TextField()
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='evolutions', default=None)
    
    

    def __str__(self):
        return f'{self.title_ru}'
    

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, null=True, blank=True)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField()  # DateTimeField for appearance time
    disappeared_at = models.DateTimeField() 
    health = models.IntegerField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    defence = models.IntegerField(null=True, blank=True)
    stamina = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.pokemon}'

 