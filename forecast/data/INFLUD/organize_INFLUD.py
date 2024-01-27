import numpy as np
import pandas as pd
from tqdm.auto import tqdm

COLUMNS_TYPES = {
    "_id": str,
    "cnes": str,
    "ocupacaoSuspeitoCli": int,
    "ocupacaoSuspeitoUti": int,
    "ocupacaoConfirmadoCli": int,
    "ocupacaoConfirmadoUti": int,
    "ocupacaoCovidUti": int,
    "ocupacaoCovidCli": int,
    "ocupacaoHospitalarUti": int,
    "ocupacaoHospitalarCli": int,
    "saidaSuspeitaObitos": int,
    "saidaSuspeitaAltas": int,
    "saidaConfirmadaObitos": int,
    "saidaConfirmadaAltas": int,
    "origem": str,
    "_p_usuario": str,
    "estadoNotificacao": str,
    "municipioNotificacao": str,
    "estado": str,
    "municipio": str,
    "excluido": bool,
    "validado": bool,
}


def preprocess():
    df = pd.DataFrame()
    for year in tqdm([19, 20, 21, 22, 23]):
        y_df = pd.read_csv(
            f"data/INFLUD/INFLUD{year}.csv",
            sep=";",
            encoding="ISO-8859-1",
            low_memory=True,
        )
        print(y_df.columns.tolist())

        # y_df.columns = y_df.columns.str.replace(" - ", "_")
        # y_df.columns = y_df.columns.str.replace(" ", "_")

        # y_df["CNES"] = y_df["CNES"].astype(int).astype(str).str.zfill(7)

        # df = pd.concat([df, y_df], ignore_index=True)

    # for column in df.columns:
    #     if column not in COLUMNS_TYPES.keys():
    #         df = df.drop(columns=[column])

    # for column, t in COLUMNS_TYPES.items():
    #     if t == int:
    #         df[column] = df[column].fillna(0)
    #         df[column] = df[column].astype(t)

    # df.to_csv("data/INFLUD/INFLUD.csv", index=False)
    # print(df.info())


def main():
    preprocess()


if __name__ == "__main__":
    main()
