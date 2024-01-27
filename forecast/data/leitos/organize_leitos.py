import pandas as pd

COLUMNS_TYPES = {
    "COMP": str,
    "REGIAO": str,
    "UF": str,
    "MUNICIPIO": str,
    "CNES": str,
    "DS_TIPO_UNIDADE": str,
    "DESC_NATUREZA_JURIDICA": str,
    "LEITOS_EXISTENTE": int,
    "LEITOS_SUS": int,
    "UTI_TOTAL_EXIST": int,
    "UTI_TOTAL_SUS": int,
    "UTI_ADULTO_EXIST": int,
    "UTI_ADULTO_SUS": int,
    "UTI_PEDIATRICO_EXIST": int,
    "UTI_PEDIATRICO_SUS": int,
    "UTI_NEONATAL_EXIST": int,
    "UTI_NEONATAL_SUS": int,
    "UTI_QUEIMADO_EXIST": int,
    "UTI_QUEIMADO_SUS": int,
    "UTI_CORONARIANA_EXIST": int,
    "UTI_CORONARIANA_SUS": int,
    "LEITOS_EXISTENTES": int,
}


def preprocess():
    df = pd.DataFrame()
    for y in [19, 20, 21, 22, 23]:
        y_df = pd.read_csv(
            f"data/leitos/Leitos_20{y}.csv",
            low_memory=False,
            encoding="ISO-8859-1",
        )

        y_df.columns = y_df.columns.str.replace(" - ", "_")
        y_df.columns = y_df.columns.str.replace(" ", "_")

        y_df["CNES"] = y_df["CNES"].astype(int).astype(str).str.zfill(7)

        df = pd.concat([df, y_df], ignore_index=True)

    print(df.columns.tolist())

    for column in df.columns:
        if column not in COLUMNS_TYPES.keys():
            df = df.drop(columns=[column])

    for column, t in COLUMNS_TYPES.items():
        if t == int:
            df[column] = df[column].fillna(0)
            df[column] = df[column].astype(t)

    df.to_csv("data/leitos/Leitos.csv", index=False)


def main():
    preprocess()

    df = pd.read_csv("data/leitos/Leitos.csv")
    print(df["DS_TIPO_UNIDADE"].unique())
    print(df["DESC_NATUREZA_JURIDICA"].unique())


if __name__ == "__main__":
    main()
