from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .mixins import TimeStampedMixin, UUIDMixin
from django.utils.translation import gettext_lazy as _


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class Filmwork(UUIDMixin, TimeStampedMixin):
    class FilmworkTypeChoices(models.TextChoices):
        MOVIE = 'movie', _('Movie')
        TV_SHOW = 'tv_show', _('TV Show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation date'), blank=True, null=True)
    rating = models.DecimalField(_('rating'), max_digits=3, decimal_places=1,
                                 validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], blank=True, null=True)
    type = models.CharField(_('type'), max_length=20, choices=FilmworkTypeChoices.choices)
    certificate = models.CharField(_('certificate'), max_length=512, blank=True, null=True)
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')

    def __str__(self):
        return self.title

    genres = models.ManyToManyField(Genre, through='GenreFilmwork')


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, verbose_name=_('Filmwork'))
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, verbose_name=_('Genre'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('Filmwork genre')
        verbose_name_plural = _('Filmwork genres')
        unique_together = (('film_work_id', 'genre_id'),)


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return self.full_name

    film_works = models.ManyToManyField(Filmwork, through='PersonFilmwork')


class PersonFilmwork(UUIDMixin):
    class Role(models.TextChoices):
        DIRECTOR = 'director', _('Director')
        WRITER = 'writer', _('Writer')
        ACTOR = 'actor', _('Actor')

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, verbose_name=_('Filmwork'))
    person = models.ForeignKey('Person', on_delete=models.CASCADE, verbose_name=_('Person'))
    role = models.CharField(_('role'), max_length=255, choices=Role.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('Filmwork person')
        verbose_name_plural = _('Filmwork persons')
        unique_together = (('film_work_id', 'person_id', 'role'),)
