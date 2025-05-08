import pandas as pd
import requests
from bs4 import BeautifulSoup


class ProcessingScraper:
    def __init__(self):
        self.base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"
        self.years = None

    def get_year(self):
        response = requests.get(self.base_url + "?opcao=opt_03")
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

        for product in df["Cultivar"]:
            product_str = str(product).strip()

            if product_str.isupper() and product_str != "NAN":
                current_category = product_str

            categories.append(current_category)

        df["Categoria"] = categories
        return df

    def remove_categories(self, df):
        mask = df["Cultivar"].apply(
            lambda x: isinstance(x, str) and not x.strip().isupper()
        )
        return df[mask].reset_index(drop=True)

    def processing_table(self):
        dfs = []
        for year in self.years:
            for subop in range(1, 5):  # subopt_01 to subopt_04
                suboption = f"subopt_0{subop}"
                url = (
                    f"{self.base_url}?subopcao={suboption}"
                    f"&opcao=opt_03&ano={year}"
                )
                try:
                    df_year = pd.read_html(url)[3]
                    df_year["ano"] = year
                    df_year["subopcao"] = suboption
                    dfs.append(df_year)
                except Exception as e:
                    print(f"Error in {year}, suboption {suboption}: {e}")

        df_final = pd.concat(dfs, ignore_index=True)

        # Remove  columns 'Unnamed: 2' and / or 'Sem definiÃ§Ã£o' if required
        if "Unnamed: 2" or "Sem definiÃ§Ã£o" in df_final.columns:
            columns_to_remove = ["Unnamed: 2", "Sem definiÃ§Ã£o"]
            df_final = df_final.drop(
                columns=[
                    col for col in columns_to_remove if col in df_final.columns
                ]
            )

        # Calls the function Categorize
        df_final = self.categorize(df_final)

        return df_final

    def encode_latin1(self, df: pd.DataFrame) -> pd.DataFrame:
        def try_fix_encoding(x):
            if not isinstance(x, str):
                return x
            try:
                # change from latin1 to utf-8 if required
                return x.encode("latin1").decode("utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError):
                return x  # If fails, original is returned

        df["Cultivar"] = df["Cultivar"].astype(str).apply(try_fix_encoding)
        return df

    def replace_quantity(self, df):
        df["Quantidade (Kg)"] = df["Quantidade (Kg)"].replace("-", "0")
        return df["Quantidade (Kg)"]

    def column_to_numeric(self, df):
        df["Quantidade (Kg)"] = (
            df["Quantidade (Kg)"]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace("-", "", regex=False)
            .str.strip()
        )

        df["Quantidade (Kg)"] = pd.to_numeric(
            df["Quantidade (Kg)"], errors="coerce"
        )
        return df["Quantidade (Kg)"]

    def remove_nan(self, df):
        df = df.dropna(axis=0)
        return df

    def remove_total(self, df):
        df = df[df["Cultivar"] != "Total"]
        return df

    def suboptions_labeling(self, df):
        map = {
            "subopt_01": "Viníferas",
            "subopt_02": "Americanas e híbridas",
            "subopt_03": "Uvas de mesa",
            "subopt_04": "Sem classificação",
        }
        df["subopcao"] = df["subopcao"].map(map)
        return df

    def save_df(self, df):
        df.to_csv(
            r"vitivinicultura-api\data\tabela_processamento.csv", index=False
        )

    def exec(self):
        self.get_year()
        df = self.processing_table()
        df = self.encode_latin1(df)
        df["Quantidade (Kg)"] = self.replace_quantity(df)
        df["Quantidade (Kg)"] = self.column_to_numeric(df)
        df = self.categorize(df)
        df = self.remove_categories(df)
        df = self.remove_nan(df)
        df = self.remove_total(df)
        df = self.suboptions_labeling(df)
        self.save_df(df)
        return df


run = ProcessingScraper()
run.exec()
print("Processing executed.")
