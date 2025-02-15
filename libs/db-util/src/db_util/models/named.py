from django.db.models import CharField, Model


class Named(Model):
    name = CharField(max_length=100)

    class Meta:
        abstract = True
