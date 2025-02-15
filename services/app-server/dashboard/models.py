from django.db.models import (
    BooleanField,
    CharField,
    JSONField,
    TextField,
    ForeignKey,
    ManyToManyField,
    CASCADE
)
from django.contrib.auth.models import User
from db_util.models.access_metadata import AccessMetadata
from db_util.models.named import Named


class Symbol(Named, AccessMetadata):
    symbol = CharField(max_length=10)
    industry = CharField(max_length=100)
    sector = CharField(max_length=100)
    businessSummary = TextField()
    irWebsite = CharField(max_length=100)

    class Meta(Named.Meta, AccessMetadata.Meta):
        pass


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
