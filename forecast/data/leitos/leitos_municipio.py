import pandas as pd

UF = "MG"

LEITOS = [
    "LEITOS EXISTENTE",
    "LEITOS SUS",
    "UTI TOTAL - EXIST",
    "UTI TOTAL - SUS",
    "UTI ADULTO - EXIST",
    "UTI ADULTO - SUS",
    "UTI PEDIATRICO - EXIST",
    "UTI PEDIATRICO - SUS",
    "UTI NEONATAL - EXIST",
    "UTI NEONATAL - SUS",
    "UTI QUEIMADO - EXIST",
    "UTI QUEIMADO - SUS",
    "UTI CORONARIANA - EXIST",
    "UTI CORONARIANA - SUS",
]

LEITOS_1 = [
    "LEITOS_EXISTENTES",
    "LEITOS_SUS",
    "UTI_TOTAL_EXIST",
    "UTI_TOTAL_SUS",
    "UTI_ADULTO_EXIST",
    "UTI_ADULTO_SUS",
    "UTI_PEDIATRICO_EXIST",
    "UTI_PEDIATRICO_SUS",
    "UTI_NEONATAL_EXIST",
    "UTI_NEONATAL_SUS",
    "UTI_QUEIMADO_EXIST",
    "UTI_QUEIMADO_SUS",
    "UTI_CORONARIANA_EXIST",
    "UTI_CORONARIANA_SUS",
]


def main():
    values_df = pd.DataFrame()
    for year in range(2019, 2024):
        df = pd.read_csv(
            f"data/leitos/Leitos_{year}.csv", low_memory=False, encoding="ISO-8859-1"
        )
        try:
            df = (
                df.loc[df["UF"] == UF, ["MUNICIPIO"] + LEITOS]
                .groupby("MUNICIPIO")
                .sum()
                .reset_index()
            )
        except:
            df = (
                df.loc[df["UF"] == UF, ["MUNICIPIO"] + LEITOS_1]
                .groupby("MUNICIPIO")
                .sum()
                .reset_index()
            )
        df["ANO"] = year

        df = df.reindex(columns=["ANO"] + df.columns.tolist()[:-1])

        df.columns = ["ANO", "MUNICIPIO"] + LEITOS_1

        values_df = pd.concat([values_df, df], ignore_index=True)

    values_df.to_csv(f"data/leitos/Leitos_municipio_{UF}.csv", index=False)


if __name__ == "__main__":
    main()
