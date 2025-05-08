import pandas as pd
import requests
from bs4 import BeautifulSoup


class ImportationScraper:
    def __init__(self):
        self.base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"
        self.years = None

    def get_year(self):
        response = requests.get(self.base_url + "?opcao=opt_05")
        soup = BeautifulSoup(response.content, "html.parser")
        select_years = soup.find("input", {"class": "text_pesq"})
        self.years = [
            year
            for year in range(
                int(select_years["min"]), int(select_years["max"]) + 1
            )
        ]

    def remove_categories(self, df):
        mask = df["Países"].apply(
            lambda x: isinstance(x, str) and not x.strip().isupper()
        )
        return df[mask].reset_index(drop=True)

    def importation_table(self):
        dfs = []
        for year in self.years:
            for subop in range(1, 6):
                suboption = f"subopt_0{subop}"
                url = (
                    f"{self.base_url}?subopcao={suboption}"
                    f"&opcao=opt_05&ano={year}"
                )
                try:
                    df_year = pd.read_html(url)[3]
                    df_year["ano"] = year
                    df_year["subopcao"] = suboption
                    dfs.append(df_year)
                except Exception as e:
                    print(f"Error in {year}, suboption {subop}: {e}")

        df_final = pd.concat(dfs, ignore_index=True)

        # Remove  columns 'Unnamed: 2' and / or 'Sem definiÃ§Ã£o' if required
        if "Unnamed: 2" or "Sem definiÃ§Ã£o" in df_final.columns:
            columns_to_remove = ["Unnamed: 2", "Sem definiÃ§Ã£o"]
            df_final = df_final.drop(
                columns=[
                    col for col in columns_to_remove if col in df_final.columns
                ]
            )

        df_final = df_final.rename(columns={"PaÃ­ses": "Países"})
        return df_final

    def encode_latin1(self, df: pd.DataFrame) -> pd.DataFrame:
        def try_fix_encoding(x):
            if not isinstance(x, str):
                return x
            try:
                return x.encode("latin1").decode("utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError):
                return x  # If fails, original is returned

        df["Países"] = df["Países"].astype(str).apply(try_fix_encoding)
        return df

    def replace_quantity(self, df):
        df["Quantidade (Kg)"] = df["Quantidade (Kg)"].replace("-", "0")
        df["Valor (US$)"] = df["Valor (US$)"].replace("-", "0")
        return df["Quantidade (Kg)"], df["Valor (US$)"]

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

        df["Valor (US$)"] = (
            df["Valor (US$)"]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace("-", "", regex=False)
            .str.strip()
        )
        df["Valor (US$)"] = pd.to_numeric(df["Valor (US$)"], errors="coerce")
        return df["Quantidade (Kg)"], df["Valor (US$)"]

    def remove_nan(self, df):
        df = df.dropna(axis=0)
        return df

    def remove_total(self, df):
        df = df[df["Países"] != "Total"]
        return df

    def suboptions_labeling(self, df):
        map = {
            "subopt_01": "Vinhos de mesa",
            "subopt_02": "Espumantes",
            "subopt_03": "Uvas frescas",
            "subopt_04": "Uvas passas",
            "subopt_05": "Suco de uva",
        }
        df["subopcao"] = df["subopcao"].map(map)
        return df

    def save_df(self, df):
        df.to_csv(
            r"vitivinicultura-api\data\tabela_importacao.csv", index=False
        )

    def exec(self):
        self.get_year()
        df = self.importation_table()
        df = self.encode_latin1(df)
        df["Quantidade (Kg)"], df["Valor (US$)"] = self.replace_quantity(df)
        df["Quantidade (Kg)"], df["Valor (US$)"] = self.column_to_numeric(df)
        df = self.remove_categories(df)
        df = self.remove_nan(df)
        df = self.remove_total(df)
        df = self.suboptions_labeling(df)
        self.save_df(df)
        return df


run = ImportationScraper()
run.exec()
print("Importation executed.")
