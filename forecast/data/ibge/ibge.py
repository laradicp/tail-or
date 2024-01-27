import pandas as pd
from unidecode import unidecode


def main():
    estados = pd.read_csv("data/estados_ibge.csv")
    municipios = pd.read_csv("data/municipios_ibge.csv")
    municipios_clean = municipios.copy()

    municipios_clean["MUNICIPIO"] = municipios_clean["NOME"].apply(
        lambda x: unidecode((str(x).upper()))
    )

    municipios_clean.to_csv("data/municipios_ibge_clean.csv", index=False)


if __name__ == "__main__":
    main()
