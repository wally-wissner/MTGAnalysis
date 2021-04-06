"""
Preprocessing to create a dataframe of columns the bot can use to generate its questions.
"""


import re

from Conn import conn_mtg
from Utilities.tokenize_cardtext import tokenize


def get_df():
    df = conn_mtg.request(conn_mtg.open_query("Queries/card_properties.sql"))

    df = df.astype({
        "convertedManaCost": int,
    })

    for col in ["supertypes", "types", "subtypes"]:
        df[col] = df[col].apply(lambda row: row.split(",") if row else [])
        values = sorted(list({i for entry in df[col] for i in entry}))
        for value in values:
            df[f"{col}_{value}"] = df[col].apply(lambda x: any(i in value for i in x)).astype(int)
        df = df.drop(col, axis=1)

    df["colors"] = df["colors"].fillna("")
    df["n_colors"] = df["colors"].apply(len)
    df["n_colored_symbols"] = df[["cost_W", "cost_U", "cost_B", "cost_R", "cost_G"]].sum(axis=1)
    df["power_equals_toughness"] = (df["power"] == df["toughness"]).astype(int)

    df["text"] = df.apply(
        lambda row: tokenize(
            text=row["text"],
            cardname=row["name"],
            reminder_text=False,
            atomic_mana_symbols=True,
            atomic_power_toughness=True,
        ), axis=1
    )

    # df["hashed_name"] = df["name"].apply(hash)


    return df


if __name__ == "__main__":
    df = get_df()
    print(df.head(20).to_string())
