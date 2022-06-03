from django.db import models
from pytils.translit import slugify

class City(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='Город',
                            unique=True)
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='Язык программирования',
                            unique=True)
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Language, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    company = models.CharField(max_length=255, verbose_name='Компания')
    description = models.TextField(verbose_name='Описания')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name='Язык программирования')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return self.title
