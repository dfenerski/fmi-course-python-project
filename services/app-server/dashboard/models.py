from django.db.models import (
    BooleanField,
    JSONField,
    ForeignKey,
    ManyToManyField,
    CASCADE
)
from django.contrib.auth.models import User
from db_util.models.access_metadata import AccessMetadata
from db_util.models.named import Named
from db_models_shared.symbol import Symbol


class Tracker(Named, AccessMetadata):
    user = ForeignKey(User, on_delete=CASCADE)
    symbols = ManyToManyField(Symbol, through="TrackerSymbols")

    is_selected = BooleanField()

    class Meta(Named.Meta, AccessMetadata.Meta):
        pass


class TrackerSymbols(AccessMetadata):
    symbol = ForeignKey(Symbol, on_delete=CASCADE)
    tracker = ForeignKey(Tracker, on_delete=CASCADE)

    is_favorite = BooleanField()
    metadata = JSONField()

    # https://stackoverflow.com/a/2881071/13163112
    class Meta(AccessMetadata.Meta):
        unique_together = ('symbol', 'tracker')
