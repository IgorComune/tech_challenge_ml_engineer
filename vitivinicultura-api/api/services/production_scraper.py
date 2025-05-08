import pandas as pd
import requests
from bs4 import BeautifulSoup


class ProductionScraper:
    def __init__(self):
        self.base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"
        self.years = None

    def get_year(self):
        response = requests.get(self.base_url + "?opcao=opt_02")
        soup = BeautifulSoup(response.content, "html.parser")
        select_years = soup.find("input", {"class": "text_pesq"})
        self.years = [
            year
            for year in range(
                int(select_years["min"]), int(select_years["max"]) + 1
            )
        ]

    def categorize(self, df: pd.DataFrame):
        current_category = None
        categories = []

        for product in df["Produto"]:
            product_str = str(product).strip()

            if product_str.isupper() and product_str != "NAN":
                current_category = product_str

            categories.append(current_category)

        df["Categoria"] = categories
        return df

    def remove_categories(self, df):
        mask = df["Produto"].apply(
            lambda x: isinstance(x, str) and not x.strip().isupper()
        )
        return df[mask].reset_index(drop=True)

    def production_table(self):
        dfs = []
        for year in self.years:
            url = f"{self.base_url}?ano={year}&opcao=opt_02"
            try:
                df_year = pd.read_html(url)[3]
                df_year["ano"] = year
                dfs.append(df_year)
            except Exception as e:
                print(f"Erro in {year}: {e}")

        df_final = pd.concat(dfs, ignore_index=True)

        #  Remove column 'Unnamed: 2' if necessary.
        if "Unnamed: 2" in df_final.columns:
            df_final = df_final.drop(columns="Unnamed: 2")

        # Calls the function Categorize
        df_final = self.categorize(df_final)

        return df_final

    def encode_latin1(self, df):
        df["Produto"] = (
            df["Produto"]
            .astype(str)
            .apply(
                lambda x: (
                    x.encode("latin1").decode("utf-8")
                    if isinstance(x, str)
                    else x
                )
            )
        )
        return df  # <- Entire DataFrame returned

    def replace_quantity(self, df):
        df["Quantidade (L.)"] = df["Quantidade (L.)"].replace("-", "0")
        return df["Quantidade (L.)"]

    def column_to_numeric(self, df):
        df["Quantidade (L.)"] = (
            df["Quantidade (L.)"]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace("-", "", regex=False)
            .str.strip()
        )

        df["Quantidade (L.)"] = pd.to_numeric(
            df["Quantidade (L.)"], errors="coerce"
        )
        return df["Quantidade (L.)"]

    def remove_nan(self, df):
        df = df.dropna(axis=0)
        return df

    def remove_total(self, df):
        df = df[df["Produto"] != "Total"]
        return df

    def save_df(self, df):
        df.to_csv(r"vitivinicultura-api\data\tabela_producao.csv", index=False)

    def exec(self):
        self.get_year()
        df = self.production_table()
        df = self.encode_latin1(df)
        df["Quantidade (L.)"] = self.replace_quantity(df)
        df["Quantidade (L.)"] = self.column_to_numeric(df)
        df = self.categorize(df)
        df = self.remove_categories(df)
        df = self.remove_nan(df)
        df = self.remove_total(df)
        self.save_df(df)
        return df


run = ProductionScraper()
run.exec()
print("Production executed.")
