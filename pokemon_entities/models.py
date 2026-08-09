from django.db import models
import datetime# noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True, upload_to="pokemon")

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)

    level = models.IntegerField(null=True, blank=True)
    health = models.IntegerField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    defense = models.IntegerField(null=True, blank=True)
    stamina = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.pokemon.title

    

