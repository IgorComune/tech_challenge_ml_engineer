from api.services.exportation_scraper import ExportationScraper
from api.services.importation_scraper import ImportationScraper
from api.services.production_scraper import ProductionScraper
from api.services.processing_scraper import ProcessingScraper
from api.services.trade_scraper import TradeScraper

scrapers_registry = {
    "exportation": ExportationScraper,
    "importation": ImportationScraper,
    "production": ProductionScraper,
    "processing": ProcessingScraper,
    "trade": TradeScraper,
}
