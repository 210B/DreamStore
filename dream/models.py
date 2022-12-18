from django.db import models
import os

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/dream/tag/{self.slug}/'


class Theme(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/dream/theme/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Themes'


class CEO(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Distributor(models.Model):
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100, blank=True)
    contact = models.EmailField(max_length=50, blank=True)
    ceo = models.ForeignKey(CEO, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Producer(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/dream/producer/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Producers'


class Dream(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    product_image = models.ImageField(upload_to='dream/images/%Y/%m/%d', blank=True)

    price = models.IntegerField(default=0)

    distributor = models.ForeignKey(Distributor, null=True, on_delete=models.SET_NULL)
    producer = models.ForeignKey(Producer, null=True, blank=True, on_delete=models.SET_NULL)
    themes = models.ManyToManyField(Theme, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    soldOut = models.BooleanField(default=False)

    def __str__(self):
        return f'[{self.pk}]{self.name}::{self.producer}'

    def get_absolute_url(self):
        return f'/dream/{self.pk}/'
