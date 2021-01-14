from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget


from .models import News
from .models import Confines
from .models import Event
from .models import Places
from .models import PlaceType
from .models import City
from .models import Tickets
from .models import EventTypes
from .models import TicketsCount
from .models import SoldTickets


class NewsResource(resources.ModelResource):
    class Meta:
        model = News


class NewsAdmin(ImportExportActionModelAdmin):
    resource_class = NewsResource
    list_display = ('Title', 'About', 'id')
admin.site.register(News, NewsAdmin)


@admin.register(Confines)
class ConfinesAdmin(admin.ModelAdmin):
    list_display = ('id', 'Name', 'About')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'Name', 'Date', 'Place_id', 'About', 'TypeId', 'ConfineId')
    list_filter = ('Place_id', 'TypeId', 'ConfineId', ('Date', DateRangeFilter))
    search_fields = ('Name', 'id')


@admin.register(Places)
class PlacesAdmin(admin.ModelAdmin):
    list_display = ('id', 'Name', 'About', 'Adress', 'TypeId', 'CityId')
    list_filter = ('CityId', 'TypeId')


@admin.register(PlaceType)
class PlaceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'Name')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'Name')


@admin.register(Tickets)
class TicketsAdmin(admin.ModelAdmin):
    list_display = ('id', 'Place', 'Price', 'TicketCat', 'EvId')
    list_filter = ('EvId', 'Price')
    search_fields = ('Price', 'EvId')


@admin.register(EventTypes)
class EventTypesAdmin(admin.ModelAdmin):
    list_display = ('id', 'Name')


@admin.register(TicketsCount)
class TicketsCountAdmin(admin.ModelAdmin):
    list_display = ('EvId', 'AllCount', 'SoldCount')


class SoldTicketsResource(resources.ModelResource):
    EvId = fields.Field(column_name="EvId", attribute="EvId", widget=ForeignKeyWidget(Event, "Name"))
    class Meta:
        model = SoldTickets


class SoldTicketsAdmin(ImportExportActionModelAdmin):
    resource_class = SoldTicketsResource
    list_display = ('TicketId', 'EvId', 'Name', 'Surname')
    search_fields = ('Name', 'Surname')
admin.site.register(SoldTickets, SoldTicketsAdmin)
