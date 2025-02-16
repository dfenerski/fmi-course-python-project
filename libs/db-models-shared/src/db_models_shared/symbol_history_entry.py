
from django.db.models import (
    CASCADE,
    DateTimeField,
    FloatField,
    ForeignKey,
    Model
)
from db_models_shared.symbol import Symbol


class SymbolHistoryEntry(Model):
    symbol = ForeignKey(Symbol, on_delete=CASCADE)

    timestamp = DateTimeField()
    close_price = FloatField()
    volume = FloatField()

    class Meta:
        # https://stackoverflow.com/a/2881071/13163112
        unique_together = ('symbol', 'timestamp')
        # Tight coupling
        # https://stackoverflow.com/a/62772698/13163112
        app_label = 'dashboard'
        # https://docs.djangoproject.com/en/5.1/topics/db/models/#meta-options
        ordering = ["timestamp"]
