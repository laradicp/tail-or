from itertools import product

import numpy as np
import pandas as pd
from tqdm import tqdm

# TODO Focar nos CNES do DF
# TODO Alterar periodo de tempo para semana ou mes (primeiro mes)


IDENT = [
    "CS_SEXO",
    "DT_NASC",
    "CS_GESTANT",
    "CS_RACA",
    "CS_ESCOL_N",
]

MORB = [
    "SURTO_SG",
    "NOSOCOMIAL",
    "AVE_SUINO",
    "FEBRE",
    "TOSSE",
    "GARGANTA",
    "DISPNEIA",
    "DESC_RESP",
    "SATURACAO",
    "DIARREIA",
    "VOMITO",
    "OUTRO_SIN",
    "PUERPERA",
    "CARDIOPATI",
    "HEMATOLOGI",
    "SIND_DOWN",
    "HEPATICA",
    "ASMA",
    "DIABETES",
    "NEUROLOGIC",
    "PNEUMOPATI",
    "IMUNODEPRE",
    "RENAL",
    "OBESIDADE",
    "OUT_MORBI",
    "SUPORT_VEN",
]

EXTRA = [
    "SURTO_SG",
    "NOSOCOMIAL",
    "AVE_SUINO",
    "FEBRE",
    "TOSSE",
    "GARGANTA",
    "DISPNEIA",
    "DESC_RESP",
    "SATURACAO",
    "DIARREIA",
    "VOMITO",
    "OUTRO_SIN",
    "PUERPERA",
    "CARDIOPATI",
    "HEMATOLOGI",
    "SIND_DOWN",
    "HEPATICA",
    "ASMA",
    "DIABETES",
    "NEUROLOGIC",
    "PNEUMOPATI",
    "IMUNODEPRE",
    "RENAL",
    "OBESIDADE",
    "OUT_MORBI",
    "SUP_VEN_INV",
    "SUP_VEN_NINV",
]

DATAS = [
    "CO_UNI_NOT",
    "DT_INTERNA",
    "DT_EVOLUCA",
    "HOSPITAL",
    "DT_ENTUTI",
    "DT_SAIDUTI",
    "UTI",
]


def valid_date(x):
    if "/" not in str(x):
        return np.datetime64("2024-01")

    day, month, year = str(x).split("/")

    if int(year) >= 2024:
        return np.datetime64("2024-01")

    return np.datetime64(f"{year}-{month}")  # -{day}")


def valid_label(x):
    if pd.isnull(x):
        return False
    return int(x) == 1


def preprocess():
    data = pd.DataFrame()

    for y in tqdm(range(19, 24)):
        df = pd.read_csv(
            f"data/INFLUD/INFLUD{y}.csv",
            sep=";",
            encoding="ISO-8859-1",
            low_memory=False,
        )

        df["CO_UNI_NOT"] = df["CO_UNI_NOT"].astype(str).str.zfill(7)

        df["DT_INTERNA"] = df["DT_INTERNA"].apply(lambda x: valid_date(x))
        df["DT_EVOLUCA"] = df["DT_EVOLUCA"].apply(lambda x: valid_date(x))
        df["DT_ENTUTI"] = df["DT_ENTUTI"].apply(lambda x: valid_date(x))
        df["DT_SAIDUTI"] = df["DT_SAIDUTI"].apply(lambda x: valid_date(x))

        df["SUP_VEN_INV"] = df["SUPORT_VEN"] == 1
        df["SUP_VEN_NINV"] = df["SUPORT_VEN"] == 2
        df["SUPORT_VEN"] = (df["SUPORT_VEN"] == 1) & (df["SUPORT_VEN"] == 2)

        df["HOSPITAL"] = df["HOSPITAL"] == 1
        df["UTI"] = df["UTI"] == 1

        for column in MORB:
            df[column] = df[column].apply(lambda x: valid_label(x))

        hospital = (
            df.loc[df["SG_UF"] == "DF", DATAS + EXTRA]
            .groupby(
                ["CO_UNI_NOT", "DT_INTERNA", "DT_EVOLUCA", "DT_ENTUTI", "DT_SAIDUTI"]
            )
            .sum()
            .sort_values("DT_INTERNA")
            .reset_index()
        )

        data = pd.concat([data, hospital], ignore_index=True)

    data.to_csv(f"data/timeseries/data_mensal.csv", index=False)


def final():
    data = pd.read_csv(f"data/timeseries/data_mensal.csv")

    data["DT_INTERNA"] = pd.to_datetime(data["DT_INTERNA"])
    data["DT_EVOLUCA"] = pd.to_datetime(data["DT_EVOLUCA"])
    data["DT_ENTUTI"] = pd.to_datetime(data["DT_ENTUTI"])
    data["DT_SAIDUTI"] = pd.to_datetime(data["DT_SAIDUTI"])

    all_cnes = data["CO_UNI_NOT"].unique().tolist()
    all_dates = (
        pd.concat(
            [
                data["DT_INTERNA"],
                data["DT_EVOLUCA"],
                data["DT_ENTUTI"],
                data["DT_SAIDUTI"],
            ]
        )
        .unique()
        .tolist()
    )

    tuples = list(product(all_dates, all_cnes))

    df = pd.DataFrame(tuples, columns=["DT", "CNES"])
    df = df.sort_values(by="DT")

    df["HOSPITAL"] = 0
    df["UTI"] = 0

    for column in EXTRA:
        df[column] = 0

    for cnes in tqdm(all_cnes):
        subset = data.loc[
            data["CO_UNI_NOT"] == cnes,
            ["DT_INTERNA", "DT_EVOLUCA", "HOSPITAL", "DT_ENTUTI", "DT_SAIDUTI", "UTI"]
            + EXTRA,
        ]

        for idx in subset.index:
            value = subset.loc[idx, ["HOSPITAL"] + EXTRA]

            df.loc[
                (df["CNES"] == cnes)
                & (df["DT"] >= subset.loc[idx, "DT_INTERNA"])
                & (df["DT"] <= subset.loc[idx, "DT_EVOLUCA"]),
                ["HOSPITAL"] + EXTRA,
            ] += value

            value = subset.loc[idx, "UTI"]

            df.loc[
                (df["CNES"] == cnes)
                & (df["DT"] >= subset.loc[idx, "DT_ENTUTI"])
                & (df["DT"] <= subset.loc[idx, "DT_SAIDUTI"])
                & (df["DT"] <= subset.loc[idx, "DT_EVOLUCA"]),
                ["UTI"],
            ] += value

    df["CNES"] = df["CNES"].astype(str).str.zfill(7)

    df = df.sort_values(["CNES", "DT"]).reset_index(drop=True)

    df.to_csv("data/timeseries/timeseries_mensal.csv")


if __name__ == "__main__":
    preprocess()
    final()
