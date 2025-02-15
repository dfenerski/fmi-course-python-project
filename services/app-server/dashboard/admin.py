from django.contrib import admin
from db_util.classes.model_utils import ModelUtils
from .models import Symbol, Tracker, TrackerSymbols


class SymbolAdmin(admin.ModelAdmin):
    model = Symbol
    ordering = tuple(['name', 'created_at'])
    search_fields = tuple(['symbol', 'name', 'created_at', 'industry', 'sector'])
    list_display = tuple(['name', 'symbol', 'industry', 'sector', 'irWebsite', 'created_at'])
    fields = ModelUtils.extract_model_fields(Symbol)


class TrackerAdmin(admin.ModelAdmin):
    model = Tracker
    ordering = tuple(['user'])
    search_fields = tuple(['user', 'is_selected'])
    list_display = tuple(['user', 'is_selected'])
    fields = ModelUtils.extract_model_fields(Tracker)


class TrackerSymbolsAdmin(admin.ModelAdmin):
    model = TrackerSymbols
    ordering = tuple(['tracker', 'symbol'])
    search_fields = tuple(['tracker', 'symbol'])
    list_display = tuple(['tracker', 'symbol', 'is_favorite', 'metadata'])
    fields = ModelUtils.extract_model_fields(TrackerSymbols)


admin.site.register(Symbol, SymbolAdmin)
admin.site.register(Tracker, TrackerAdmin)
admin.site.register(TrackerSymbols, TrackerSymbolsAdmin)

