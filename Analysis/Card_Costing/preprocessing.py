import numpy as np
import pandas as pd
import sys

from Conn import conn_mtg
from Utilities.tokenize_cardtext import tokenize


def to_int(text):
    try:
        return int(text)
    except (TypeError, ValueError):
        return -1


def get_df(use_rarity=False):
    df = conn_mtg.request(conn_mtg.open_query(sys.path[1] + "/Analysis/Card_Costing/Queries/card_properties.sql"))

    df["releaseDate"] = pd.to_datetime(df["releaseDate"])
    df["years"] = (df["releaseDate"] - df["releaseDate"].min()) / np.timedelta64(1, 'Y')
    df = df.drop("releaseDate", axis=1)

    df["n_colors"] = (df[["cost_W", "cost_U", "cost_B", "cost_R", "cost_G"]] > 0).sum(axis=1)
    df["n_colored_symbols"] = df[["cost_W", "cost_U", "cost_B", "cost_R", "cost_G"]].sum(axis=1)

    for col in ["power", "toughness", "loyalty"]:
        df[col] = df[col].apply(to_int)

    # Can only process subtypes after types are processed.
    for col in ["supertypes", "types", "subtypes"]:
        df[col] = df[col].apply(lambda row: row.split(",") if row else [])

        # Don't include creature or planeswalker subtypes.
        if col == "subtypes":
            _df = df[df[["types_Creature", "types_Planeswalker", "types_Tribal"]].sum(axis=1) == 0]
        else:
            _df = df
        values = sorted(list({i for entry in _df[col] for i in entry}))

        for value in values:
            df[f"{col}_{value}"] = df[col].apply(lambda x: any(i in value for i in x)).astype(int)
        df = df.drop(col, axis=1)

    if use_rarity:
        df["rarity_mythic"] = (df["rarity"] == "mythic")
        df["rarity_rare"] = (df["rarity"] == "rare") | df["rarity_mythic"]
        df["rarity_uncommon"] = (df["rarity"] == "uncommon") | df["rarity_rare"]
        df["rarity_common"] = (df["rarity"] == "common") | df["rarity_uncommon"]
        for col in df.columns:
            if "rarity_" in col:
                df[col] = df[col].astype(int)
    df = df.drop("rarity", axis=1)

    df["text"] = df.apply(
        lambda row: tokenize(
            text=row["text"],
            cardname=row["name"],
            reminder_text=True,
            atomic_mana_symbols=True,
            atomic_power_toughness=True,
        ), axis=1
    )

    df["n_words"] = df["text"].apply(lambda x: len(x.split()))
    df["n_abilities"] = df["text"].apply(lambda x: len(x.split("&")))

    return df


if __name__ == "__main__":
    df = get_df()
    print(df.head(10).to_string())
    print(df.describe().to_string())
    print(df[["name", "text"]].head(50).to_string())
    # print({ch for row in df["text"].fillna("") for ch in row if not ch.isalnum()})
