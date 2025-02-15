from django.db.models import CharField, TextField
from db_util.models.access_metadata import AccessMetadata
from db_util.models.named import Named


class Symbol(Named, AccessMetadata):
    symbol = CharField(max_length=10, unique=True)
    industry = CharField(max_length=100)
    sector = CharField(max_length=100)
    businessSummary = TextField()
    irWebsite = CharField(max_length=100, null=True)

    class Meta(Named.Meta, AccessMetadata.Meta):
        # Tight coupling
        # https://stackoverflow.com/a/62772698/13163112
        app_label = 'dashboard'
