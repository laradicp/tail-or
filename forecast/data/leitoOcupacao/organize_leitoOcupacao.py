import numpy as np
import pandas as pd

COLUMNS_TYPES = {
    "_id": str,
    "dataNotificacao": np.datetime64,
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
    "_created_at": np.datetime64,
    "_updated_at": np.datetime64,
}


def preprocess():
    df = pd.DataFrame()
    for y in [0, 1, 2]:
        y_df = pd.read_csv(
            f"data/leitoOcupacao/esus-vepi.LeitoOcupacao_202{y}.csv",
            low_memory=False,
            index_col="Unnamed: 0",
        )
        df = pd.concat([df, y_df])

    df["cnes"] = (
        df["cnes"]
        .astype(str)
        .map(lambda x: "".join([i for i in x if str(i).isdigit()]))
    )
    df["cnes"] = df["cnes"].str.zfill(7)

    for column in df.columns:
        if column not in COLUMNS_TYPES.keys():
            df = df.drop(columns=[column])

    for column, t in COLUMNS_TYPES.items():
        if t == int:
            df[column] = df[column].fillna(0)
            df[column] = df[column].astype(t)
        if t == np.datetime64:
            df[column] = pd.to_datetime(df[column])

    df.to_csv("data/leitoOcupacao/esus-vepi.LeitoOcupacao.csv")


def main():
    preprocess()


if __name__ == "__main__":
    main()
