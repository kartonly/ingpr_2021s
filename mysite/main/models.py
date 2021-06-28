from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class News(models.Model):
    id = models.AutoField(primary_key=True)
    Title = models.CharField('Название', max_length=50)
    About = models.TextField('Описание')

    def __str__(self):
        return self.Title

    class Meta:
        verbose_name= 'Новость'
        verbose_name_plural= 'Новости'


class Confines(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.TextField('Название')
    About = models.TextField('Описание')

    class Meta:
        verbose_name= 'Ограничение'
        verbose_name_plural= 'Ограничения'

    def __str__(self):
        return self.Name


class EventTypes(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.TextField('Тип мероприятия')

    class Meta:
        verbose_name= 'Тип мероприятия'
        verbose_name_plural= 'Типы мероприятий'

    def __str__(self):
        return self.Name


class PlaceType(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.TextField('Название типа площадки')

    class Meta:
        verbose_name= 'Тип площадки'
        verbose_name_plural= 'Типы площадок'

    def __str__(self):
        return self.Name


class City(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.TextField('Город')

    class Meta:
        verbose_name= 'Город'
        verbose_name_plural= 'Города'

    def __str__(self):
        return self.Name


class Places(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.TextField('Название места')
    About = models.TextField('Описание места')
    TypeId = models.ForeignKey(PlaceType, on_delete=models.CASCADE)
    Adress = models.TextField('Адрес проведения мероприятия')
    CityId = models.ForeignKey(City, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Площадка проведения мероприятия'
        verbose_name_plural = 'Площадки проведения мероприятий'

    def __str__(self):
        return self.Name


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.TextField('Название')
    Date = models.DateTimeField('Дата и время мероприятия')
    Place_id = models.ForeignKey(Places, on_delete=models.CASCADE)
    About = models.TextField('Описание мероприятия')
    TypeId = models.ForeignKey(EventTypes, on_delete=models.CASCADE)
    ConfineId = models.ForeignKey(Confines, on_delete=models.CASCADE)

    class Meta:
        verbose_name= 'Мероприятие'
        verbose_name_plural= 'Мероприятия'

    def __str__(self):
        return self.Name


class Tickets(models.Model):
     id = models.AutoField(primary_key=True)
     Place = models.TextField('Место в зале')
     Price = models.IntegerField('Цена')
     TicketCat = models.TextField('Категория билета')
     EvId = models.ForeignKey(Event, on_delete=models.CASCADE)

     class Meta:
        verbose_name= 'Билет'
        verbose_name_plural= 'Билеты'


class TicketsCount(models.Model):
    EvId = models.ForeignKey(Event, on_delete=models.CASCADE)
    AllCount = models.IntegerField('Общее количество билетов')
    SoldCount = models.IntegerField('Количество проданных билетов')

    class Meta:
        verbose_name= 'Кол-во билетов'
        verbose_name_plural= 'Кол-во билетов'


class SoldTickets(models.Model):
    TicketId = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    EvId = models.ForeignKey(Event, on_delete=models.CASCADE)
    Name = models.TextField('Имя покупателя')
    Surname = models.TextField('Фамилия покупателя')
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        verbose_name= 'Проданный билет'
        verbose_name_plural= 'Проданные билеты'










