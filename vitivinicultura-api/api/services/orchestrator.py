import pandas as pd

from processing_scraper import ProcessingScraper
from trade_scraper import TradeScraper
from production_scraper import ProductionScraper
from importation_scraper import ImportationScraper
from exportation_scraper import ExportationScraper


class Orchestrator:
    def exec_processing(self):
        try:
            df_processing = ProcessingScraper().exec()
            return df_processing
        except Exception:
            df_processing = pd.read_csv(
                r"vitivinicultura-api\data\processamento.csv"
            )
            return df_processing

    def exec_trade(self):
        try:
            df_trade = TradeScraper().exec()
            return df_trade
        except Exception:
            df_trade = pd.read_csv(
                r"vitivinicultura-api\data\tabela_comercio.csv"
            )
            return df_trade

    def exec_production(self):
        try:
            df_production = ProductionScraper().exec()
            return df_production
        except Exception:
            df_production = pd.read_csv(
                r"vitivinicultura-api\data\tabela_producao.csv"
            )
            return df_production

    def exec_importation(self):
        try:
            df_importation = ImportationScraper().exec()
            return df_importation
        except Exception:
            df_importation = pd.read_csv(
                r"vitivinicultura-api\data\tabela_importacao.csv"
            )
            return df_importation

    def exec_exportation(self):
        try:
            df_exportation = ExportationScraper().exec()
            return df_exportation
        except Exception:
            df_exportation = pd.read_csv(
                r"vitivinicultura-api\data\tabela_exportacao.csv"
            )
            return df_exportation

    def exec(self):
        self.exec_processing()
        self.exec_trade()
        self.exec_production()
        self.exec_importation()
        self.exec_exportation()
