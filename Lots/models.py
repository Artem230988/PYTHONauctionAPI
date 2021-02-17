from datetime import datetime
from django.utils.timezone import utc
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Lot(models.Model):

    title = models.CharField(max_length=50)
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='lots')
    owner = models.ForeignKey(User, verbose_name='Автор лота', on_delete=models.CASCADE, related_name='owner_lots', default=1)
    current_buyer = models.ForeignKey(User, verbose_name='Текущий покупатель', blank=True, on_delete=models.PROTECT, related_name='buyer_bets', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    closed_date = models.DateField(verbose_name='Дата закрытия лота', blank=True, null=True)
    starting_rate = models.IntegerField(verbose_name='Начальная ставка')
    current_rate = models.IntegerField(verbose_name='Текущая ставка', default=0, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lot_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_at', ]


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    lot = models.ForeignKey(Lot, related_name='photos', on_delete=models.CASCADE)
