from django.db import models
import datetime  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Имя"
    )
    title_eng = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Имя на английском",
    )
    title_jpn = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Имя на японском",
    )
    image = models.ImageField(
        upload_to="pokemon",
        verbose_name="Изображение"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="evolutions",
        verbose_name="Из кого эволюционировал"
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name="Покемон"
    )

    appeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Время появления"
    )
    disappeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Время исчезновения"
    )

    level = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Уровень"
    )
    health = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Здоровье"
    )
    strength = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Сила"
    )
    defense = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Защита"
    )
    stamina = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Выносливость"
    )

    def __str__(self):
        return self.pokemon.title
