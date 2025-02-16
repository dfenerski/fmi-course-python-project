from inspect import getmembers
from common_util.singleton import Singleton
from db_models_shared.symbol import Symbol
from django.test import TestCase
from etl.etl_symbol_history import EtlSymbolHistory, SymbolHistoryEntry
from dashboard.models import Tracker
from dashboard.services.dashboard_base_service import DashboardBaseService
from db_util.classes.model_utils import ModelUtils


class SymbolTestCase(TestCase):
    def setUp(self):
        Symbol.objects.create(
            symbol="TESTSYM",
            name="TestStock",
            industry="TestIndustry",
            sector="TestSector",
            businessSummary="TestBusinessSummary",
            irWebsite="https://py-fmi.org/"
        )

    def test_symbol_exist(self):
        symbol = Symbol.objects.get(symbol="TESTSYM")
        self.assertTrue(symbol)


class DashboardBaseServiceTestCase(TestCase):
    def setUp(self):
        service = DashboardBaseService()
        service.get_symbol_graceful("MSFT")

    def test_symbol_is_imported(self):
        symbol = Symbol.objects.get(symbol="MSFT")
        self.assertTrue(symbol)


class SingletonTestCase(TestCase):
    def setUp(self):
        class BaseSingleton(metaclass=Singleton):
            pass

        class TestClass(BaseSingleton):
            pass
        self.cls = TestClass

    def test_singleton_works(self):
        self.assertIs(self.cls(), self.cls())


class EtfSymbolHistoryBaseTestCase(TestCase):
    def setUp(self):
        DashboardBaseService().get_symbol_graceful("TSM")
        EtlSymbolHistory().run_pipeline("TSM", period="1d")

    def test_historical_import_works(self):
        symbol_instance = Symbol.objects.get(symbol="TSM")
        self.assertTrue(SymbolHistoryEntry.objects.filter(symbol=symbol_instance.id).exists())


class EtfSymbolHistoryDuplicationTestCase(TestCase):
    def setUp(self):
        DashboardBaseService().get_symbol_graceful("TSM")
        EtlSymbolHistory().run_pipeline("TSM", period="1d")

    def test_historical_import_works(self):
        symbol_instance = Symbol.objects.get(symbol="TSM")
        initial_count = SymbolHistoryEntry.objects.filter(symbol=symbol_instance.id).count()
        EtlSymbolHistory().run_pipeline("TSM", period="1d")
        self.assertEqual(initial_count, SymbolHistoryEntry.objects.filter(symbol=symbol_instance.id).count())


class EtfSymbolHistoryDefaultTestCase(TestCase):
    def setUp(self):
        DashboardBaseService().get_symbol_graceful("TSM")
        EtlSymbolHistory().run_pipeline("TSM")

    def test_historical_import_works(self):
        symbol_instance = Symbol.objects.get(symbol="TSM")
        self.assertGreater(SymbolHistoryEntry.objects.filter(symbol=symbol_instance.id).count(), 60)


# class ModelUtilsTestCase(TestCase):
#     def test_field_extraction(self):
#         print(getmembers(Tracker))
#         self.assertEqual(
#             ModelUtils.extract_model_fields(Tracker),
#             ("name", "created_at", "modified_at", "user", "symbols", "is_selected")
#         )
