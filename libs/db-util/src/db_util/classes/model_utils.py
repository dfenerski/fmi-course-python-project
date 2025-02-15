from inspect import getmembers
from django.db.models import Field


class ModelUtils:
    @staticmethod
    def extract_model_fields(model_cls):
        return tuple((prop for (prop, _) in getmembers(model_cls, lambda v: isinstance(v, Field))))
