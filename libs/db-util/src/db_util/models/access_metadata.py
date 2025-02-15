from django.db.models import DateTimeField, Model
from django.utils.timezone import now


class AccessMetadata(Model):
    created_at = DateTimeField(default=now)
    modified_at = DateTimeField(default=now)

    class Meta:
        abstract = True
