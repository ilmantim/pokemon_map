from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='pokemons', null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.title}'
    

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

 