from django.contrib import admin
from db_util.classes.model_utils import ModelUtils
from .models import Symbol, Tracker, TrackerSymbols


class SymbolAdmin(admin.ModelAdmin):
    model = Symbol
    ordering = tuple(['name'])
    search_fields = tuple(['symbol', 'name', 'industry', 'sector'])
    list_display = tuple(['name', 'symbol', 'industry', 'sector', 'irWebsite'])
    fields = ModelUtils.extract_model_fields(Symbol)


class TrackerAdmin(admin.ModelAdmin):
    model = Tracker
    ordering = tuple([])
    search_fields = tuple([])
    list_display = tuple([])
    fields = ModelUtils.extract_model_fields(Tracker)


class TrackerSymbolsAdmin(admin.ModelAdmin):
    model = TrackerSymbols
    ordering = tuple([])
    search_fields = tuple([])
    list_display = tuple([])
    fields = ModelUtils.extract_model_fields(TrackerSymbols)


admin.site.register(Symbol, SymbolAdmin)
admin.site.register(Tracker, TrackerAdmin)
admin.site.register(TrackerSymbols, TrackerSymbolsAdmin)

